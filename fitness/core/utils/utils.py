import threading
from django.contrib.sites.shortcuts import get_current_site

_thread_locals = threading.local()


def set_current_user(user):
    _thread_locals.user = user


def get_current_user():
    return getattr(_thread_locals, "user", None)


def get_domain_url(request):
    return request.scheme + "://" + get_current_site(request).domain


def get_or_none(class_, **kwargs) -> object:
    try:
        return class_.objects.get(**kwargs)
    except class_.DoesNotExist:
        pass
    except class_.MultipleObjectsReturned:
        return []
    return None
