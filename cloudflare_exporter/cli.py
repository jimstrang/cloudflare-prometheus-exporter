# -*- coding: utf-8 -*-

"""Console script for cloudflare_exporter."""
import sys
import yaml
import click
import logging
import logging.config
from importlib import resources
from .cloudflare_exporter import run_exporter

LOGGER = logging.getLogger("stdout")
_load_logging_yaml = yaml.load


def configure_logging():
    log_cfg = _load_logging_yaml(
        resources.files("cloudflare_exporter")
        .joinpath("logging.yaml")
        .read_text(encoding="utf-8"),
        Loader=yaml.SafeLoader,
    )
    logging.config.dictConfig(log_cfg)


@click.group(invoke_without_command=True)
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def main(ctx, debug):
    """Console script for cloudflare_exporter."""
    configure_logging()
    LOGGER.debug(
        "Running cloudflare_exporter in %s mode", "debug" if debug else "standard"
    )
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
@click.argument("config", type=click.File("rb"))
def export(config):
    LOGGER.debug("parallel export mode")
    config_dict = yaml.load(config, Loader=yaml.FullLoader)
    run_exporter(config_dict)


@main.command()
def get():
    LOGGER.debug("get mode")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
