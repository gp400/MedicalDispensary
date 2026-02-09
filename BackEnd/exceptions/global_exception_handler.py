from fastapi import HTTPException, Request
from starlette.responses import JSONResponse

async def global_exception_handler(request: Request, exc: Exception):

    if isinstance(exc, HTTPException):
        status = exc.status_code
        detail = exc.detail

    else:
        status = 400
        detail = str(exc)

    return JSONResponse(
        status_code=status,
        content={"error": detail},
    )