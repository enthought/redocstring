import sys

if sys.version_info >= (2, 7):
    import unittest  # noqa
else:
    import unittest2 as unittest  # noqa
