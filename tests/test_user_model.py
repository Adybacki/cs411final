from contextlib import contextmanager
import re
import sqlite3

import pytest

from meal_max.models.user_model import User, create_account, update_password, login


######################################################
#
#    Fixtures
#
######################################################

def normalize_whitespace(sql_query: str) -> str:
    return re.sub(r'\s+', ' ', sql_query).strip()

# Mocking the database connection for tests
@pytest.fixture
def mock_cursor(mocker):
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()

    # Mock the connection's cursor
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None  # Default return for queries
    mock_cursor.fetchall.return_value = []
    mock_cursor.commit.return_value = None

    # Mock the get_db_connection context manager from sql_utils
    @contextmanager
    def mock_get_db_connection():
        yield mock_conn  # Yield the mocked connection object

    mocker.patch("meal_max.models.kitchen_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

######################################################
#
#    Add and delete
#
######################################################

def test_create_account(mock_cursor):
    # Call the function
    create_account("test_user", "password123")

    expected_query = normalize_whitespace(
        """
        INSERT INTO users (username, salt, password)
        VALUES (?, ?, ?)
        """
    )

    # Check that the cursor executed the query with the correct arguments
    
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query, "The SQL query did not match the expected structure."
   
    # Extract the arguments used in the SQL call (second element of call_args)
    actual_arguments = mock_cursor.execute.call_args[0][1]

    # Check that the arguments match the expected values
    expected_arguments = ("test_user", mocker.ANY, mocker.ANY) # We don't know the exact values for salt and password
    assert actual_arguments == expected_arguments, "The SQL arguments did not match the expected values."


def test_update_password(mock_cursor):
    # Call the function
    update_password("test_user", "new_password123")

    expected_query = normalize_whitespace(
        """
        UPDATE users
        SET salt = ?, password = ?
        WHERE username = ?
        """
    )

    # Check that the cursor executed the query with the correct arguments
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Extract the arguments used in the SQL call (second element of call_args)
    actual_arguments = mock_cursor.execute.call_args[0][1]

    # Check that the arguments match the expected values
    expected_arguments = (mocker.ANY, mocker.ANY, "test_user") # We don't know the exact values for salt and password
    assert actual_arguments == expected_arguments, "The SQL arguments did not match the expected values."

def test_login(mock_cursor):
    # mock an entry into the database
    mock_cursor.fetchone.return_value = ("test_user", "salt", "password123")

    # Call the function
    result = login("test_user", "password123")

    # Check that the function returned True
    assert result == True, "The login function did not return True as expected."

    # Check that the cursor executed the query with the correct arguments
    expected_query = normalize_whitespace(
        """
        SELECT username, salt, password
        FROM users
        WHERE username = ?
        """
    )

    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Extract the arguments used in the SQL call (second element of call_args)
    actual_arguments = mock_cursor.execute.call_args[0][1]

    # Check that the arguments match the expected values
    expected_arguments = ("test_user",) # We know the username
    assert actual_arguments == expected_arguments, "The SQL arguments did not match the expected values."

#Create account with duplicate usernames 
def test_create_account_duplicate_user(mock_cursor):
    # Simulate that a user with the same username already exists
    mock_cursor.fetchone.return_value = ("test_user",)

    # Expect that an IntegrityError (or custom exception) is raised
    with pytest.raises(Exception) as excinfo:
        create_account("test_user", "password123")
    
    # Assert the exception contains the relevant message
    assert "already exists" in str(excinfo.value), "Expected an exception for duplicate username."

#Updated password for non-existent users 
def test_update_password_nonexistent_user(mock_cursor):
    # Simulate no rows affected by the update
    mock_cursor.rowcount = 0

    with pytest.raises(Exception) as excinfo:
        update_password("nonexistent_user", "new_password123")
    
    assert "User not found" in str(excinfo.value), "Expected an exception for non-existent user."

#Login with invalid password 
def test_login_invalid_password(mock_cursor):
    # Mock a valid user entry in the database
    mock_cursor.fetchone.return_value = ("test_user", "salt", "hashed_password")

    # Call the function with an incorrect password
    result = login("test_user", "wrong_password")

    # Check that the function returns False
    assert result == False, "Expected login to fail for invalid password."

#Login for nonexitent users 
def test_login_nonexistent_user(mock_cursor):
    # Simulate no user found in the database
    mock_cursor.fetchone.return_value = None

    # Call the function
    result = login("nonexistent_user", "password123")

    # Check that the function returns False
    assert result == False, "Expected login to fail for non-existent user."

#Database errors are handled gracefully // When database is unavilable or queries fail 
def test_create_account_database_error(mock_cursor):
    # Simulate a database error
    mock_cursor.execute.side_effect = sqlite3.DatabaseError("Database error")

    with pytest.raises(Exception) as excinfo:
        create_account("test_user", "password123")
    
    assert "Database error" in str(excinfo.value), "Expected a database error to be raised."

