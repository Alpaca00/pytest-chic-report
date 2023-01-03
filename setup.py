from setuptools import setup, find_packages

setup(
    name="pytest-summary",
    version="0.1.0",
    description="A pytest plugin to send a report and printing summary of tests.",
    author="Oleg Matskiv",
    author_email="alpaca00tuha@gmail.com",
    license="MIT",
    packages=find_packages(include=['pytest_summary']),
    requires=["pytest"],
    entry_points={
        'pytest11': [
            'pytest-summary = pytest_summary.plugin',
        ]
    }
)
