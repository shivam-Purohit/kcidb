# import sys
# from abc import abstractmethod
# from functools import reduce
# from cached_property import cached_property
import kcidb.db
import kcidb
# from kcidb.misc import LIGHT_ASSERTS
# from kcidb.orm import Type, SCHEMA, Pattern, Source


class ArgumentParser(kcidb.argparse.ArgumentParser):
    """
    Command-line argument parser with common OO arguments added.
    """

    def __init__(self, *args, database=None, **kwargs):
        """
        Initialize the parser, adding common OO arguments.

        Args:
            args:       Positional arguments to initialize ArgumentParser
                        with.
            database:   The default database specification to use, or None to
                        make database specification required.
            kwargs:     Keyword arguments to initialize ArgumentParser with.
        """
        super().__init__(*args, **kwargs)
        kcidb.db.add_args(self, database=database)
        kcidb.orm.add_args(self)


class OutputArgumentParser(kcidb.argparse.OutputArgumentParser):
    """
    Command-line argument parser for tools outputting JSON,
    with common OO arguments added.
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
        kcidb.db.add_args(self, database=database)
        kcidb.orm.add_args(self)
