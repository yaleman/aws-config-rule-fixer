import json
import sys
from typing import Any
import boto3
import click
from loguru import logger
import questionary

from aws_config_rule_fixer import get_all_buckets


def get_policy(bucket: str) -> dict[str, Any]:
    """get a policy"""
    return {
        "Id": "ExamplePolicy",
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowSSLRequestsOnly",
                "Action": "s3:*",
                "Effect": "Deny",
                "Resource": [
                    f"arn:aws:s3:::{bucket}",
                    f"arn:aws:s3:::{bucket}/*",
                ],
                "Condition": {"Bool": {"aws:SecureTransport": "false"}},
                "Principal": "*",
            }
        ],
    }


@click.command()
def main() -> None:
    """does the thing"""
    buckets = get_all_buckets()

    for bucket in buckets:
        logger.info("Bucket: {}", bucket)

        logger.debug("Getting bucket policy")
        policy = None
        try:
            client = boto3.client("s3", region_name=bucket["region"])
            response = client.get_bucket_policy(
                Bucket=bucket["bucket"].name,
            )
            policy = response.get("Policy")
            logger.info(response)
        except Exception as err:
            if "NoSuchBucketPolicy" in str(err):
                logger.debug("No policy! Can yeet one in.")
            else:
                logger.error("Failed to get bucket policy for {}: {}", err)
                sys.exit(1)
        new_policy = get_policy(bucket["bucket"].name)
        if policy is None:
            logger.info("Creating a block policy for {}", bucket["bucket"].name)
            try:
                if questionary.confirm(
                    f"Push a default policy to {bucket['bucket'].name}?"
                ).ask():
                    logger.debug("Pushing policy")
                    client.put_bucket_policy(
                        Bucket=bucket["bucket"].name,
                        Policy=json.dumps(new_policy, default=str),
                    )
                    logger.info(
                        "Policy pushed successfully for {}", bucket["bucket"].name
                    )
                else:
                    logger.info("Skipping {}", bucket["bucket"].name)
            except Exception as error:
                logger.error(
                    "Failed to push policy for {}: {}", bucket["bucket"].name, error
                )
                sys.exit(1)
        # see if the policy's already good
        elif json.loads(policy) == new_policy:
            logger.info(
                "Policy already exists and is set for {}", bucket["bucket"].name
            )
        else:
            logger.error(
                "A policy exists for {} and is different, not going to mess with that one!",
                bucket["bucket"].name,
            )
            logger.info("new policy: {}", json.dumps(new_policy))
            logger.info("existing policy: {}", json.loads(policy))
