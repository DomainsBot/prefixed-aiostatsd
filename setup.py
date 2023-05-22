from collections.abc import Iterator
from contextlib import suppress

from setuptools import setup


def load_requirements(file_name: str) -> Iterator[str]:
    """Returns the dependencies from a pip requirements file."""
    for line in open(file_name, encoding="utf-8"):
        if line.startswith("-r"):  # This is an include command to pip.
            yield from load_requirements(line.strip().split(" ", 1)[1].strip())
        else:
            req = line
            for char in "#;":
                with suppress(ValueError):
                    req = req[: req.index(char)]

            if line.startswith("-") or "://" in line:
                pass  # Ignore other type of pip commands and repository installs.
            else:
                req = req.strip()
                if req:
                    yield req


setup(
    name="prefixed-aiostatsd",
    version="1.1",
    description="Prefixed AioStatsD",
    classifiers=[
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
    ],
    url="https://github.com/DomainsBot/prefixed-aiostatsd",
    author="Domainsbot",
    author_email="tech@domainsbot.com",
    packages=[
        "prefixed_aiostatsd",
    ],
    install_requires=list(load_requirements("requirements.txt")),
    extras_require={
        "dev": list(load_requirements("dev-requirements.txt")),
    },
)
