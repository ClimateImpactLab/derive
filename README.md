# glean

Tools for processing results of the Climate Prospectus.

This is a rough packaging and cleanup of [jrising/prospectus-tools](https://github.com/jrising/prospectus-tools).

## Examples

After an impact projection has completed, running the command
```shell
glean single -c region=CAN.1.2.28 /path/to/projection/output.nc
```
will extract a timeseries for the given country into a local CSV file.

Similarly, given a YAML [configuration file](https://github.com/ClimateImpactLab/glean/blob/master/config-docs.md), we can extract more sophisticated quantiles from the output projection data.

```shell
glean quantiles config.yaml -- outputbasename -historicalbasename
```

Here we're extracting quantiles given a configuration while also defining a glob-like "basename", identifying which output files to extract from. With `-historicalbasename` we're subtracting results from the sum using files with the `historicalbasename` basename pattern.

Much like before, we can add additional configurations that might not be in our configuration file. For example:
```shell
glean quantiles config.yaml \ 
    -c region=USA \
    -- outputbasename -historicalbasename
```
and here we're getting quantile values for the USA, over a given year span:
```shell
glean quantiles config.yaml \ 
    -c region=USA \
    -c yearsets=True \
    outputbasename
```
Use the `--help` option with `glean`, `glean single`, or `glean quantiles` for more details.

## Installation

You can install the package from PyPI with
```shell
pip install glean
```
for a bleeding-edge version:
```shell
pip install git+https:github.com/climateimpactlab/glean
```

## Development and Support

Source code is [hosted online](https://github.com/climateimpactlab/glean) under an Open Source license. Please feel free to file any [bugs and issues](https://github.com/ClimateImpactLab/glean) you find. 

This code is modified from James Rising's jrising/prospectus-tools, which is available under an Open Source MIT license at https://github.com/jrising/prospectus-tools.