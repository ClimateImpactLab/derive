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
    license="MIT license",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    project_urls={
        "Source": "https://github.com/ClimateImpactLab/derive",
        "Tracker": "https://github.com/ClimateImpactLab/derive/issues",
    },
    packages=find_packages(include=["derive", "derive.*"]),
    include_package_data=True,
    keywords="derive",
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=requirements,
    setup_requires=["setuptools_scm"],
    entry_points="""
    [console_scripts]
    derive=derive.cli:derive_cli
""",
)
