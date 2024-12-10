import hashlib
import logging
import os

from typing import Any
from sqlalchemy.exc import IntegrityError
from meal_max.db import db

from meal_max.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    salt = db.Column(db.String(32), nullable=False)  # 16-byte salt in hex
    password = db.Column(db.String(64), nullable=False)  # SHA-256 hash in hex
    location_name = db.Column(db.String(80), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    @classmethod
    def _generate_salted_hash(cls, password: str) -> tuple[str, str]:
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

    @classmethod
    def check_password(cls, username: str, password: str) -> bool:
        """
        Check if a given password matches the stored password for a user.

        Args:
            username (str): The username of the user.
            password (str): The password to check.

        Returns:
            bool: True if the password is correct, False otherwise.

        Raises:
            ValueError: If the user does not exist.
        """
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")
        hashed_password = hashlib.sha256((password + user.salt).encode()).hexdigest()
        return hashed_password == user.password
    
    @classmethod
    def create_account(cls, username: str, password: str) -> None:
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
            logger.error("Password must be at least 8 characters long")
            raise ValueError("Password must be at least 8 characters long")
        salt, hashed_password = cls._generate_salted_hash(password)
        new_user = cls(username=username, salt=salt, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            logger.info("User successfully added to the database: %s", username)
        except IntegrityError:
            db.session.rollback()
            logger.error("Duplicate username: %s", username)
            raise ValueError(f"User with username '{username}' already exists")
        except Exception as e:
            db.session.rollback()
            logger.error("Database error: %s", str(e))
            raise e
    
    @classmethod
    def update_password(cls, username: str, new_password: str) -> None:
        """
        Updates the password for a user account.

        Args:
            username (str): The username for the account.
            new_password (str): The new password for the account.

        Raises:
            ValueError: If the username is not found in the database.
            sqlite3.Error: If there is an error with the database connection or query.
        """
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")

        salt, hashed_password = cls._generate_salted_hash(new_password)
        user.salt = salt
        user.password = hashed_password
        db.session.commit()
        logger.info("Password updated successfully for user: %s", username)
        
    @classmethod
    def login(cls, username: str, password: str) -> bool:
        """
        Validates a user's login credentials.

        Args:
            username (str): The username for the account.
            password (str): The password for the account.
        
        Returns:
            bool: True if the login is successful, False otherwise.

        Raises:
            ValueError: If the username is not found in the database.
            sqlite3.Error: If there is an error with the database connection or query.
        """
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("User %s not found", username)
            raise ValueError(f"User {username} not found")
        hashed_password = hashlib.sha256((password + user.salt).encode()).hexdigest()
        return hashed_password == user.password

    @classmethod
    def set_favorite(cls, username: str, city_name:str, lat:float, lon:float) -> None:
        """
        Sets a favorite city for a user.

        Args:
            username (str): The username of the user.
            city_name (str): The name of the city.
            lat (float): The latitude of the city.
            lon (float): The longitude of the city.

        Raises:
            ValueError: If the username is not found in the database.
            sqlite3.Error: If there is an error with the database connection or query.
        """
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("Username %s not found", username)
            raise ValueError(f"Username {username} not found")
        user.location_name = city_name
        user.latitude = lat
        user.longitude = lon
        db.session.commit()
        logger.info("Favorite city set for user %s: %s", username, city_name)

    @classmethod
    def get_favorite(cls, username:str) -> Any: 
        """
        Gets the favorite city for a user.

        Args:
            username (str): The ID of the user.

        Returns:
            Any: A tuple containing the city name, latitude, and longitude.

        Raises:
            ValueError: If the username is not found in the database.
            sqlite3.Error: If there is an error with the database connection or query.
        """
        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.info("Username %s not found", username)
            raise ValueError(f"Username {username} not found")
        return user.location_name, user.latitude, user.longitude
    