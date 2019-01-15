#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
sqblack.cli
~~~~~~~~~~~

Single Quotes Black CLI
'''

# Import Python libs
import re

# Import 3rd-party libs
import black
from blib2to3.pgen2 import driver, token
from blib2to3.pytree import Leaf

# Let the patching being
black.DEFAULT_LINE_LENGTH = 100


def normalize_string_quotes(leaf: Leaf) -> None:
    '''Prefer double quotes but only if it doesn't cause more escaping.
    Adds or removes backslashes as appropriate. Doesn't parse and fix
    strings nested in f-strings (yet).
    Note: Mutates its argument.

    SaltStack prefers single quotes over double quotes
    '''
    value = leaf.value.lstrip('furbFURB')
    if value[:3] == "'''":
        return

    elif value[:3] == '"""':
        orig_quote = '"""'
        new_quote = "'''"
    elif value[0] == '"':
        orig_quote = '"'
        new_quote = "'"
    else:
        orig_quote = "'"
        new_quote = '"'
    first_quote_pos = leaf.value.find(orig_quote)
    if first_quote_pos == -1:
        return  # There's an internal error

    prefix = leaf.value[:first_quote_pos]
    unescaped_new_quote = re.compile(rf'(([^\\]|^)(\\\\)*){new_quote}')
    escaped_new_quote = re.compile(rf'([^\\]|^)\\((?:\\\\)*){new_quote}')
    escaped_orig_quote = re.compile(rf'([^\\]|^)\\((?:\\\\)*){orig_quote}')
    body = leaf.value[first_quote_pos + len(orig_quote) : -len(orig_quote)]
    if 'r' in prefix.casefold():
        if unescaped_new_quote.search(body):
            # There's at least one unescaped new_quote in this raw string
            # so converting is impossible
            return

        # Do not introduce or remove backslashes in raw strings
        new_body = body
    else:
        # remove unnecessary escapes
        new_body = black.sub_twice(escaped_new_quote, rf'\1\2{new_quote}', body)
        if body != new_body:
            # Consider the string without unnecessary escapes as the original
            body = new_body
            leaf.value = f'{prefix}{orig_quote}{body}{orig_quote}'
        new_body = black.sub_twice(escaped_orig_quote, rf'\1\2{orig_quote}', new_body)
        new_body = black.sub_twice(unescaped_new_quote, rf'\1\\{new_quote}', new_body)
    if 'f' in prefix.casefold():
        matches = re.findall(r'[^{]\{(.*?)\}[^}]', new_body)
        for m in matches:
            if '\\' in str(m):
                # Do not introduce backslashes in interpolated expressions
                return
    if new_quote == '"""' and new_body[-1:] == '"':
        # edge case:
        new_body = new_body[:-1] + '\\"'
    orig_escape_count = body.count('\\')
    new_escape_count = new_body.count('\\')
    if new_escape_count > orig_escape_count:
        return  # Do not introduce more escaping

    if new_escape_count == orig_escape_count and orig_quote == "'":
        return  # Prefer single quotes

    leaf.value = f'{prefix}{new_quote}{new_body}{new_quote}'


black.normalize_string_quotes = normalize_string_quotes


def main():
    try:
        black.patched_main()
    except AttributeError:
        # Black <= 19.9b0
        black.patch_click()
        black.main()


if __name__ == '__main__':
    main()
