# AWS Config rule fixer

... run these at your own risk blah blah

## Installation

Clone the repo, create a venv and `pip install .`, or `poetry install && poetry run <scriptname>`

## Scripts

- s3-bucket-ssl-requests-only - applies a blanked "if you're not coming from HTTPS then deny" policy.
