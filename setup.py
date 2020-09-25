from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = f.read().strip().split("\n")

setup(
    name="derive",
    use_scm_version=True,
    description="Tools for processing results of the Climate Prospectus.",
    url="https://github.com/ClimateImpactLab/derive",
    author="James Rising",
    author_email="jarising@gmail.com",
    license="MIT",
    project_urls={
        "Source": "https://github.com/ClimateImpactLab/derive",
        "Tracker": "https://github.com/ClimateImpactLab/derive/issues",
    },
    zip_safe=False,
    install_requires=requirements,
    setup_requires=["setuptools_scm"],
    entry_points="""
    [console_scripts]
    derive=derive.cli:derive_cli
""",
)
