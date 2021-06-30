#!/usr/bin/env python
from setuptools import setup

NAME = "hypertk"
setup(
    name=NAME,
    use_scm_version={
        "local_scheme": "dirty-tag",
        "write_to": f"{NAME}/_version.py",
        "fallback_version": "0.0.0",
    },
    author="Ross Fenning",
    author_email="github@rossfenning.co.uk",
    packages=[NAME],
    package_data={NAME: ["py.typed"]},
    description="Hypermedia Toolkit",
    setup_requires=[
        "setuptools_scm>=3.3.1",
        "pre-commit",
    ],
    install_requires=["doltcli"],
    extras_require={
        "test": ["pytest", "hypothesis", "pytest-pikachu", "pytest-mypy"],
    },
)
