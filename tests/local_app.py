"""
Use this class for local cdk synth, manual deploy to development account, and to run checkov tests
"""

import aws_cdk as cdk

from constructs import Construct
from org_cdk.org_s3 import OrgBucket


class LocalTestBucketStack(cdk.Stack):
    """Local test/deploy of bucket"""

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        bucket = OrgBucket(
            scope=self,
            id="Bucket",
            name="test-bucket",
        )

        bucket.apply_removal_policy(policy=cdk.RemovalPolicy.DESTROY)


env = cdk.Environment(account="123456789012", region="us-east-1")

app = cdk.App()

LocalTestBucketStack(
    scope=app,
    id="LocalTestBucketStack",
    env=env,
)

app.synth()
