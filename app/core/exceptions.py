# from fastapi import HTTPException
# from starlette.requests import Request
# from starlette.responses import JSONResponse
# from typing import List, Optional, Union

# class APIException(HTTPException):
#     def __init__(
#         self,
#         field: Optional[Union[str, List[str]]],  # Support multiple fields
#         message: str,
#         status_code: int = 400,
#         error_type: str = "validation_error",
#         input_value: Optional[Union[str, int, float, None]] = None,  # Store actual input if available
#         location: str = "body",  # Default to body, but allow other locations
#     ):
#         if isinstance(field, list):  # Handle multiple error locations
#             loc = [location] + field
#         else:
#             loc = [location, field] if field else [location]

#         super().__init__(
#             status_code=status_code,
#             detail=[{
#                 "type": error_type,
#                 "loc": loc,
#                 "msg": message,
#                 "input": input_value
#             }]
#         )

# async def api_exception_handler(request: Request, exc: APIException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"errors": exc.detail}  # Use "errors" to support multiple issues
#     )
