import aws_cdk as cdk

from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm
from constructs import Construct


class OrgBucket(s3.Bucket):
    """
    Create custom S3 Bucket with Org defaults.

    1. Enable encryption
    2. Public access blocked
    3. Apply object versioning
    4. Enforce object ownership (disable ACLs)
    5. Enable access logs
    6. Delete incomplete uploads after
    7. Move non-current versions to Infrequent Access
    8. Apply intelligent tiering
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        use_default_lifecycle_rules: bool = True,
        **kwargs,
    ) -> None:
        # The stage name / account where the bucket is deployed
        # I.e. production, staging, development
        self._stage = ssm.StringParameter.value_from_lookup(
            scope=scope,
            parameter_name="/org-platform/stage",
        )

        # Loads the access logs bucket from SSM parameter
        access_logs_bucket = s3.Bucket.from_bucket_arn(
            scope=scope,
            id=f"{id}AccessLogsBucket",
            bucket_arn=ssm.StringParameter.value_from_lookup(
                scope=scope,
                parameter_name="/org-platform/access-logs/bucket/arn",
            ),
        )

        super().__init__(
            scope=scope,
            id=id,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
            server_access_logs_bucket=access_logs_bucket,
            server_access_logs_prefix="S3Logs/",
            transfer_acceleration=kwargs.get("transfer_acceleration", False),
        )

        if use_default_lifecycle_rules:
            self.add_lifecycle_rule(
                abort_incomplete_multipart_upload_after=cdk.Duration.days(amount=7),
                noncurrent_version_transitions=[
                    s3.NoncurrentVersionTransition(
                        storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                        transition_after=cdk.Duration.days(amount=60),
                    )
                ],
                transitions=[
                    s3.Transition(
                        storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                        transition_after=cdk.Duration.days(amount=60),
                    )
                ],
            )
