#!/usr/bin/env python

import os

"""
distutils/setuptools install script.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from setuptools import find_packages

# standard package doesn't start with these (we just limit to git for now)
gits = ["git@", "git+ssh"]

def get_package_list(packages):
    std_ps = []
    git_ps = []
    for p in packages:
        for g in gits:
            if p.startswith(g):
                git_ps.append(p)
                break
        std_ps.append(p)
    return std_ps, git_ps

def read_requirements_txt():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    req_file = os.path.join(current_dir, "requirements.txt")
    with open(req_file, "r") as f:
        flines = f.readlines()
    return [l for l in flines if l and not l.startswith("#")]

requirements = read_requirements_txt()
std_ps, git_ps = get_package_list(requirements)

setup(
    name="name_taken_yet",
    version="0.1",
    description="Check if name taken",
    author="Yeuk Hon Wong",
    author_email="yeukhon@acm.org",
    packages=find_packages(exclude=["tests*"]),
    install_requires=std_ps,
    dependency_links=git_ps
)
