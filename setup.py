import io
import os
from setuptools import setup, find_packages

setup(
    name="pytest-summary",
    version="0.1.0",
    description="A pytest plugin to send a report and printing summary of tests.",
    author="Oleg Matskiv",
    author_email="alpaca00tuha@gmail.com",
    long_description=io.open(os.path.join(os.path.dirname('__file__'), 'README.md'), encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    license="MIT",
    packages=find_packages(include=['pytest_summary']),
    requires=["pytest"],
    url="https://github.com/Alpaca00/pytest-summary",
    entry_points={
        'pytest11': [
            'pytest-summary = pytest_summary.plugin',
        ]
    }
)
