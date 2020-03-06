class ChallongeException(Exception):
    """The base exception class for my Challonge library.

    Should be able to catch this to handle any library-specific exceptions.
    """
    pass

class HTTPException(ChallongeException):
    """Exception whenever a request gets a response code other than 200: OK.
    """
    def __init__(self, code = None):
        super().__init__(f"Request failed with code: {code}" or "Request failed.")

class UserInputError(ChallongeException):
    """Handler for all user input related errors.

    Handles all exceptions related to user actions.
    """
    pass

class BadArgument(UserInputError):
    """Handles improper command arguments.

    This exception handles all user errors in command arguments.
    """
    def __init__(self, message = None):
        super().__init__(message or 'A bad argument was received.')
