from setuptools import setup, find_packages

setup(
    name="autoproxy",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "reportlab"
    ],
    entry_points={
        "console_scripts": [
            "autoproxy = autoproxy.cli:main"
        ]
    }
)

