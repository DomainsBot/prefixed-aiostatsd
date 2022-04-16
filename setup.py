from typing import Iterator

from setuptools import setup


def load_requirements(file_name: str) -> Iterator[str]:
    """Returns the dependencies from a pip requirements file."""
    for line in open(file_name):
        if line.startswith("-r"):  # This is an include command to pip.
            for req in load_requirements(line.strip().split(" ", 1)[1].strip()):
                yield req
        elif line.startswith("-") or "://" in line:
            pass  # Ignore other type of pip commands and repository installs.
        else:
            req = line
            for char in "#;":
                try:
                    req = req[: req.index(char)]
                except ValueError:
                    pass  # Char not found.
            req = req.strip()
            if req:
                yield req


setup(
    name="prefixed-aiostatsd",
    version="0.3",
    description="Prefixed AioStatsD",
    classifiers=[
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    author="Domainsbot",
    author_email="tech@domainsbot.com",
    url="www.domainsbot.com",
    packages=[
        "prefixed_aiostatsd",
    ],
    install_requires=list(load_requirements("requirements.txt")),
)
