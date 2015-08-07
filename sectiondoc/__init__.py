# -----------------------------------------------------------------------------
#  file: __init__.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-2014, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
try:  # pragma: no cover
    from sectiondoc._version import full_version as __version__
except ImportError:  # pragma: no cover
    __version__ = "not-built"

from sectiondoc.styles.legacy import setup

__all__ = ['__version__', 'setup']
