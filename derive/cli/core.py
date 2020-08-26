import click
from yaml import safe_load
import derive.api
from derive.api.configs import read_config


# This is your main entry point
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def derive_cli():
    """Extract climate impact projection output files"""


@derive_cli.command(help="Extract data from a single netCDF result file")
@click.argument("netcdfpath", required=True, type=click.Path(exists=True))
@click.option(
    "-c",
    "--conf",
    nargs=1,
    default="",
    multiple=True,
    help="Additional KEY=VALUE configuration option.",
)
def single(netcdfpath, conf):
    """Run the derive single system with configuration file"""
    # Parse CLI config values as yaml str before merging.
    arg_configs = {}
    for k, v in (arg.strip().split("=") for arg in conf):
        arg_configs[k] = yaml.safe_load(v)

    derive.api.single([netcdfpath], arg_configs)


@derive_cli.command(help="Extract quantiles across collections of results")
@click.argument("confpath", required=True, type=click.Path(exists=True))
@click.option(
    "-c",
    "--conf",
    nargs=1,
    default="",
    multiple=True,
    help="Additional KEY=VALUE configuration option.",
)
@click.argument("basenames", nargs=-1)
def quantiles(confpath, basenames, conf):
    """Run the derive quantiles system with configuration file"""
    file_configs = read_config(confpath)

    # Parse CLI config values as yaml str before merging.
    arg_configs = {}
    for k, v in (arg.strip().split("=") for arg in conf):
        arg_configs[k] = yaml.safe_load(v)
    file_configs.update(arg_configs)

    derive.api.quantiles(basenames, file_configs)
