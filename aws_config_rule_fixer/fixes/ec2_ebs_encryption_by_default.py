import boto3
import sys

from loguru import logger

from aws_config_rule_fixer import get_all_regions


def main() -> None:
    regions = get_all_regions()
    for region in regions:
        client = boto3.client("ec2", region_name=region)
        try:
            logger.info("Setting EBS encryption by default in {}", region)
            client.enable_ebs_encryption_by_default()
            logger.info("Done! {} is good", region)
        except Exception as error:
            logger.error(
                "Failed to set EBS encryption by default in {}: {}", region, error
            )
            sys.exit(1)
    logger.info("All set on {}", ",".join(regions))


if __name__ == "__main__":
    main()
