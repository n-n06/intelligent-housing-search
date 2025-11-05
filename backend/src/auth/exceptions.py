from fastapi import HTTPException, status

class InvalidRegistrationError(HTTPException):
    def __init__(self, loc, msg, err_type="value_error"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{
                "loc": loc,
                "msg": msg,
                "type": err_type
            }]
        )
