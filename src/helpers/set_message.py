from fastapi import Response, status

def _translate_code(code: int):
    if code == 200:
        return status.HTTP_200_OK
    elif code == 201:
        return status.HTTP_201_CREATED
    elif code == 400:
        return status.HTTP_400_BAD_REQUEST
    elif code == 401:
        return status.HTTP_401_UNAUTHORIZED
    elif code == 404:
        return status.HTTP_404_NOT_FOUND
    elif code == 500:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    

def set_message(
    message:str,
    code:int = 200,
    data:dict = None,
    error:dict = None
) -> dict:
    response = {
        "message": message,
        "code": code,
    }

    if data is not None:
        response["data"] = data

    if error is not None:
        response["error"] = error

    # throw response
    Response.status_code = _translate_code(code)
    return response