from enum import Enum


class AwsAccountId(str, Enum):
    """AWS account IDs"""

    SANDBOX = "637423243766"
    STAGING = "905418189086"
    PRODUCTION = "730335548799"
    SHARED_SERVICES = "767397808306"
    MANAGEMENT = "267631547124"


class AwsRegion(str, Enum):
    """AWS regions"""

    US_EAST_1 = "us-east-1"


class AwsStage(str, Enum):
    """AWS stages"""

    SANDBOX = "sandbox"
    STAGING = "staging"
    PRODUCTION = "production"
    SHARED_SERVICES = "shared_services"
    MANAGEMENT = "management"
