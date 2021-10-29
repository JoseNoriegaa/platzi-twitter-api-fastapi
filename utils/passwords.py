import bcrypt



def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def check_password(password, hashed):
    """
    Checks if a password matches a hashed password.

    Args:
        password (str): The password to check.
        hashed (str): The hashed password.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
