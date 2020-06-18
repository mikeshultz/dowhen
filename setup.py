import dowhen

from pathlib import Path
from setuptools import setup, find_packages

this_dir = Path(__file__).parent.absolute()

# Get the long description from the README file
with this_dir.joinpath("README.md").open(encoding="utf-8") as f:
    long_description = f.read()


def requirements_to_list(filename):
    return [
        dep
        for dep in this_dir.joinpath(filename).open().read().split("\n")
        if (dep and not dep.startswith("#"))
    ]


setup(
    name="dowhen",
    version=dowhen.__version__,
    description="A conditional execution system and scheduler.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikeshultz/dowhen",
    author=dowhen.__author__,
    author_email=dowhen.__email__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="conditional execution scheduler",
    packages=find_packages(exclude=["docs", "tests", "scripts", "build"]),
    install_requires=requirements_to_list("requirements.txt"),
    package_data={"": ["README.md",],},
    entry_points={"console_scripts": ["dowhen=dowhen.cli:main",],},
)
