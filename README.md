# AWS Config rule fixer

... run these at your own risk blah blah

## Installation

Clone the repo, create a venv and `pip install .`, or `uv run <scriptname>`

## Fixes

These are pretty splashy but if you've read the code then it's an easy fix.

- ec2-ebs-encryption-by-default - does what it says on the tin
- s3-bucket-ssl-requests-only - applies a blanked "if you're not coming from HTTPS then deny" policy.

## Checks

- check-ec2-imdsv2 - Checks every EC2 instance to make sure they have Instance Metadata V2 enforced.
