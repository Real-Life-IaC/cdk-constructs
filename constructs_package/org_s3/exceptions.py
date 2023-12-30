from typing import Optional


class InvalidBucketNameException(Exception):
    """
    Exception raised for errors in the bucket name.

    Args:
        bucket_name (str): Input bucket name which caused the error.
        pattern (str): The regex pattern that the bucket name must follow.
        message (str): Human readable explanation of the error.

    Attributes:
        bucket_name (str): Input bucket name which caused the error.
        pattern (str): The regex pattern that the bucket name must follow.
        message (str): Human readable explanation of the error.
    """

    default_message_list = [
        "Invalid S3 bucket name (value: {bucket_name})\n\n",
        "The bucket name must follow the pattern: `{pattern}`.\n"
        "Bucket names can consist only of lowercase letters, "
        "numbers and hyphens (-) and must end with a letter or number.\n"
        "The prefix `util-(stage)-` is added automatically.",
    ]

    def __init__(self, bucket_name: str, pattern: str, message: Optional[str] = None) -> None:
        self.bucket_name = bucket_name
        self.pattern = pattern

        if message:
            self.message = message
        else:
            self.message = "".join(self.default_message_list).format(
                bucket_name=self.bucket_name, pattern=self.pattern
            )

        super().__init__(self.message)
