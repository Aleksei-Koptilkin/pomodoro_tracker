class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "Password is incorrect"


class TokenExpiredException(Exception):
    detail = "Token is expired"


class TokenNotCorrectException(Exception):
    detail = "Token is not correct"