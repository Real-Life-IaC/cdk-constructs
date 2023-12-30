import re

import aws_cdk as cdk

from aws_cdk import aws_s3 as s3
from aws_cdk import aws_ssm as ssm

from constructs import Construct
from constructs.org_s3.exceptions import InvalidBucketNameException


class OrgBucket(s3.Bucket):
    """
    Create custom S3 Bucket with Org defaults.

    1. Enforce name convention: org-(production|staging|development)-(name)
    1. Enable encryption
    1. Public access blocked
    1. Apply object versioning
    1. Enforce object ownership (disable ACLs)
    1. Enable access logs
    1. Delete incomplete uploads after
    1. Move non-current versions to Infrequent Access
    1. Apply intelligent tiering

    Raises:
        InvalidBucketNameException: If the name doesn't follow the requirements
    """

    def __init__(
        self,
        scope: Construct,
        id: str,
        name: str,
        use_default_lifecycle_rules: bool = True,
        **kwargs,
    ) -> None:
        self.name = name

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
            scope,
            id,
            bucket_name=self.bucket_name,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
            object_ownership=s3.ObjectOwnership.BUCKET_OWNER_ENFORCED,
            server_access_logs_bucket=access_logs_bucket,
            server_access_logs_prefix=f"S3Logs/{self.bucket_name}/",
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

    @property
    def bucket_name(self) -> str:
        """
        Compose the bucket name and validate if it follows the pattern.

        Returns:
            The validated bucket name
        """
        bucket_name = f"org-{self._stage}-{self.name}"

        pattern = "^org-(production|staging|development)-([a-z]|[0-9]|-)+([a-z]|[0-9])$"

        if not re.match(pattern, bucket_name):
            raise InvalidBucketNameException(bucket_name=bucket_name, pattern=pattern)

        if len(re.findall("org-(production|staging|development)", bucket_name)) > 1:
            raise InvalidBucketNameException(bucket_name=bucket_name, pattern=pattern)

        return bucket_name
