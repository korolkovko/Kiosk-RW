# password.py
# Password hashing and verification utilities

import bcrypt
from typing import Optional


class PasswordManager:
    """Handles password hashing and verification using bcrypt"""

    def __init__(self):
        # Bcrypt rounds for hashing (12 = strong security)
        self.rounds = 12

    def hash_password(self, password: str) -> str:
        """
        Hash a plain text password using bcrypt

        Args:
            password: Plain text password to hash

        Returns:
            Hashed password string

        Raises:
            ValueError: If password exceeds bcrypt's 72-byte limit
        """
        # Bcrypt has a 72-byte limit, check password length
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            raise ValueError(
                f"Password is {len(password_bytes)} bytes (limit: 72 bytes). Password cannot be longer than 72 bytes."
            )

        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=self.rounds)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain text password against a hashed password

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against

        Returns:
            True if password matches, False otherwise
        """
        if not hashed_password:
            return False

        try:
            password_bytes = plain_password.encode('utf-8')
            hashed_bytes = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hashed_bytes)
        except Exception:
            return False

    def needs_update(self, hashed_password: str) -> bool:
        """
        Check if a hashed password needs to be rehashed

        Args:
            hashed_password: Hashed password to check

        Returns:
            Always returns False for bcrypt (no automatic updates needed)
        """
        # bcrypt doesn't have an automatic needs_update mechanism
        # This method is kept for compatibility
        return False


# Global password manager instance
password_manager = PasswordManager()