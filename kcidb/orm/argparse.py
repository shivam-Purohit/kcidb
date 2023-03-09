

import re
import textwrap
import logging
import argparse
from abc import ABC, abstractmethod
import jsonschema
import kcidb.io as io
import kcidb.misc
import kcidb
import __init__ 
from kcidb.misc import LIGHT_ASSERTS

# We'll get to it, pylint: disable=too-many-lines


# Module's logger
LOGGER = logging.getLogger(__name__)


def add_args(parser):
    """
    Add common ORM arguments to an argument parser.

    Args:
        The parser to add arguments to.
    """
    parser.add_argument(
        'pattern_strings',
        nargs='*',
        default=[],
        metavar='PATTERN',
        help='Object-matching pattern. '
             'See pattern documentation with --pattern-help.'
    )
    parser.add_argument(
        '--pattern-help',
        action=__init__.PatternHelpAction,
        help='Print pattern string documentation and exit.'
    )


class ArgumentParser(kcidb.argparse.ArgumentParser):
    """
    Command-line argument parser with common ORM arguments added.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the parser, adding common ORM arguments.

        Args:
            args:   Positional arguments to initialize ArgumentParser with.
            kwargs: Keyword arguments to initialize ArgumentParser with.
        """
        super().__init__(*args, **kwargs)
        add_args(self)


class OutputArgumentParser(kcidb.argparse.OutputArgumentParser):
    """
    Command-line argument parser for tools outputting JSON,
    with common ORM arguments added.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the parser, adding JSON output arguments.

        Args:
            args:   Positional arguments to initialize ArgumentParser with.
            kwargs: Keyword arguments to initialize ArgumentParser with.
        """
        super().__init__(*args, **kwargs)
        add_args(self)
