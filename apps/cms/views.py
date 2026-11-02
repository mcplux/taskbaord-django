from typing import Any

from django.views.generic.base import TemplateView

from .models import HomePage


class HomePageView(TemplateView):
    template_name = "cms/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["page"] = HomePage.for_active_language()
        return context
