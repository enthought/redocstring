import re

function_regex = re.compile(r'\w+\(.*\)\s*')
signature_regex = re.compile('\((.*)\)')
header_regex = re.compile(r'\s:\s?')
definition_regex = re.compile(r"""
\*{0,2}            #  no, one or two stars
\w+\s:             #  a word followed by a space and a semicolumn
(
        \s         # just a space
    |              # OR
        \s[\w.]+   # dot separated words
        (\(.*\))?  # with maybe a signature
    |
        \s[\w.]+   # dot separated words
        (\(.*\))?
        \sor       # with an or in between
        \s[\w.]+
        (\(.*\))?
)?
$                  # match at the end of the line
""", re.VERBOSE)
