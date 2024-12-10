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

##################
# Check Password #
##################

def test_check_password_correct(session, sample_user):
    """Test checking the password for an existing user."""
    User.create_account(**sample_user)
    assert User.check_password(sample_user["username"], sample_user["password"]) is True, "Password should be correct."

def test_check_password_incorrect(session, sample_user):
    """Test checking an incorrect password for an existing user."""
    User.create_account(**sample_user)
    assert User.check_password(sample_user["username"], "wrongpassword") is False, "Password should be incorrect."

###################
# Update Password #
###################

def test_update_password(session, sample_user):
    """Test updating the password for an existing user."""
    User.create_account(**sample_user)
    new_password = "newpassword456"
    User.update_password(sample_user["username"], new_password)
    assert User.check_password(sample_user["username"], new_password) is True, "Password should be updated successfully."
    

#Updated password for non-existent users 
def test_update_password_nonexistent_user(session):
    """Test updating the password for a non-existent user."""
    with pytest.raises(ValueError, match="User nonexistentuser not found"):
        User.update_password("nonexistentuser", "newpassword")

###################
# Login Function #
###################

def test_login(session, sample_user):
    """Test logging in with the correct password."""
    User.create_account(**sample_user)
    assert User.login(sample_user["username"], sample_user["password"]) is True, "Login should succeed with correct password."

def test_login_invalid_password(session):
    """Test logging in with an incorrect password."""
    User.create_account("test_user", "password123")
    assert User.login("test_user", "wrongpassword") is False, "Login should fail with incorrect password."

#Login for nonexitent users 
def test_login_nonexistent_user(session):
    """Test login for a non-existent user."""
    with pytest.raises(ValueError, match="User nonexistentuser not found"):
        User.login("nonexistentuser", "newpassword")

def test_set_favorite(session, sample_user):
    """Test setting a favorite location for a user."""
    User.create_account(**sample_user)
    User.set_favorite(sample_user["username"], "Boston", 42.3601, -71.0589)
    user = session.query(User).filter_by(username=sample_user["username"]).first()
    assert user.location_name == "Boston", "Favorite meal should be set."
    assert user.latitude == 42.3601, "Latitude should match input."
    assert user.longitude == -71.0589, "Longitude should match input."

def test_set_favorite_nonexistent_user(session):
    """Test setting a favorite location for a non-existent user."""
    with pytest.raises(ValueError, match="Username nonexistentuser not found"):
        User.set_favorite("nonexistentuser", "Boston", 42.3601, -71.0589)

def test_get_favorite(session, sample_user):
    """Test getting the favorite location for a user."""
    User.create_account(**sample_user)
    User.set_favorite(sample_user["username"], "Boston", 42.3601, -71.0589)
    favorite = User.get_favorite(sample_user["username"])
    assert favorite == ("Boston", 42.3601, -71.0589), "Favorite location should be returned."

def test_get_favorite_nonexistent_user(session):
    """Test getting the favorite location for a non-existent user."""
    with pytest.raises(ValueError, match="Username nonexistentuser not found"):
        User.get_favorite("nonexistentuser")
        