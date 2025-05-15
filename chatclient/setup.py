from setuptools import setup, find_packages

setup(
    name="chatclient",
    version="0.1",
    packages=find_packages(),
    py_modules=["cli"],
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "chatclient=cli:main",
        ],
    },
    author="Your Name",
    description="A simple chat client that interacts with a REST API",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)

