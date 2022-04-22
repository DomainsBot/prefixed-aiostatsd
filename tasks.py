import os

from invoke import task


@task
def test(ctx):
    ctx.run("mypy", pty=True)

    ctx.run("PYTHONMALLOC=debug coverage run -m unittest discover", pty=True)
    ctx.run("coverage report", pty=True)


@task
def test_timing(ctx):
    """Runs test showing the slowest."""
    # module=None means discover.
    # verbosity>=2 starts displaying timing info.
    program = (
        "import unittest;"
        "from mamba_runner.runner import BlackMambaTestRunner;"
        "unittest.TestProgram("
        "    module=None,"
        "    testRunner=BlackMambaTestRunner,"
        "    verbosity=2,"
        ")"
    )
    # mamba_runner does not play well with invoke.
    os.execlp(
        "python",  # File to execute.
        # Argv.
        "python",
        "-c",
        program,
    )


@task(post=[test])
def update(ctx):
    """Pull, install reqs and test."""
    ctx.run("git pull || true")

    ctx.run(
        "aws --region us-east-1"
        " codeartifact login --tool pip --repository production --domain domainsbot-production"
        " --domain-owner 600475891916"
    )
    ctx.run("pip install -r dev-requirements.txt")


@task(post=[update])
def setup(ctx):
    """Setup the environment."""
    ctx.run("pre-commit install --install-hooks")

    # Add here any other setup steps.
