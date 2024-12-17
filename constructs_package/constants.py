from enum import StrEnum


class AwsAccountId(StrEnum):
    """AWS account IDs"""

    SANDBOX = "637423243766"
    STAGING = "905418189086"
    PRODUCTION = "730335548799"
    MANAGEMENT = "267631547124"


class AwsRegion(StrEnum):
    """AWS regions"""

    US_EAST_1 = "us-east-1"


class AwsStage(StrEnum):
    """AWS stages"""

    SANDBOX = "sandbox"
    STAGING = "staging"
    PRODUCTION = "production"
    MANAGEMENT = "management"
