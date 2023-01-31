import io
import os
from setuptools import setup, find_packages

__version__ = "2.0.0"

setup(
    author="Oleg Matskiv",
    author_email="alpaca00tuha@gmail.com",
    name="pytest-chic-report",
    version=__version__,
    classifiers=[
        "Framework :: Pytest",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="A pytest plugin to send a report and printing summary of tests.",
    long_description=io.open(
        os.path.join(os.path.dirname("__file__"), "README.md"), encoding="utf-8"
    ).read(),
    long_description_content_type="text/markdown",
    license="MIT",
    include_package_data=True,
    packages=find_packages(include=["pytest_chic_report"]),
    requires=["pytest"],
    keywords=["pytest", "py.test", "pytest summary", "slack", "teams", "pytest report"],
    url="https://github.com/Alpaca00/pytest-summary",
    entry_points={
        "pytest11": [
            "pytest-summary = pytest_chic_report.plugin",
        ]
    },
)
