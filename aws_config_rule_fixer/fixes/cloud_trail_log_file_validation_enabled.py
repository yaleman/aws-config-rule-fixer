# aws_config_rule_fixer/fixes/cloud_trail_log_file_validation_enabled.py
import sys
import click
import boto3
from loguru import logger

from aws_config_rule_fixer import get_all_regions


@click.command()
def main() -> None:
    """cloud-trail-log-file-validation-enabled fixer"""

    region = "us-east-1"

    already_done_arns = []

    for region in get_all_regions():
        client = boto3.client("cloudtrail", region_name=region)
        for trail in client.describe_trails()["trailList"]:
            trail_arn = trail.get("TrailARN")
            if trail_arn in already_done_arns:
                logger.debug("Already seen {}", trail_arn)
                continue
            already_done_arns.append(trail_arn)
            logger.debug(trail)
            if trail["LogFileValidationEnabled"]:
                logger.info(
                    "LogFileValidationEnabled already enabled for {}", trail_arn
                )
            else:
                logger.info("Enabling LogFileValidationEnabled for {}", trail_arn)
                try:
                    response = client.update_trail(
                        Name=trail_arn,
                        EnableLogFileValidation=True,
                    )
                    logger.debug(response)
                except Exception as error:
                    logger.error("Failed to update {}: {}", trail_arn, error)
                    sys.exit(1)
                logger.success("Enabled LogFileValidationEnabled for {}", trail_arn)
