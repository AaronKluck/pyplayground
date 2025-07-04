class NotFoundError(Exception):
    """Raised when a resource is not found"""

    pass


class ConflictError(Exception):
    """Raised when a unique constraint would be violated"""

    pass


class ValidationError(Exception):
    """Raised when input validation fails"""

    pass
