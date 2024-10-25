from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
import re


class ComplexPasswordValidator:
    """
    Validate whether the password contains minimum one uppercase, one digit and one symbol.
    """
    def validate(self, password, user=None):
        if re.search('[A-Z]', password) is None or re.search('[0-9]', password) is None or re.search('[^A-Za-z0-9]', password) is None:
            raise ValidationError(
                _("To hasło jest zbyt słabe. Hasło musi zawierać przynajmniej jedną dużą literę, jedną cyfrę i jeden znak specjalny."),
                code='password_is_weak',
            )

    def get_help_text(self):
        return _("Hasło musi zawierać przynajmniej jedną dużą literę, jedną cyfrę i jeden znak specjalny.")
