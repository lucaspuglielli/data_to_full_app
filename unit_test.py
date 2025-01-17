import unittest
from unittest.mock import patch, MagicMock
from helper import user_auth
from cryptography.fernet import Fernet
from sqlalchemy import create_engine
import random
import pandas as pd
import os


# Generate a valid Fernet key
fernet_key = Fernet.generate_key().decode()


class TestUserAuth(unittest.TestCase):

    def setUp(self):
        # Patch and initialize the mocked Redis instance
        self.mock_redis_patcher = patch('helper.get_redis')
        self.mock_redis = self.mock_redis_patcher.start()
        self.mock_redis_instance = self.mock_redis.return_value
        self.mock_redis_instance.reset_mock()  # Reset any previous state

    def tearDown(self):
        # Stop the patcher after each test
        self.mock_redis_patcher.stop()

    @patch('builtins.input', side_effect=["test_user", "wrong_password", "n"])
    @patch('os.getenv', side_effect=lambda k: {
        'FERNET_KEY': fernet_key,
        'SIGN_UP_PASSWORD': 'invitation',
        'POSTGRES_USER': 'username',
        'POSTGRES_PASSWORD': 'password',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_AUTH_DB': 'auth_db'
    }.get(k))
    def test_auth_failure(self, mock_input, mock_getenv):
        self.mock_redis_instance.get.side_effect = [b"wrong_password"]

        mock_table_df = pd.DataFrame({'table_name': ['users']})
        with patch('pandas.read_sql', return_value=mock_table_df):
            result = user_auth()

            self.mock_redis_instance.set('datamaster_user_username', '')
            self.mock_redis_instance.set('datamaster_user_password', '')
            self.assertFalse(result, "Expected authentication to fail with incorrect password")

    @patch('helper.get_redis')
    @patch('builtins.input', side_effect=[
        "test_user", "correct_password",  # Inputs for login
        "y", "datamaster1", "test_user", "correct_password",  # Inputs for sign-up
        "y", "datamaster1", "new_username", "new_password",  # Additional inputs to satisfy all prompts
    ])
    @patch('os.getenv', side_effect=lambda k: {
        'FERNET_KEY': fernet_key,
        'SIGN_UP_PASSWORD': 'datamaster1',
        'POSTGRES_USER': 'username',  # Ensure this matches the expected value
        'POSTGRES_PASSWORD': 'password',  # Ensure this matches the expected value
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_AUTH_DB': 'auth_db'
    }.get(k))
    @patch('sqlalchemy.create_engine')  # Mock SQLAlchemy engine creation
    def test_user_registry(self, mock_create_engine, mock_getenv, mock_input, mock_get_redis):
        # Mock Redis instance
        mock_redis_instance = mock_get_redis.return_value
        mock_redis_instance.get.side_effect = [
            None,  # Simulate no existing Redis keys
            'mocked_password'.encode()  # Simulate encoded password from Redis
        ]
        mock_redis_instance.set.return_value = None  # Simulate Redis set
    
        # Mock SQLAlchemy engine and connection
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value = mock_connection
        mock_connection.execute.return_value = None  # Simulate SQL execution
    
        # Mock psycopg2 connection
        with patch('psycopg2.connect') as mock_psycopg2_connect:
            mock_psycopg2_connect.return_value = mock_connection
            mock_connection.cursor.return_value = MagicMock()
    
            # Mock pandas.read_sql responses
            mock_read_sql_side_effect = [
                pd.DataFrame({'table_name': ['users']}),  # Mock for table existence check
                pd.DataFrame(columns=['USERNAME', 'PASSWORD']),  # Mock for user query
            ]
            with patch('pandas.read_sql', side_effect=mock_read_sql_side_effect):
                # Call the function under test
                result = user_auth()
    
        # Assertions
        mock_redis_instance.set.assert_called_with('datamaster_user_password', '')
        self.assertTrue(result, "Expected authentication to succeed with correct password or after signing up")





    @patch('builtins.input', side_effect=["test_user", "correct_password"])
    @patch('os.getenv', side_effect=lambda k: {
        'FERNET_KEY': fernet_key,
        'SIGN_UP_PASSWORD': 'invitation',
        'POSTGRES_USER': 'username',
        'POSTGRES_PASSWORD': 'password',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_AUTH_DB': 'auth_db'
    }.get(k))
    def test_auth_success(self, mock_input, mock_getenv):
        self.mock_redis_instance.get.side_effect = [b"correct_password"]

        cipher_suite = Fernet(fernet_key.encode())
        encrypted_password = cipher_suite.encrypt(b"correct_password").decode()

        mock_table_df = pd.DataFrame({'table_name': ['users']})
        mock_user_df = pd.DataFrame({'USERNAME': ['test_user'], 'PASSWORD': [encrypted_password]})

        with patch('pandas.read_sql', side_effect=[mock_table_df, mock_user_df]):
            result = user_auth()

            self.mock_redis_instance.set('datamaster_user_username', '')
            self.mock_redis_instance.set('datamaster_user_password', '')
            self.assertTrue(result, "Expected authentication to succeed with correct password")

    @patch('builtins.input', side_effect=[str(random.getrandbits(25)), "any_password", "n"])
    @patch('os.getenv', side_effect=lambda k: {
        'FERNET_KEY': fernet_key,
        'SIGN_UP_PASSWORD': 'invitation',
        'POSTGRES_USER': 'username',
        'POSTGRES_PASSWORD': 'password',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_AUTH_DB': 'auth_db'
    }.get(k))
    def test_auth_new_user(self, mock_input, mock_getenv):
        self.mock_redis_instance.get.side_effect = [None]

        mock_table_df = pd.DataFrame({'table_name': ['users']})
        with patch('pandas.read_sql', return_value=mock_table_df):
            result = user_auth()

            self.mock_redis_instance.set('datamaster_user_username', '')
            self.mock_redis_instance.set('datamaster_user_password', '')
            self.assertFalse(result, "Expected authentication to fail for new users that don't want to register")


if __name__ == "__main__":
    unittest.main()
