import re


def check_name(name: str) -> bool:
    """ Check correctness of name

    Args:
        name (str): Name of the project

    Returns:
        bool: True if name is correct, else false
    """
    en_pattern = "^[a-zA-Z0-9_.-]*$"
    ru_pattern = "^[а-яА-ЯёЁ0-9_.-]*$"
    res_en = bool(re.search(en_pattern, name))
    res_ru = bool(re.search(ru_pattern, name))
    if (not res_en and not res_ru) or len(name) < 3 or len(name) > 20:
        return False
    
    else:
        return True


def check_password(password: str) -> bool:
    """ Check is password strength or not.
        Min number of characters - 8
        Also pswd should contains at least one special symbol (!@#$&*)
        And at least one number
        And at least one upper case letter.

    Args:
        password (str): Password.

    Returns:
        bool: Is password strength of nor.
    """
    
    pattern = "^(?=.*[A-Z].*)(?=.*[!@#$&*])(?=.*[0-9].*)(?=.*[a-z].*[a-z].*[a-z]).{8,}$"
    res = bool(re.search(pattern, password))
    return res

#TODO: Add validation of email