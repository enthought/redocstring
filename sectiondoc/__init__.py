# -----------------------------------------------------------------------------
#  file: __init__.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-2014, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
__all__ = ['__version__', 'setup']

try:  # pragma: no cover
    from sectiondoc._version import full_version as __version__
except ImportError:  # pragma: no cover
    __version__ = "not-built"


def setup(app):
    import warnings
    from sectiondoc.styles.old_style import setup
    warnings.warn(
        "This entry-point will be removed in the next release"
        "Please use 'reafactordoc.styles.old_style' in conf.py",
        DeprecationWarning)
    setup(app)
