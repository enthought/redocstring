# -----------------------------------------------------------------------------
#  file: __init__.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-2014, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
__all__ = ['__version__', 'setup']

try:  # pragma: no cover
    from refactordoc._version import full_version as __version__
except ImportError:  # pragma: no cover
    __version__ = "not-built"

from refactordoc.styles.old_style import setup
