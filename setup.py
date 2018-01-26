from setuptools import setup


def load_requirements(fn):
    """Returns the dependencies from a pip requirements file."""
    for line in open(fn):
        if line.startswith('-r'):  # This is an include command to pip.
            yield from load_requirements(line.strip().split(' ', 1)[1].strip())
        elif line.startswith('-') or '://' in line:
            pass  # Ignore other type of pip commands and repository installs.
        else:
            req = line
            for char in '#;':
                try:
                    req = req[:req.index(char)]
                except ValueError:
                    pass  # Char not found.
            req = req.strip()
            if req:
                yield req


setup(name='prefixed-aiostatsd',
      version='0.1',
      description='Prefixed AioStatsD',
      author='Domainsbot',
      author_email='steven@domainsbot.com',
      url='www.domainsbot.com',
      packages=[
          'prefixed_aiostatsd',
      ],
      install_requires=list(load_requirements('requirements.txt')),
      )
