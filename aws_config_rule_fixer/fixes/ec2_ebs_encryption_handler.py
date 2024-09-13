from typing import Optional

import click
from loguru import logger

# from aws_config_rule_fixer import get_all_regions


@click.command()
def main(region: Optional[str] = None) -> None:
    """ " does things"""

    # logger.info("Using region: {}", region)

    logger.error("Ok, this doesn't do anything yet...")


if __name__ == "__main__":
    main()
