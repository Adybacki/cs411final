import hashlib
import logging
import os
import sqlite3
from dataclasses import dataclass
from typing import Any

from meal_max.utils.sql_utils import get_db_connection
from meal_max.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

@dataclass
class User:
    id: int
    username: str
    salt: str
    password: str

    @staticmethod
    def generate_salted_hash(password: str) -> tuple[str, str]:
        """
        Generates a salted hash for the given password.

        Args:
            password (str): The password to hash.

        Returns:
            tuple[str, str]: A tuple containing the salt and hashed password.
        """
        salt = os.urandom(16).hex()
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return salt, hashed_password

    @staticmethod
    def verify_password(stored_password: str, salt: str, password: str) -> bool:
        """
        Verifies a given password against the stored hash and salt.

        Args:
            stored_password (str): The hashed password stored in the database.
            salt (str): The salt stored in the database.
            password (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed_password == stored_password

def create_account(username: str, password: str) -> None:
    """
    Creates a new user account in the user table.

    Args:
        username (str): The username for the new account.
        password (str): The password for the new account.

    Raises:
        ValueError: If the password is less than 8 characters long.
        ValueError: If the username already exists in the database.
        sqlite3.Error: If there is an error with the database connection or query.
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    salt, hashed_password = User.generate_salted_hash(password)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, salt, password)
                VALUES (?, ?, ?)
                """,
                (username, salt, hashed_password),
            )
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
    Updates the password for a user account.

    Args:
        username (str): The username for the account.
        password (str): The new password for the account.

    Raises:
        ValueError: If the password is less than 8 characters long.
        ValueError: If the username does not exist in the database.
        sqlite3.Error: If there is an error with the database connection or query.
    """
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    salt, hashed_password = User.generate_salted_hash(password)

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE users
                SET salt = ?, password = ?
                WHERE username = ?
                """,
                (salt, hashed_password, username),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"User '{username}' does not exist")
            conn.commit()
            logger.info("Password successfully updated for account: %s", username)

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e

def login(username: str, password: str) -> bool:
    """
    Validates a user's login credentials.

    Args:
        username (str): The username for the account.
        password (str): The password for the account.

    Returns:
        bool: True if the credentials are valid, False otherwise.

    Raises:
        ValueError: If the username does not exist.
        sqlite3.Error: If there is an error with the database connection or query.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT salt, password
                FROM users
                WHERE username = ?
                """,
                (username,),
            )
            row = cursor.fetchone()

            if row is None:
                logger.info("User %s not found", username)
                raise ValueError(f"User '{username}' not found")

            salt, stored_password = row
            if User.verify_password(stored_password, salt, password):
                logger.info("Login successful for user: %s", username)
                return True
            else:
                logger.info("Invalid password for user: %s", username)
                return False

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e
