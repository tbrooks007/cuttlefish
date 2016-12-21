import os

from pip.req import parse_requirements
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(os.path.join(here, 'requirements.txt'), session=False)
install_reqs_tests = parse_requirements(os.path.join(here, 'tests/requirements.txt'), session=False)

# get readme text
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

# build list of requirements
reqs = filter(None, [str(ir.req) for ir in install_reqs])
test_reqs = filter(None, [str(ir.req) for ir in install_reqs_tests])

setup(name='cuttlefish',
      version='1.0',
      description='Cuttlefish is a distributed neural network using distributed tensorflow and docker containers. '
                  'This project is a proof of concept library.',
      long_description=README,
      author='VaderGirl13, Rania, Abu and Yu',
      author_email='teresa@quarksandbits.com',
      packages=find_packages(exclude=['tests*']),
      install_requires=reqs,
      extras_require={
        'testing': test_reqs,
      },
)
