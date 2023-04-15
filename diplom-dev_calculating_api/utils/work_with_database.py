# from utils.config import mydb, method
# # from work_with_firebase import add_user_to_firebase, send_email_verification_by_email_and_password
# from utils.encoding import password_encoding, check_password

# def check_username(username: str) -> bool:
#     """ Check username in database.
#     Args:
#         username (str): Username of user.
#     Returns: bool.
#     """
#     if len(list(mydb.users.find({"username": username}))) == 0:
#         return False
#     else:
#         return True


# def check_email(email: str) -> bool:
#     """ Check email in database.
#     Args:
#         email (str): email of user.
 
#     Returns: bool.
#     """
#     if len(list(mydb.users.find({"email": email}))) == 0:
#         return False
#     else:
#         return True

# def check_user_password(username: str, password: str, method: str = method) -> bool:
#     """ Check username password.
#     Args:
#         username (str): Username of user.
#         password: (str): Password.
#     Returns: bool.
#     """
#     encoded_password = get_password_from_database(username)
#     return check_password(password, encoded_password, method)

# def create_user(username: str, password: str, email: str, method:str = method) -> str:
#     """ Add user to database. Create user folder on google drive.
#     Args:
#         username (str): Username of user.
#         password (str): Password of user.
#         email (str): email of user.
#         method (str): Encryption method.
#     """
#     #pattern for check pwsd '^(?=.*[A-Z].*[A-Z])(?=.*[!@#$&*])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{8,}$'

#     encoded_password = password_encoding(password, method)
#     mydb.users.insert_one({
#         "username": username,
#         "password": encoded_password,
#         "email": email,
#     })
    
# def get_password_from_database(username: str) -> str:
#     """ Get username password from database
#     Args:
#         username (str): Username of user.
#     Returns:
#         str: encoded password.
#     """
#     return list(mydb.users.find({"username": username}))[0]['password']
