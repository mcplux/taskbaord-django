from django import forms

from apps.core.forms import CHECKBOX_CLASSES, INPUT_CLASSES, TailwindFormMixin


class SampleForm(TailwindFormMixin, forms.Form):
    name = forms.CharField(help_text="Your name")
    nickname = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "extra"}))
    agree = forms.BooleanField(required=False)


def test_widgets_get_classes_by_type() -> None:
    fields = SampleForm().fields

    assert fields["name"].widget.attrs["class"] == INPUT_CLASSES
    assert fields["agree"].widget.attrs["class"] == CHECKBOX_CLASSES


def test_existing_widget_classes_are_kept() -> None:
    assert SampleForm().fields["nickname"].widget.attrs["class"] == f"{INPUT_CLASSES} extra"


def test_field_group_links_errors_and_help_text_to_the_input() -> None:
    html = SampleForm(data={})["name"].as_field_group()

    assert 'aria-describedby="id_name_helptext id_name_error"' in html
    assert 'id="id_name_helptext"' in html
    assert 'id="id_name_error"' in html


def test_checkbox_field_group_places_the_label_after_the_input() -> None:
    html = SampleForm()["agree"].as_field_group()

    assert html.index('name="agree"') < html.index('<label for="id_agree"')


def test_other_forms_keep_the_default_renderer() -> None:
    class PlainForm(forms.Form):
        name = forms.CharField()

    assert "<label" in PlainForm()["name"].as_field_group()
    assert "mt-1" not in PlainForm()["name"].as_field_group()
