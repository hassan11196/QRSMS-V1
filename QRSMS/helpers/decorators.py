
from functools import wraps


def user_passes_test(test_func, on_failure_json_response):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # print('We Checking if user passes test')
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            return on_failure_json_response
        return _wrapped_view
    return decorator
