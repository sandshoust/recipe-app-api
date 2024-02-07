"""
Test custom Django management commands"""

from unittest.mock import patch
# change as name to another error
from psycopg2 import OperationalError as Psycopg2OpError
# simulate call commands
from django.core.management import call_command
from django.db.utils import OperationalError
# use to test our unit test - just using simple to simulate db
from django.test import SimpleTestCase

# mock behaviour of the database with the patch command so these tests will run
# basecomand has a function command check


@patch('core.management.commands.wait_for_db.Command.check')
# corres  patched_check parameter in method test_...ready
class CommandTests(SimpleTestCase):
    """Test commands"""

    # when check is called we use patched_check variable
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if databse ready"""
        patched_check.return_value = True

        # checks database ready and set up correctly
        call_command('wait_for_db')

        # check test is called with database default
        patched_check.assert_called_once_with(databases=['default'])

    # test behaviour when database is not ready - patch is just for this method
    # this overrides behavious of sleep with a mock
    @patch('time.sleep')  # corresponds to patch_sleep in args below
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when get operation error """

        # testing different types of exceptions
        # 2 psycop errors and 3 op errors
        # this simulates roughly what happens when database is not ready
        # on 6th time it will go to True - he used psycop2Error
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
