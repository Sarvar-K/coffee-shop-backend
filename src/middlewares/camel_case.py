from json import JSONDecodeError

from fastapi import Request, Response
from typing import Any, Callable
import json
from urllib.parse import urlencode
import humps
from starlette.middleware.base import BaseHTTPMiddleware


def transform_keys(obj: Any, transform: Callable[[str], str]) -> Any:
    if isinstance(obj, dict):
        return {transform(k): transform_keys(v, transform) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [transform_keys(item, transform) for item in obj]
    else:
        return obj


class CamelCaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if request.method in ("POST", "PUT", "PATCH"):
            # Transform request body to snake_case
            await _request_body_to_snake_case(request)

        # Transform query parameters to snake_case
        query_params = request.query_params
        transformed_query_params = {
            humps.decamelize(key): value for key, value in query_params.items()
        }
        request.scope["query_string"] = urlencode(transformed_query_params).encode()

        response: Response = await call_next(request)
        response_headers = response.headers

        if response_headers.get("content-type") == "application/json":
            # Transform response body to camelCase
            response_body = await _get_response_json(response)

            transformed_body = transform_keys(response_body, humps.camelize)
            transformed_body_bytes = json.dumps(transformed_body).encode("utf-8")

            response_headers['content-length'] = str(len(transformed_body_bytes))

            response = Response(
                content=transformed_body_bytes,
                status_code=response.status_code,
                headers=response_headers,
                media_type="application/json"
            )

        return response


async def _get_response_json(response: Response):
    response_body = b""

    async for chunk in response.body_iterator:
        response_body += chunk

    return json.loads(response_body)


async def _request_body_to_snake_case(request: Request):
    body = await request.body()
    if not body:
        return None

    try:
        body_json = json.loads(body)
    except JSONDecodeError as e:
        return None

    transformed_body = transform_keys(body_json, humps.decamelize)
    request._body = json.dumps(transformed_body).encode("utf-8")
