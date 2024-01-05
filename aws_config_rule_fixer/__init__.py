from typing import Generator
import boto3


def get_all_regions() -> list[str]:
    """returns a list of regions"""

    client = boto3.client("ec2", region_name="us-east-1")
    return [region["RegionName"] for region in client.describe_regions()["Regions"]]


def get_all_buckets() -> Generator[dict[str, str], None, None]:
    """returns all bucket names across all regions"""
    # for region in get_all_regions():
    region = "us-east-1"
    s3 = boto3.resource("s3", region_name=region)
    for bucket in s3.buckets.all():
        yield {"bucket": bucket, "region": region}
