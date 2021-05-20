"""Helper utilities and decorators."""
from flask import flash

from registry.donor.models import Medals


def flash_errors(form, category="warning"):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            # make the first character of the label lowercase
            field_label = getattr(form, field).label.text
            field_label = field_label[0].lower() + field_label[1:]

            flash(f"{error} (pole: {field_label})", category)


def template_globals():
    """
    Injected into all templates
     - all medals are needed for the nav bar
    """
    all_medals = Medals.query.all()
    return dict(all_medals=all_medals)
