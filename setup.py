from setuptools import setup, find_packages

setup(
    name="glean",
    version="0.1.0a0",
    description="",
    url="",
    author="James Rising",
    author_email="jarising@gmail.com",
    license="GNU v. 3",
    packages=find_packages(),
    install_requires=["pyyaml", "numpy", "scipy", "statsmodels", "netCDF4"],
)
