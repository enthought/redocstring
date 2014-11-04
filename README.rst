Redocstring: Docstring rendering sphinx extension
=================================================

.. image:: https://travis-ci.org/enthought/sectiondoc.svg?branch=master
   :target: https://travis-ci.org/enthought/sectiondoc
   :alt: Build status

.. image:: https://img.shields.io/coveralls/enthought/sectiondoc.svg
   :target: https://coveralls.io/r/enthought/sectiondoc?branch=master
   :alt: Coverage status


The sectiondoc extension parses the function and class docstrings as
they are retrieved by the autodoc extension and renders the section
blocks into sphinx friendly rst. The extension shares similarities
with alternatives (such as numpydoc) but aims at reflecting the
original form of the docstring.

Key aims of **sectiondoc** are:

    - Do not change the order of sections.
    - Allow sphinx directives between (and inside) section blocks.
    - Easier to debug (native support for debugging) and extend
      (future versions).

Repository
----------

The sectiondoc extension lives at Github. You can clone the repository
using::

    $ git clone https://github.com/enthought/sectiondoc.git


Installation
------------

1. Install ``sectiondoc`` from pypi using pip::

    $ pip install sectiondoc

2. Add sectiondoc to the extensions variable of your sphinx ``conf.py``::

    extensions = [
        ...,
        'sectiondoc',
        ...,
    ]
