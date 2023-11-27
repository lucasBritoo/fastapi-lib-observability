from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'requirements/dev.txt')) as f:
    install_reqs = f.read().splitlines()

setup(
    include_package_data=True,
    name='fastapi_lib_observability',
    version="0.0.1",
    description='Libray to plug-in-play observability in FastAPI applications',
    author='Lucas Brito',
    author_email='britol599@gmail.com',
    
    package_dir={'': 'src'},
    packages=find_packages(
        where='src'
    ),

    install_requires = install_reqs,

    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ]
)