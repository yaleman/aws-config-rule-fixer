import boto3
import sys

from loguru import logger

from aws_config_rule_fixer import get_all_regions


def main() -> None:
    regions = get_all_regions()
    for region in regions:
        client = boto3.client("ec2", region_name=region)
        try:
            groups = client.describe_security_groups(
                Filters=[
                    {
                        "Name": "group-name",
                        "Values": [
                            "default",
                        ],
                    },
                ],
            )
            for group in groups.get("SecurityGroups", []):
                group_id = group["GroupId"]
                if (
                    group.get("IpPermissionsEgress")
                    and group.get("GroupName") == "default"
                ):
                    logger.info("Removing egress rules from group={}", group_id)
                    logger.debug(group)
                    client.revoke_security_group_egress(
                        GroupId=group_id,
                        IpPermissions=group["IpPermissionsEgress"],
                    )
                else:
                    logger.success(
                        "group id={} in region={} already has no egress rules",
                        group_id,
                        region,
                    )
        except Exception as error:
            logger.error("Failed to handle groups in region={}: {}", region, error)
            sys.exit(1)
    logger.info("All set on {}", ",".join(regions))


if __name__ == "__main__":
    main()
