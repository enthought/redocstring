Docstring refactoring
#####################

RefactorDoc sphinx extension is designed to re-factor the doc-strings of
python objects. The sections are replaced (in-place) by sphinx friendly rst and
the rest of the doc-string is left untouched. Thus the original form remains as
intended by the author.

Extension hooks on the 'autodoc-process-docstring' event to receive the
automatically discovered and extracted docstring of the python objects. Given
the type of the object that is processed at the time ``refactordoc`` creates
the respective refactoring object and executes the objects parsing method.


.. todo:: Workflow diagrams

