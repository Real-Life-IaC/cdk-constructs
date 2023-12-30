import json
import os

import aws_cdk as cdk
import pytest

from constructs import Construct


class Stack(cdk.Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


@pytest.fixture(scope="function", name="stack")
def stack_fixture():
    cdk_context = os.path.join(os.getcwd(), "cdk.context.json")

    with open(cdk_context, "r") as file:
        context = json.loads(file.read())

    app = cdk.App(context=context)

    return Stack(
        scope=app,
        id="CdkTestStack",
        env=cdk.Environment(account="123456789012", region="us-east-1"),
    )
