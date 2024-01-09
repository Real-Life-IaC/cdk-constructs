from enum import Enum


class AwsAccountId(Enum, str):
    """AWS account IDs"""

    SANDBOX = "637423243766"
    STAGING = "905418189086"
    PRODUCTION = "730335548799"
    SHARED_SERVICES = "767397808306"
    MANAGEMENT = "267631547124"
