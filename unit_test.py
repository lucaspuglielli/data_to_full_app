import unittest
from unittest.mock import patch, MagicMock
from helper import user_auth
from cryptography.fernet import Fernet
import random
import pandas as pd
import base64
import os

class TestUserAuth(unittest.TestCase):

    @patch('helper.get_engine')
    @patch('helper.get_redis')
    @patch('builtins.input', side_effect=["test_user", "wrong_password", "n"])
    def test_auth_failure(self, mock_input, mock_redis, mock_engine):
        mock_redis_instance = mock_redis.return_value
        mock_redis_instance.get.side_effect = [b"wrong_password"]
        
        mock_engine_instance = MagicMock()
        mock_engine.return_value = mock_engine_instance
        
        mock_table_df = pd.DataFrame({'table_name': ['users']})
        with patch('pandas.read_sql', return_value=mock_table_df):
            result = user_auth()
            self.assertFalse(result, "Expected authentication to fail with incorrect password")


    @patch('helper.get_engine')
    @patch('helper.get_redis')
    @patch('builtins.input', side_effect=["test_user", "correct_password", "y", "datamaster1", "test_user", "correct_password"])
    def test_auth_signup(self, mock_input, mock_redis, mock_engine):
        mock_redis_instance = mock_redis.return_value
        mock_redis_instance.get.side_effect = [None, None]
        
        mock_engine_instance = MagicMock()
        mock_engine.return_value = mock_engine_instance

        mock_table_df = pd.DataFrame({'table_name': ['users']})
        mock_user_query_df = pd.DataFrame(columns=['USERNAME', 'PASSWORD'])
        
        with patch('pandas.read_sql', side_effect=[mock_table_df, mock_user_query_df]):
            result = user_auth()
            self.assertTrue(result, "Expected authentication to succeed with correct password or signing up")


    
    @patch('helper.get_engine')
    @patch('helper.get_redis')
    @patch('builtins.input', side_effect=["test_user", "correct_password"])
    def test_auth_success(self, mock_input, mock_redis, mock_engine):
        mock_redis_instance = mock_redis.return_value
        mock_redis_instance.get.side_effect = [b"correct_password"]
        
        mock_engine_instance = MagicMock()
        mock_engine.return_value = mock_engine_instance

        fernet_key = base64.urlsafe_b64encode(os.urandom(32))
        cipher_suite = Fernet(fernet_key)
        encrypted_password = cipher_suite.encrypt(b"correct_password").decode()

        mock_table_df = pd.DataFrame({'table_name': ['users']})
        mock_user_df = pd.DataFrame({'USERNAME': ['test_user'], 'PASSWORD': [encrypted_password]})

        with patch('pandas.read_sql', side_effect=[mock_table_df, mock_user_df]):
            with patch('os.getenv', side_effect=lambda k: {'FERNET_KEY': fernet_key.decode(), 'SIGN_UP_PASSWORD': 'invitation'}.get(k)):
                result = user_auth()
                self.assertTrue(result, "Expected authentication to succeed with correct password")

    
    @patch('helper.get_engine')
    @patch('helper.get_redis')
    @patch('builtins.input', side_effect=[random.getrandbits(25), "any_password", "n"])
    def test_auth_new_user(self, mock_input, mock_redis, mock_engine):
        mock_redis_instance = mock_redis.return_value
        mock_redis_instance.get.side_effect = [None]
        
        mock_engine_instance = MagicMock()
        mock_engine.return_value = mock_engine_instance

        mock_table_df = pd.DataFrame({'table_name': ['users']})
        with patch('pandas.read_sql', return_value=mock_table_df):
            result = user_auth()
            self.assertFalse(result, "Expected authentication to fail for new users that doesn't want to register")

if __name__ == "__main__":
    unittest.main()
