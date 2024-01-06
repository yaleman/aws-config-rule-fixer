from pathlib import Path
import re
import sys

import click
from loguru import logger

from aws_config_rule_fixer.pyproject import add_script


@click.command()
@click.argument("rule_name")
def new_rule(rule_name: str) -> None:
    """creates a new rule, give it the dashed-name-version like example-rule-name-here"""

    logger.info("Trying to create a new rule: {}", rule_name)

    valid_rule_name = r"^[a-z0-9-]+-[a-z]+$"
    if re.match(valid_rule_name, rule_name) is None:
        logger.error(
            "Rule name '{}' is invalid, needs to match '{}'", rule_name, valid_rule_name
        )
        sys.exit(1)
    else:
        logger.debug("Rule name '{}' is valid", rule_name)

    rule_file_name = rule_name.replace("-", "_")
    rule_file_path = Path(f"aws_config_rule_fixer/fixes/{rule_file_name}.py")
    if rule_file_path.exists():
        logger.error("Rule file '{}' already exists", rule_file_path)
        sys.exit(1)
    rule_file_path.write_text(
        f"""# {rule_file_path}
import click

@click.command()
def main() -> None:
    \"\"\"{rule_name} fixer\"\"\"

    raise NotImplementedError("This is just a stub, implement me!")
"""
    )
    logger.success("Created {}", rule_file_path)

    # add the script to the pyproject.toml file
    try:
        add_script(
            Path("pyproject.toml"),
            rule_name,
            f"aws_config_rule_fixer.fixes.{rule_file_name}:main",
        )
    except FileNotFoundError as err:
        logger.error("Couldn't find pyproject.toml: {}", err)
        sys.exit(1)
    except ValueError as err:
        logger.error("Failed to add script to pyproject.toml: {}", err)
        sys.exit(1)
    logger.success("Added script to pyproject.toml OK, all done!")


@click.group()
def cli() -> None:
    """AWS Config Rule Fixer"""
    pass


cli.add_command(new_rule)
