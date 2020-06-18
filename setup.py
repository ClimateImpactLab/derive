from setuptools import setup, find_packages

setup(
    name="glean",
    version="0.1.0a0",
    description="Tools for processing results of the Climate Prospectus.",
    url="https://github.com/ClimateImpactLab/glean",
    author="James Rising",
    author_email="jarising@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["pyyaml", "numpy", "scipy", "statsmodels", "netCDF4"],
)
