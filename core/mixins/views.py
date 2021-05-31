from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


class LogoutMixin:
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        request = self.request
        if request.user.is_authenticated:
            logout(request)
        return super(LogoutMixin, self).dispatch(*args, **kwargs)
