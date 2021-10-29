from typing import Union

from schemas.user import UserOut


def get_fullname(user: Union[UserOut, dict]) -> str:
    """
    Get the full name of a user.

    Args:
        user (Union[User, dict]): The user to get the full name of.

    Returns:
        str: The full name of the user.
    """

    if isinstance(user, dict):
        return f"{user['first_name']} {user['last_name']}"

    return user.first_name + " " + user.last_name
