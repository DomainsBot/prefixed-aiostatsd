import base64
import os
import re
import sys
from typing import Iterable, TextIO

from invoke import task


@task
def test_timing(ctx):
    """Runs test showing the slowest."""
    # module=None means discover.
    # verbosity>=2 starts displaying timing info.
    program = "" \
        "import unittest;" \
        "from mamba_runner.runner import BlackMambaTestRunner;" \
        "unittest.TestProgram(" \
        "    module=None," \
        "    testRunner=BlackMambaTestRunner," \
        "    verbosity=2," \
        ")"
    # mamba_runner does not play well with invoke.
    os.execlp(
        'python',  # File to execute.
        'python', '-c', program,  # Argv.
    )


@task
def test(ctx):
    ctx.run('mypy')

    ctx.run('PYTHONMALLOC=debug coverage run -m unittest')
    ctx.run('coverage report')


@task(post=[test])
def update(ctx):
    """Pull, install reqs and test."""
    ctx.run('git pull || true')
    ctx.run(
        'aws --region us-east-1'
        ' codeartifact login --tool pip --repository production --domain domainsbot-production'
        ' --domain-owner 600475891916'
    )
    ctx.run('pip install -r dev-requirements.txt')
