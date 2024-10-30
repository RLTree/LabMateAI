# test_labmateai_db.py

import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from labmateai.labmateai_db import get_engine

class TestLabmateaiDB(unittest.TestCase):
    def setUp(self):
        self.db_config = {
            'user': 'test_user',
            'password': 'test_password',
            'host': 'localhost',
            'port': '5432',
            'dbname': 'test_db'
        }

    @patch('labmateai.labmateai_db.create_engine')
    def test_get_engine_success(self, mock_create_engine):
        """Test that get_engine creates an engine with the correct URL."""
        # Mock the engine
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        # Call get_engine
        engine = get_engine(self.db_config)

        # Assert create_engine was called with the correct URL
        expected_url = 'postgresql://test_user:test_password@localhost:5432/test_db'
        mock_create_engine.assert_called_once_with(expected_url)

        # Assert the returned engine is the mock_engine
        self.assertEqual(engine, mock_engine)

    @patch('labmateai.labmateai_db.create_engine')
    def test_get_engine_failure(self, mock_create_engine):
        """Test that get_engine handles exceptions correctly."""
        # Simulate an exception when create_engine is called
        mock_create_engine.side_effect = SQLAlchemyError("Failed to create engine")

        # Call get_engine and expect SystemExit
        with self.assertRaises(SystemExit) as cm:
            get_engine(self.db_config)

        # Assert that the exit code is 1
        self.assertEqual(cm.exception.code, 1)

        # Assert create_engine was called once
        mock_create_engine.assert_called_once()

    def test_get_engine_invalid_config(self):
        """Test that get_engine exits when db_config is missing keys."""
        # Remove 'user' from db_config
        invalid_config = self.db_config.copy()
        del invalid_config['user']

        # Call get_engine and expect SystemExit
        with self.assertRaises(SystemExit) as cm:
            get_engine(invalid_config)

        # Assert that the exit code is 1
        self.assertEqual(cm.exception.code, 1)

    @patch('labmateai.labmateai_db.create_engine')
    def test_get_engine_testing(self, mock_create_engine):
        """Test that get_engine returns SQLite engine when testing is True."""
        # Set the testing flag to True
        testing = True

        # Mock the engine
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        # Call get_engine with testing=True
        engine = get_engine(self.db_config, testing=testing)

        # Assert create_engine was called with SQLite URL
        mock_create_engine.assert_called_once_with('sqlite:///:memory:')

        # Assert the returned engine is the mock_engine
        self.assertEqual(engine, mock_engine)

    @patch('labmateai.labmateai_db.create_engine')
    def test_get_engine_no_config(self, mock_create_engine):
        """Test that get_engine exits when db_config is None."""
        # Call get_engine with db_config=None
        with self.assertRaises(SystemExit) as cm:
            get_engine(None)

        # Assert that the exit code is 1
        self.assertEqual(cm.exception.code, 1)

        # Assert create_engine was not called
        mock_create_engine.assert_not_called()

if __name__ == '__main__':
    unittest.main()