import sys
import logging
import argparse
import datetime
import kcidb.io as io
import kcidb.orm
import kcidb.misc
from kcidb.misc import LIGHT_ASSERTS
from kcidb.db import abstract, schematic, mux, \
    bigquery, postgresql, sqlite, json, null, misc, argparse # noqa: F401



def add_args(parser, database=None):
    """
    Add common database arguments to an argument parser.

    Args:
        parser:     The parser to add arguments to.
        database:   The default database specification to use.
    """
    assert database is None or isinstance(database, str)
    parser.add_argument(
        '-d', '--database',
        help=("Specify DATABASE to use, formatted as <DRIVER>:<PARAMS>. " +
              "Use --database-help for more details." +
              ("" if database is None
               else f"Default is {database!r}.")),
        default=database,
        required=(database is None)
    )
    parser.add_argument(
        '--database-help',
        action=DBHelpAction,
        help='Print documentation on database specification strings and exit.'
    )


class ArgumentParser(kcidb.argparse.ArgumentParser):
    """
    Command-line argument parser with common database arguments added.
    """

    def __init__(self, *args, database=None, **kwargs):
        """
        Initialize the parser, adding common database arguments.

        Args:
            args:       Positional arguments to initialize ArgumentParser
                        with.
            database:   The default database specification to use, or None to
                        make database specification required.
            kwargs:     Keyword arguments to initialize ArgumentParser with.
        """
        super().__init__(*args, **kwargs)
        add_args(self, database=database)


class OutputArgumentParser(kcidb.argparse.OutputArgumentParser):
    """
    Command-line argument parser for tools outputting JSON,
    with common database arguments added.
    """

    def __init__(self, *args, database=None, **kwargs):
        """
        Initialize the parser, adding JSON output arguments.

        Args:
            args:       Positional arguments to initialize ArgumentParser
                        with.
            database:   The default database specification to use, or None to
                        make database specification required.
            kwargs:     Keyword arguments to initialize ArgumentParser with.
        """
        super().__init__(*args, **kwargs)
        add_args(self, database=database)


class SplitOutputArgumentParser(kcidb.argparse.SplitOutputArgumentParser):
    """
    Command-line argument parser for tools outputting split-report streams,
    with common database arguments added.
    """

    def __init__(self, *args, database=None, **kwargs):
        """
        Initialize the parser, adding split-report output arguments.

        Args:
            args:       Positional arguments to initialize ArgumentParser
                        with.
            database:   The default database specification to use, or None to
                        make database specification required.
            kwargs:     Keyword arguments to initialize ArgumentParser with.
        """
        super().__init__(*args, **kwargs)
        add_args(self, database=database)


# No, it's OK, pylint: disable=too-many-ancestors
class QueryArgumentParser(SplitOutputArgumentParser):
    """
    Command-line argument parser with common database query arguments added.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the parser, adding common database query arguments.

        Args:
            args:   Positional arguments to initialize the parent
                    SplitOutputArgumentParser with.
            kwargs: Keyword arguments to initialize the parent
                    SplitOutputArgumentParser with.
        """
        super().__init__(*args, **kwargs)

        self.add_argument(
            '-c', '--checkout-id',
            metavar="ID",
            default=[],
            help='ID of a checkout to match',
            dest="checkout_ids",
            action='append',
        )
        self.add_argument(
            '-b', '--build-id',
            metavar="ID",
            default=[],
            help='ID of a build to match',
            dest="build_ids",
            action='append',
        )
        self.add_argument(
            '-t', '--test-id',
            metavar="ID",
            default=[],
            help='ID of a test to match',
            dest="test_ids",
            action='append',
        )

        self.add_argument(
            '--parents',
            help='Match parents of matching objects',
            action='store_true'
        )
        self.add_argument(
            '--children',
            help='Match children of matching objects',
            action='store_true'
        )
