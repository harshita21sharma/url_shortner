from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import MiddlewareNotUsed
from .models import URL, Click

class ClickTrackingMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)
        if not get_response:
            raise MiddlewareNotUsed

    def process_view(self, request, view_func, view_args, view_kwargs):
        short_alias = view_kwargs.get('short_alias')
        if short_alias:
            url = URL.objects.filter(short_alias=short_alias).first()
            if url:
                ip_address = request.META.get('REMOTE_ADDR')
                referral_source = request.META.get('HTTP_REFERER')
                Click.objects.create(url=url, ip_address=ip_address, referer=referral_source)
                url.click_count += 1
                url.save()