# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  License: LICENSE.TXT
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from setuptools import setup, find_packages

MAJOR = 1
MINOR = 0
MICRO = 0
DEV = 0

VERSION = '{0:d}.{1:d}.{2:d}'.format(MAJOR, MINOR, MICRO)
FULLVERSION = '{0:d}.{1:d}.{2:d}'.format(MAJOR, MINOR, MICRO, DEV)
IS_RELEASED = False


def write_version_py(filename='sectiondoc/_version.py'):
    template = """\
# THIS FILE IS GENERATED FROM SECTIONDOC SETUP.PY
version = '{version}'
full_version = '{full_version}'
is_released = {is_released}

if not is_released:
    version = full_version
"""
    with open(filename, "wt") as fp:
        fp.write(template.format(
            version=VERSION,
            full_version=FULLVERSION,
            is_released=IS_RELEASED))


if __name__ == "__main__":
    write_version_py()
    from sectiondoc import __version__

    setup(
        name='sectiondoc',
        version=__version__,
        packages=find_packages(),
        author="Enthought Ltd",
        author_email="info@enthought.com",
        test_suite='sectiondoc.tests',
    )
