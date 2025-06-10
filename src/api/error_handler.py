from typing import Sequence, Any

import humps
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from exceptions import RequestError
from utils import is_regular_iterable


async def request_exception_handler(request: Request, exc: RequestError):
    return JSONResponse(
        status_code=exc.status_code,
        content=dict(
            message=exc.message,
            details=[],
        ),
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    return JSONResponse(
        status_code=400,
        content=dict(
            message='Field value errors',
            details=_construct_validation_error_details(errors)
        ),
    )


def _construct_validation_error_details(request_validation_errors: Sequence[Any]):
    return [_convert_fastapi_validation_error_obj(fastapi_field_error_obj) for fastapi_field_error_obj in request_validation_errors]


def _convert_fastapi_validation_error_obj(fastapi_field_error_obj: Any):
    default_result = dict(
        name='fieldUnrelatedErrors',
        errors=[str(fastapi_field_error_obj)]
    )

    if not isinstance(fastapi_field_error_obj, dict):
        return default_result

    loc = fastapi_field_error_obj.get('loc')
    msg = fastapi_field_error_obj.get('msg')

    if not loc or not msg:
        return default_result

    field_names = [humps.camelize(field_name) for field_name in loc[1:]]
    if len(field_names) == 1:
        field_names = field_names[0]

    if is_regular_iterable(msg):
        msgs = [str(message) for message in msg]
    else:
        msgs = [str(msg)]

    return dict(
        name=field_names,
        errors=msgs,
    )
