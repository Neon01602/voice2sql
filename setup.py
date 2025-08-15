from setuptools import setup, find_packages

setup(
    name="voice2sql",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "speechrecognition",
        "mysql-connector-python",
        "psycopg2",
    ],
    entry_points={
        "console_scripts": [
            "voice2sql=voice2sql.cli:main"
        ]
    },
)
