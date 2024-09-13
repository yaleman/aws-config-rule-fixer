# import sys
from typing import Optional

# import boto3
import click  # type: ignore
from loguru import logger  # type: ignore

# from aws_config_rule_fixer import get_all_regions


@click.command()
def main(region: Optional[str] = None) -> None:
    """ " does things"""

    logger.info("Using region: {}", region)


if __name__ == "__main__":
    main()
