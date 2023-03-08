
import math
import datetime
import json
import logging
import threading
import sys
import argparse
import email
import email.message
import email.policy
from abc import ABC, abstractmethod
from google.cloud import pubsub
from google.api_core.exceptions import DeadlineExceeded
import kcidb.io as io
import kcidb.orm
from kcidb import misc
from kcidb.misc import LIGHT_ASSERTS


# Module's logger
LOGGER = logging.getLogger(__name__)

def argparse_add_args(parser):
    """
    Add common message queue arguments to an argument parser.

    Args:
        parser:     The parser to add arguments to.
    """
    parser.add_argument(
        '-p', '--project',
        help='ID of the Google Cloud project with the message queue',
        required=True
    )
    parser.add_argument(
        '-t', '--topic',
        help='Name of the message queue topic',
        required=True
    )


class ArgumentParser(misc.ArgumentParser):
    """
    Command-line argument parser with common message queue arguments added.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the parser, adding common message queue arguments.

        Args:
            args:       Positional arguments to initialize ArgumentParser
                        with.
            kwargs:     Keyword arguments to initialize ArgumentParser with.
        """
        super().__init__(*args, **kwargs)
        argparse_add_args(self)


def argparse_publisher_add_args(parser, data_name):
    """
    Add message queue publisher arguments to an argument parser.

    Args:
        parser:     The parser to add arguments to.
        data_name:  Name of the message queue data.
    """
    argparse_add_args(parser)
    subparsers = parser.add_subparsers(dest="command",
                                       title="Available commands",
                                       metavar="COMMAND",
                                       parser_class=argparse.ArgumentParser)
    subparsers.required = True
    parser.subparsers = {}
    description = f"Initialize {data_name} publisher setup"
    parser.subparsers["init"] = subparsers.add_parser(
        name="init", help=description, description=description
    )
    description = \
        f"Publish {data_name} from standard input, print publishing IDs"
    parser.subparsers["publish"] = subparsers.add_parser(
        name="publish", help=description, description=description
    )
    description = f"Cleanup {data_name} publisher setup"
    parser.subparsers["cleanup"] = subparsers.add_parser(
        name="cleanup", help=description, description=description
    )


class PublisherArgumentParser(misc.ArgumentParser):
    """
    Command-line argument parser with common message queue arguments added.
    """

    def __init__(self, data_name, *args, **kwargs):
        """
        Initialize the parser, adding common message queue arguments.

        Args:
            data_name:  Name of the message queue data.
            args:       Positional arguments to initialize ArgumentParser
                        with.
            kwargs:     Keyword arguments to initialize ArgumentParser with.
        """
        super().__init__(*args, **kwargs)
        self.subparsers = {}
        argparse_publisher_add_args(self, data_name)


def argparse_subscriber_add_args(parser, data_name):
    """
    Add message queue subscriber arguments to an argument parser.

    Args:
        parser:     The parser to add arguments to.
        data_name:  Name of the message queue data.
    """
    argparse_add_args(parser)
    parser.add_argument(
        '-s', '--subscription',
        help='Name of the subscription',
        required=True
    )
    subparsers = parser.add_subparsers(dest="command",
                                       title="Available commands",
                                       metavar="COMMAND",
                                       parser_class=argparse.ArgumentParser)
    subparsers.required = True
    parser.subparsers = {}

    description = f"Initialize {data_name} subscriber setup"
    parser.subparsers["init"] = subparsers.add_parser(
        name="init", help=description, description=description
    )

    description = \
        f"Pull {data_name} with a subscriber, print to standard output"
    parser.subparsers["pull"] = subparsers.add_parser(
        name="pull", help=description, description=description
    )
    parser.subparsers["pull"].add_argument(
        '--timeout',
        metavar="SECONDS",
        type=float,
        help='Wait the specified number of SECONDS for a message, '
             'or "inf" for infinity. Default is "inf".',
        default=math.inf,
        required=False
    )
    parser.subparsers["pull"].add_argument(
        '-m',
        '--messages',
        metavar="NUMBER",
        type=misc.non_negative_int_or_inf,
        help='Pull maximum NUMBER of messages, or "inf" for infinity. '
             'Default is 1.',
        default=1,
        required=False
    )

    description = f"Cleanup {data_name} subscriber setup"
    parser.subparsers["cleanup"] = subparsers.add_parser(
        name="cleanup", help=description, description=description
    )


class SubscriberArgumentParser(misc.ArgumentParser):
    """
    Command-line argument parser with message queue subscriber arguments
    added.
    """

    def __init__(self, data_name, *args, **kwargs):
        """
        Initialize the parser, adding message queue subscriber arguments.

        Args:
            data_name:  Name of the message queue data.
            args:       Positional arguments to initialize ArgumentParser
                        with.
            kwargs:     Keyword arguments to initialize ArgumentParser with.
        """
        super().__init__(*args, **kwargs)
        self.subparsers = {}
        argparse_subscriber_add_args(self, data_name)
