from dataclasses import dataclass
import logging
import sqlite3
from typing import Any
import bcrypt

from meal_max.utils.sql_utils import get_db_connection
from meal_max.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


@dataclass
class User:
    id: int
    username: str
    password: str

    def __post_init__(self):
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        self.password = bcrypt.hash_password(self.password)

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')


def create_account(username: str, password: str) -> None:
    """
    Creates a new user account in the user table

    Args:
        username (str): The username for the new account
        password (str): The password for the new account
    
    Raises:
        ValueError: If the password is less than 8 characters long
        ValueError: If the username already exists in the database
        sqlite3.Error: If there is an error with the database connection or query
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    hashed_password = User.hash_password(password)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (?, ?)
            """, (username, hashed_password))
            conn.commit()

            logger.info("Account successfully created: %s", username)

    except sqlite3.IntegrityError:
        logger.error("Duplicate username: %s", username)
        raise ValueError(f"Username '{username}' already exists")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e
    
def update_password(username: str, password: str) -> None:
    """
    Updates the password for a user account

    Args:
        username (str): The username for the account
        password (str): The new password for the account
    
    Raises:
        ValueError: If the password is less than 8 characters long
        ValueError: If the username does not exist in the database
        sqlite3.Error: If there is an error with the database connection or query
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    hashed_password = User.hash_password(password)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users
                SET password = ?
                WHERE username = ?
            """, (hashed_password, username))
            conn.commit()

            logger.info("Password successfully updated for account: %s", username)

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e
    
def login(username: str, password: str) -> bool:
    """
    Validates a user's login credentials

    Args:
        username (str): The username for the account
        password (str): The password for the account
    
    Returns:
        bool: True if the credentials are valid, False otherwise
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result:
                hashed_password = result[0]
                return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
            else:
                return False

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e