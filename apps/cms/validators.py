import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _

INVALID_LINK_MESSAGE = _(
    "Enter a path starting with “/”, an anchor starting with “#”, or an http(s) URL."
)

# "//host" and "/\host" are treated by browsers as links to another site, not as paths.
_LOCAL_LINK_RE = re.compile(r"(?!//|/\\)[/#][^\s\x00-\x1f\x7f]*")
_validate_absolute_url = URLValidator(schemes=["http", "https"], message=INVALID_LINK_MESSAGE)


def validate_link(value: str) -> None:
    """
    Allow only links that are safe to put in an href
    """
    if value.startswith(("/", "#")):
        if not _LOCAL_LINK_RE.fullmatch(value):
            raise ValidationError(INVALID_LINK_MESSAGE, code="invalid")
        return
    _validate_absolute_url(value)
