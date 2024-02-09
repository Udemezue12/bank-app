from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
# from functools import wraps
from django.contrib.auth.decorators import user_passes_test

def group_required(group_name, pass_test=True):
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name=group_name)) != pass_test or u.is_superuser:
                return True
            raise PermissionDenied
        return False
    return user_passes_test(in_groups)
