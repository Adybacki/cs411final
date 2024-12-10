from contextlib import contextmanager
import re
import sqlite3

import pytest
from sqlalchemy.exc import IntegrityError
from meal_max.models.user_model import User


######################################################
#
#    Fixtures
#
######################################################

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

def test_create_account(session, sample_user):
    # Call the function
    """Test creating a new user with a unique username."""
    User.create_account(**sample_user)
    user = session.query(User).filter_by(username=sample_user["username"]).first()

    assert user is not None, "User should be created in the database."
    assert user.username == sample_user["username"], "Username should match the input."
    assert len(user.salt) == 32, "Salt should be 32 characters (hex)."
    assert len(user.password) == 64, "Password should be a 64-character SHA-256 hash."

#Create account with duplicate usernames 
def test_create_account_duplicate_user(session, sample_user):

    """Test attempting to create a user with a duplicate username."""
    User.create_account(**sample_user)
    with pytest.raises(ValueError, match="User with username 'test_user' already exists"):
        User.create_account(**sample_user)

def test_create_account_short_password(session):

    """Test creating a user with a password that is too short."""
    with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
        User.create_account("test_user", "short")

###################
# Update Password #
###################

def test_update_password(session, sample_user):
    """Test updating the password for an existing user."""
    User.create_account(**sample_user)
    new_password = "newpassword456"
    User.update_password(sample_user["username"], new_password)
    assert User.verify_password(sample_user["username"], new_password, new_password) is True, "Password should be updated successfully."
    

#Updated password for non-existent users 
def test_update_password_nonexistent_user(mock_cursor):
    # Simulate no rows affected by the update
    mock_cursor.rowcount = 0

    with pytest.raises(Exception) as excinfo:
        User.update_password("nonexistent_user", "new_password123")
    
    assert "User not found" in str(excinfo.value), "Expected an exception for non-existent user."

###################
# Login Function #
###################

def test_login(mock_cursor, sample_user):


    #create a user in the database
    User.create_account(**sample_user)

    # Mock a valid user entry in the database
    actual_arguments = mock_cursor.execute.call_args[0][1]

    # Call the function
    result = User.login(sample_user["username"], sample_user["password"])

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
    result = User.login("test_user", "wrong_password")

    # Check that the function returns False
    assert result == False, "Expected login to fail for invalid password."

#Login for nonexitent users 
def test_login_nonexistent_user(mock_cursor):
    # Simulate no user found in the database
    mock_cursor.fetchone.return_value = None

    # Call the function
    result = User.login("nonexistent_user", "password123")

    # Check that the function returns False
    assert result == False, "Expected login to fail for non-existent user."

