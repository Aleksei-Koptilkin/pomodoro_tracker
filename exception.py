class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "Password is incorrect"


class TokenExpiredException(Exception):
    detail = "Token is expired"


class TokenNotCorrectException(Exception):
    detail = "Token is not correct"


class TaskNotFoundException(Exception):
    detail = "Task not found"


class NoTasksThisCategoryException(Exception):
    detail = "No tasks in this category"