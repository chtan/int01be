from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse

def token_required(view_func):
	@wraps(view_func)
	def _wrapped_view(request, *args, **kwargs):
		if not request.session.get("access_token"):
			return redirect(reverse("core:token"))
		return view_func(request, *args, **kwargs)

	return _wrapped_view


