import os
from contextlib import suppress

from invoke import Context, task


@task()
def test(ctx: Context) -> None:
    ctx.run("mypy", pty=True)

    ctx.run("PYTHONMALLOC=debug coverage run -m unittest discover", pty=True)
    ctx.run("coverage report", pty=True)


@task()
def test_timing(_: Context) -> None:
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


@task()
def update_tldextract(_: Context) -> None:
    """Update TLDExtract, if installed."""
    with suppress(ImportError):
        import tldextract

        tldextract.TLDExtract().update()


@task(post=[update_tldextract, test])
def update(ctx: Context) -> None:
    """Pull, install reqs and test."""
    ctx.run("git pull || true")

    ctx.run(
        "aws --region us-east-1"
        " codeartifact login --tool pip --repository production --domain domainsbot-production"
        " --domain-owner 600475891916"
    )
    ctx.run("pip install -r dev-requirements.txt")

    # Update the pre-commit hooks then re-apply to the project files
    ctx.run("pre-commit autoupdate", pty=True)
    ctx.run("pre-commit run --all-files", pty=True)


@task(post=[update])
def setup(ctx: Context) -> None:
    """Setup the environment."""
    ctx.run("pre-commit install --install-hooks")

    # Configure pip only within the virtualenv for DomainsBot.
    ctx.run("pip config --site set global.extra-index-url https://pypi.python.org/simple/")
    ctx.run("pip config --site set install.upgrade yes")
    ctx.run("pip config --site set install.upgrade-strategy eager")

    # Add here any other setup steps.


@task()
def clean(ctx: Context) -> None:
    """Cleans build artifacts."""
    ctx.run("rm -rf dist/*")
    ctx.run("rm -rf ./*.egg-info")
    ctx.run("rm -rf build")


@task(post=[clean], pre=[clean])
def publish(ctx: Context) -> None:
    """Build and publish a package to DomainsBot's private repository."""
    ctx.run(
        "aws --region us-east-1 codeartifact login --tool twine --repository production"
        " --domain domainsbot-production --domain-owner 600475891916"
    )
    ctx.run("python setup.py bdist_wheel")
    ctx.run("twine upload dist/*")  # Publish to PyPI.
