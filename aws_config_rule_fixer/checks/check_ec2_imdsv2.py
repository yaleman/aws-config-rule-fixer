"""This should be a config rule but sometimes you just have to check manually..."""

from aws_config_rule_fixer import get_all_regions
import boto3
import click
from loguru import logger


@click.command()
def main() -> None:
    for region in get_all_regions():
        client = boto3.client("ec2", region_name=region)
        response = client.describe_instances()
        for reservations in response["Reservations"]:
            for instance in reservations["Instances"]:
                instance_id = instance["InstanceId"]
                if "MetadataOptions" not in instance:
                    logger.error(
                        "Couldn't get metadata for {} in {}", instance_id, region
                    )
                    continue
                metadata_options = instance["MetadataOptions"]
                http_tokens = metadata_options["HttpTokens"]
                state = metadata_options["State"]

                if http_tokens == "required" and state == "applied":
                    logger.success(
                        "IMDSv2 is enforced on {} in {}", instance_id, region
                    )
                else:
                    logger.error(
                        "IMDSv2 is not enforced on {} in {}", instance_id, region
                    )


if __name__ == "__main__":
    main()
