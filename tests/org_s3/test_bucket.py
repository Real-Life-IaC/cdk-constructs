import pytest

from aws_cdk.assertions import Template
from constructs_package.org_s3 import OrgBucket


@pytest.fixture(scope="function", name="template")
def template_fixture(stack):
    OrgBucket(
        scope=stack,
        id="Bucket",
    )
    return Template.from_stack(stack)


# CDK tests
def test_resource_count(template):
    template.resource_count_is(type="AWS::S3::Bucket", count=1)


def test_org_bucket(template):
    template.has_resource_properties(
        type="AWS::S3::Bucket",
        props={
            "BucketEncryption": {
                "ServerSideEncryptionConfiguration": [{"ServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
            },
            "LifecycleConfiguration": {
                "Rules": [
                    {
                        "AbortIncompleteMultipartUpload": {"DaysAfterInitiation": 7},
                        "NoncurrentVersionTransitions": [{"StorageClass": "STANDARD_IA", "TransitionInDays": 60}],
                        "Status": "Enabled",
                        "Transitions": [{"StorageClass": "INTELLIGENT_TIERING", "TransitionInDays": 60}],
                    }
                ]
            },
            "LoggingConfiguration": {
                "DestinationBucketName": "org-development-access-logs",
                "LogFilePrefix": "S3Logs/",
            },
            "OwnershipControls": {"Rules": [{"ObjectOwnership": "BucketOwnerEnforced"}]},
            "PublicAccessBlockConfiguration": {
                "BlockPublicAcls": True,
                "BlockPublicPolicy": True,
                "IgnorePublicAcls": True,
                "RestrictPublicBuckets": True,
            },
            "VersioningConfiguration": {"Status": "Enabled"},
        },
    )
