from setuptools import setup, find_packages

setup(
    name="crypto",
    version="0.0.1",
    packages=["cryptobot", "cryptohistory", "cryptocore"],
    install_requires=[
        "ccxt",
        "cfscrape",
        "python-binance",
        "requests",
        "websockets"
    ]
)
