from typing import Any

from django.http import HttpRequest, HttpResponseBase
from django.http.response import HttpResponse, HttpResponseRedirectBase
from django.utils.cache import patch_vary_headers
from django.views.generic.base import TemplateResponseMixin, View


class HtmxMixin(TemplateResponseMixin, View):
    """
    Make a template view HTMX-aware
    """

    htmx_template: str | None = None

    @property
    def is_htmx(self) -> bool:
        headers = self.request.headers
        return headers.get("HX-Request") == "true"

    def get_template_names(self) -> list[str]:
        """
        HTMX renders only the {% partialdef %} from a template name
        """
        templates = super().get_template_names()
        if self.is_htmx and self.htmx_template:
            return [f"{template}#{self.htmx_template}" for template in templates]
        return templates

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        """
        Redirects become HX-Redirect header so HTMX does a full page navigation
        instead of swapping the redirect page into the target
        """
        response = super().dispatch(request, *args, **kwargs)
        if self.is_htmx and isinstance(response, HttpResponseRedirectBase):
            return HttpResponse(headers={"HX-Redirect": response.url})
        patch_vary_headers(response, ["HX-Request"])
        return response
