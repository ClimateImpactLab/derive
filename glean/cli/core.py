import click


# This is your main entry point
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def glean_cli():
    """Extract climate impact projection output files"""


@glean_cli.command(help="Extract data from a single netCDF result file")
@click.argument("netcdfpath", type=click.Path())
def single(netcdfpath):
    """Run the glean single system with configuration file"""
    raise NotImplementedError


@glean_cli.command(help="Extract quantiles across collections of results")
@click.argument("confpath", type=click.Path())
@click.option(
    "-c",
    "--conf",
    nargs=1,
    default="",
    multiple=True,
    help="Additional KEY=VALUE configuration option.",
)
def quantiles(confpath, conf):
    """Run the glean quantiles system with configuration file"""
    raise NotImplementedError
