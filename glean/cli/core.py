import click


# This is your main entry point
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def glean_cli():
    """Extract climate impact projection output files"""


@glean_cli.command(help="Extract quantiles across collections of results")
@click.argument("confpath", type=click.Path())
def quantiles(confpath):
    """Run the glean quantiles system with configuration file"""
    raise NotImplementedError


@glean_cli.command(help="Extract data from a single netCDF result file")
@click.argument("confpath", type=click.Path())
def single(confpath):
    """Run the glean single system with configuration file"""
    raise NotImplementedError
