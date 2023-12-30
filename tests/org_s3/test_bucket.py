import pytest

from aws_cdk.assertions import Template

from org_cdk.org_s3 import OrgBucket
from org_cdk.org_s3.exceptions import InvalidBucketNameException


class TestOrgBucket:
    @pytest.mark.parametrize(
        "name",
        [("foobar"), ("foo-bar"), ("foo1-bar2"), ("foo1bar2")],
    )
    def test_bucket_name_with_valid_name(self, name, stack):
        bucket = OrgBucket(
            scope=stack,
            id="Bucket",
            name=name,
        )

        actual = bucket.bucket_name
        expected = f"org-development-{name}"

        assert actual == expected

    @pytest.mark.parametrize(
        "name",
        [("foo_bar"), ("foo bar"), ("foo.bar"), ("FooBar"), ("foobar-"), ("foo#bar"), ("org-development-foobar")],
    )
    def test_bucket_name_with_invalid_name(self, name, stack):
        with pytest.raises(InvalidBucketNameException):
            OrgBucket(
                scope=stack,
                id="Bucket",
                name=name,
            )


@pytest.fixture(scope="function", name="template")
def template_fixture(stack):
    OrgBucket(
        scope=stack,
        id="Bucket",
        name="test-bucket",
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
            "BucketName": "org-development-test-bucket",
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
                "LogFilePrefix": "S3Logs/org-development-test-bucket/",
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
