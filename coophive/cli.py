"""This module defines the CLI (Command Line Interface) for the Coophive application."""

import json
import os
import subprocess
from datetime import datetime

import click

from coophive import constants, utils

current_time = datetime.now().replace(second=0, microsecond=0)

CLI_TIME = current_time.strftime("%Y-%m-%d_%H-%M")
output_path: str


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--verbose", is_flag=True)
@click.option("--no-color", is_flag=True)
@click.option("--logs-filename", default="coophive-{time}.log")
@click.option(
    "--output-path",
    default="./coophive_output/",
)
def cli(
    verbose: bool,
    no_color: bool,
    logs_filename: str,
    output_path: str,
):
    """Management CLI for CoopHive."""
    constants.VERBOSE = verbose
    constants.NO_COLOR = no_color

    logs_filename = utils.template(logs_filename, dict(time=CLI_TIME))

    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    logs_path = os.path.join(output_dir, logs_filename)

    utils.setup_logger(logs_path=logs_path, verbose=verbose, no_color=no_color)


@cli.command()
@click.option(
    "--role",
    required=True,
)
@click.option(
    "--private-key",
    required=True,
)
@click.option(
    "--public-key",
    required=True,
)
@click.option("--policy-name", required=True, help="Agent Policy.")
@click.option("--inference-endpoint-port", required=True)
@click.option("--initial-offer", default=None)
def run(
    role: str,
    private_key: str,
    public_key: str,
    policy_name: str,
    inference_endpoint_port: str,
    initial_offer: str,
):
    """Run Agent."""
    os.environ["ROLE"] = role

    os.environ["PRIVATE_KEY"] = private_key
    os.environ["PUBLIC_KEY"] = public_key
    os.environ["POLICY_NAME"] = policy_name

    subprocess.Popen(
        [
            "uvicorn",
            "coophive.fastapi_app:app",
            "--reload",
            "--host",
            "localhost",
            "--port",
            inference_endpoint_port,
        ],
    )

    if initial_offer:
        initial_offer = json.loads(initial_offer)
        initial_offer["pubkey"] = public_key
        initial_offer["initial"] = True
        initial_offer["data"]["_tag"] = "offer"

        command = ["redis-cli", "publish", "initial_offers", json.dumps(initial_offer)]
        subprocess.Popen(command)
