import click
import glean.api
from glean.api.configs import read_config


# This is your main entry point
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def glean_cli():
    """Extract climate impact projection output files"""


@glean_cli.command(help="Extract data from a single netCDF result file")
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
    """Run the glean single system with configuration file"""
    arg_configs = dict(arg.strip().split("=") for arg in conf)
    glean.api.single([netcdfpath], arg_configs)


@glean_cli.command(help="Extract quantiles across collections of results")
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
    """Run the glean quantiles system with configuration file"""
    file_configs = read_config(confpath)

    arg_configs = dict(arg.strip().split("=") for arg in conf)
    file_configs.update(arg_configs)

    glean.api.quantiles(basenames, file_configs)
