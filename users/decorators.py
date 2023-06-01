import functools
from django.contrib import messages
from django.shortcuts import redirect


def authentication_not_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.college == "Other":
            return redirect("waitlist")
        else:
            return view_func(request,*args, **kwargs)
    return wrapper