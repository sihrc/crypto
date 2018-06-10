from setuptools import setup, find_packages

setup(
    name="crypto",
    version="0.0.1",
    packages=["cryptobot", "cryptocore"],
    install_requires=[
        "ccxt",
        "cfscrape",
        "pandas",
        "python-binance",
        "requests",
        "websockets"
    ]
)