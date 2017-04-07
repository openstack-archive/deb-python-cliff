#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from cliff import command


class TestCommand(command.Command):
    """Description of command.
    """

    def get_parser(self, prog_name):
        parser = super(TestCommand, self).get_parser(prog_name)
        parser.add_argument(
            'long_help_argument',
            help="Create a NIC on the server.\n"
                 "Specify option multiple times to create multiple NICs. "
                 "Either net-id or port-id must be provided, but not both.\n"
                 "net-id: attach NIC to network with this UUID\n"
                 "port-id: attach NIC to port with this UUID\n"
                 "v4-fixed-ip: IPv4 fixed address for NIC (optional)\n"
                 "v6-fixed-ip: IPv6 fixed address for NIC (optional)\n"
                 "none: (v2.37+) no network is attached\n"
                 "auto: (v2.37+) the compute service will automatically "
                 "allocate a network.\n"
                 "Specifying a --nic of auto or none "
                 "cannot be used with any other --nic value.",
        )
        parser.add_argument(
            'regular_help_argument',
            help="The quick brown fox jumps "
                 "over the lazy dog.",
        )
        return parser

    def take_action(self, parsed_args):
        return 42


class TestCommandNoDocstring(command.Command):

    def take_action(self, parsed_args):
        return 42


def test_get_description_docstring():
    cmd = TestCommand(None, None)
    desc = cmd.get_description()
    assert desc == "Description of command.\n    "


def test_get_description_attribute():
    cmd = TestCommand(None, None)
    # Artificially inject a value for _description to verify that it
    # overrides the docstring.
    cmd._description = 'this is not the default'
    desc = cmd.get_description()
    assert desc == 'this is not the default'


def test_get_description_default():
    cmd = TestCommandNoDocstring(None, None)
    desc = cmd.get_description()
    assert desc == ''


def test_get_parser():
    cmd = TestCommand(None, None)
    parser = cmd.get_parser('NAME')
    assert parser.prog == 'NAME'


def test_get_name():
    cmd = TestCommand(None, None, cmd_name='object action')
    assert cmd.cmd_name == 'object action'


def test_run_return():
    cmd = TestCommand(None, None, cmd_name='object action')
    assert cmd.run(None) == 42


def test_smart_help_formatter():
    cmd = TestCommand(None, None)
    parser = cmd.get_parser('NAME')
    expected_help_message = """
  long_help_argument    Create a NIC on the server.
                        Specify option multiple times to create multiple NICs.
                        Either net-id or port-id must be provided, but not
                        both.
                        net-id: attach NIC to network with this UUID
                        port-id: attach NIC to port with this UUID
                        v4-fixed-ip: IPv4 fixed address for NIC (optional)
                        v6-fixed-ip: IPv6 fixed address for NIC (optional)
                        none: (v2.37+) no network is attached
                        auto: (v2.37+) the compute service will automatically
                        allocate a network.
                        Specifying a --nic of auto or none cannot be used with
                        any other --nic value.
  regular_help_argument
                        The quick brown fox jumps over the lazy dog.
"""
    assert expected_help_message in parser.format_help()
