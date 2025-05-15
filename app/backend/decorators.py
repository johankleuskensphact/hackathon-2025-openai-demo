import logging
from functools import wraps
from typing import Any, Callable, TypeVar, cast

from quart import abort, current_app, request

from config import CONFIG_AUTH_CLIENT, CONFIG_SEARCH_CLIENT
from core.authentication import AuthError
from error import error_response

# Dictionary to maintain API mappings of type str, str
customers: dict[str, list[str]] = {
    "63aba3c3-130c-43e8-b9ec-242c8c0bff84": ["puurbaarlo"],
    "1a62f099-6824-4a1e-a1ec-ab7df7aed7f1": ["melderslo"],
    "adb0eba3-4d47-4ab3-b446-eabac9bcca4d": ["phact-hrm"]
}


def authenticated_path(route_fn: Callable[[str, dict[str, Any]], Any]):
    """
    Decorator for routes that request a specific file that might require access control enforcement
    """

    @wraps(route_fn)
    async def auth_handler(path=""):
        # If authentication is enabled, validate the user can access the file
        auth_helper = current_app.config[CONFIG_AUTH_CLIENT]
        search_client = current_app.config[CONFIG_SEARCH_CLIENT]
        authorized = False
        try:
            auth_claims = await auth_helper.get_auth_claims_if_enabled(request.headers)
            authorized = await auth_helper.check_path_auth(path, auth_claims, search_client)
        except AuthError:
            abort(403)
        except Exception as error:
            logging.exception("Problem checking path auth %s", error)
            return error_response(error, route="/content")

        if not authorized:
            abort(403)

        return await route_fn(path, auth_claims)

    return auth_handler


_C = TypeVar("_C", bound=Callable[..., Any])


def authenticated(route_fn: _C) -> _C:
    """
    Decorator for routes that might require access control. Unpacks Authorization header information into an auth_claims dictionary
    """

    @wraps(route_fn)
    async def auth_handler(*args, **kwargs):
        auth_helper = current_app.config[CONFIG_AUTH_CLIENT]

        subscriptionKey = request.headers.get("X-Subscription-Key")
        if subscriptionKey:
            categories = customers.get(subscriptionKey)
            if categories:
                # If the subscription key is valid, we can return the claims
                auth_claims = {"oid": subscriptionKey, "groups": categories}
            else:
                # If the subscription key is invalid, we return a 403
                logging.error("Invalid subscription key: %s", subscriptionKey)
                abort(403)
        else:
            abort(403)

        # try:
        #     auth_claims = await auth_helper.get_auth_claims_if_enabled(request.headers)
        # except AuthError:
        #     abort(403)

        return await route_fn(auth_claims, *args, **kwargs)

    return cast(_C, auth_handler)
