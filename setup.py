from setuptools import setup, find_packages

setup(
    name="derive",
    use_scm_version=True,
    description="Tools for processing results of the Climate Prospectus.",
    url="https://github.com/ClimateImpactLab/derive",
    author="James Rising",
    author_email="jarising@gmail.com",
    license="MIT",
    packages=find_packages(),
    zip_safe=False,
    install_requires=["click", "pyyaml", "numpy", "scipy", "statsmodels", "netCDF4"],
    setup_requires=["setuptools_scm"],
    extras_require={
        "test": ["pytest"],
        "dev": ["pytest", "pytest-cov", "pytest-mock", "wheel", "flake8", "black", "twine"],
    },
    entry_points="""
    [console_scripts]
    derive=derive.cli:derive_cli
""",
)
