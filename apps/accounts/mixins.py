from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse

class LogoutRequiredMixin(AccessMixin):
    """Verify that the current user is unauthenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # next_url = request.GET.get('next', reverse('projects:projects_list'))
            return redirect('projects:projects_list')
            
        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
                return JsonResponse(
                    {"status": "error", "message": "You must login first!"}
                )
            next_url = request.GET.get('next', request.get_full_path())
            logout_url = reverse('accounts:logout')
            if next_url != logout_url:
                return redirect(f"{reverse('accounts:login')}?next={next_url}")

        return super().dispatch(request, *args, **kwargs)