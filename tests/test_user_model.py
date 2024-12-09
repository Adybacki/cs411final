from contextlib import contextmanager
import re
import sqlite3

import pytest
from pytest_mock import mocker
from meal_max.utils.sql_utils import get_db_connection

from meal_max.models.user_model import (User, create_account, update_password, login)


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

    mocker.patch("meal_max.models.user_model.get_db_connection", mock_get_db_connection)

    return mock_cursor  # Return the mock cursor so we can set expectations per test

@pytest.fixture
def sample_user():
    return {
        "username": "test_user",
        "password": "password123"
    }
######################################################
#
#    Create_account
#
######################################################

def test_create_account(mock_cursor, sample_user):
    # Call the function
    create_account(**sample_user)

    expected_query = normalize_whitespace(
        """
        INSERT INTO users (username, salt, pword)
        VALUES (?, ?, ?)
        """
    )

    # Check that the cursor executed the query with the correct arguments
    
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    actual_arguments = mock_cursor.execute.call_args[0][1]

    username = sample_user["username"]

    # Check that the user was added to the database
    assert actual_arguments[0] == username, "The user was not added to the database."

    # Check that the salt and password are the correct lengths
    assert len(actual_arguments[1]) == 32, "Salt should be 32 characters (hex)."
    assert len(actual_arguments[2]) == 64, "Password should be a 64-character SHA-256 hash."

#Create account with duplicate usernames 
def test_create_account_duplicate_user(mock_cursor, sample_user):

    mock_cursor.execute.side_effect = sqlite3.IntegrityError("UNIQUE constraint failed: users.username")
    # Expect that an IntegrityError (or custom exception) is raised
    with pytest.raises(ValueError, match="Username 'test_user' already exists") as excinfo:
        create_account(**sample_user)
    
    # Assert the exception contains the relevant message
    assert "already exists" in str(excinfo.value), "Expected an exception for duplicate username."

def test_create_account_short_password():

    with pytest.raises(ValueError, match="Password must be at least 8 characters long") as excinfo:
        create_account("test_user", "short")
    
    # Expect that a ValueError (or custom exception) is raised
    assert "Password must be at least 8 characters long" in str(excinfo.value), "Expected an exception for short password."

#Database errors are handled gracefully // When database is unavilable or queries fail 
def test_create_account_database_error(mock_cursor):
    # Simulate a database error
    mock_cursor.execute.side_effect = sqlite3.DatabaseError("Database error")

    with pytest.raises(sqlite3.DatabaseError) as excinfo:
        create_account("test_user", "password123")

    assert "Database error" in str(excinfo.value), "Expected an exception for database error."

###################
# Update Password #
###################

def test_update_password(mock_cursor, sample_user):

    #mock a user in the database with the password "password123"
    create_account(**sample_user)

    new_password = "new_password123"
    # Call the function
    update_password(sample_user["username"], new_password)


    expected_query = normalize_whitespace(
        """
        UPDATE users
        SET salt = ?, pword = ?
        WHERE username = ?
        """
    )

    # Check that the cursor executed the query with the correct arguments
    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query, "The SQL query did not match the expected structure."
    
    #Check that the password was updated successfully
    assert login(sample_user["username"], new_password), "The password was not updated successfully."
    

#Updated password for non-existent users 
def test_update_password_nonexistent_user(mock_cursor):
    # Simulate no rows affected by the update
    mock_cursor.rowcount = 0

    with pytest.raises(Exception) as excinfo:
        update_password("nonexistent_user", "new_password123")
    
    assert "User not found" in str(excinfo.value), "Expected an exception for non-existent user."

###################
# Login Function #
###################

def test_login(mock_cursor, sample_user):


    #create a user in the database
    create_account(**sample_user)

    # Mock a valid user entry in the database
    actual_arguments = mock_cursor.execute.call_args[0][1]

    # Call the function
    result = login(sample_user["username"], sample_user["password"])

    # Check that the function returned True
    assert result == True, "The login function did not return True as expected."

    # Check that the cursor executed the query with the correct arguments
    expected_query = normalize_whitespace(
        """
        SELECT username, salt, pword
        FROM users
        WHERE username = ?
        """
    )

    actual_query = normalize_whitespace(mock_cursor.execute.call_args[0][0])
    assert actual_query == expected_query, "The SQL query did not match the expected structure."

    # Extract the arguments used in the SQL call (second element of call_args)
    actual_arguments = mock_cursor.execute.call_args[0][1]

    # Check that the arguments match the expected values
    expected_arguments = (sample_user["username"],) # We know the username
    assert actual_arguments == expected_arguments, "The SQL arguments did not match the expected values."

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

