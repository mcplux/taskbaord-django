from typing import Any

from django import forms
from django.forms.renderers import BaseRenderer, TemplatesSetting

INPUT_CLASSES = (
    "mt-1 block w-full rounded-lg border-slate-300 bg-white text-sm text-slate-900 shadow-sm "
    "placeholder:text-slate-400 focus:border-indigo-500 focus:ring-indigo-500 "
    "aria-invalid:border-red-500 dark:border-slate-600 dark:bg-slate-800 dark:text-white"
)
CHECKBOX_CLASSES = (
    "size-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500 "
    "dark:border-slate-600 dark:bg-slate-800"
)


class TailwindFormRenderer(TemplatesSetting):
    """
    Render fields with the project's markup, so `{{ form.x.as_field_group }}` is styled
    """

    field_template_name = "forms/field.html"


class TailwindFormMixin:
    """
    Add Tailwind classes to the widgets and render with TailwindFormRenderer
    """

    default_renderer: BaseRenderer | type[BaseRenderer] | None = TailwindFormRenderer
    fields: dict[str, forms.Field]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            attrs = field.widget.attrs
            is_checkbox = isinstance(field.widget, forms.CheckboxInput)
            classes = CHECKBOX_CLASSES if is_checkbox else INPUT_CLASSES
            attrs["class"] = f"{classes} {attrs['class']}" if attrs.get("class") else classes
