from flask_wtf import FlaskForm
from wtforms import BooleanField, HiddenField, StringField, TextAreaField
from wtforms.validators import DataRequired

from registry.donor.models import AwardedMedals, DonorsOverride
from registry.utils import NumericValidator


class RemoveMedalForm(FlaskForm):
    rodne_cislo = HiddenField(validators=[DataRequired()])
    medal_id = HiddenField(validators=[DataRequired()])

    def validate(self):
        self.awarded_medal = AwardedMedals.query.get(
            (self.rodne_cislo.data, self.medal_id.data)
        )
        return self.awarded_medal is not None


class AwardMedalForm(FlaskForm):
    medal_id = HiddenField(validators=[DataRequired()])

    def add_checkboxes(self, rodna_cisla):
        for rodne_cislo in rodna_cisla:
            name = "rodne_cislo_" + rodne_cislo
            checkbox = BooleanField(_form=self, _name="rodne_cislo", default="checked")
            checkbox.data = rodne_cislo
            setattr(self, name, checkbox)

    def add_one_rodne_cislo(self, rodne_cislo):
        rodne_cislo_input = HiddenField(
            _form=self, _name="rodne_cislo", validators=[DataRequired()]
        )
        rodne_cislo_input.data = rodne_cislo
        setattr(self, "rodne_cislo", rodne_cislo_input)


class NoteForm(FlaskForm):
    rodne_cislo = HiddenField(validators=[DataRequired()])
    note = TextAreaField("Poznámka k dárci")


class IgnoreDonorForm(FlaskForm):
    rodne_cislo = StringField("Rodné číslo", validators=[DataRequired()])
    reason = StringField("Důvod k ignoraci", validators=[DataRequired()])


class RemoveFromIgnoredForm(FlaskForm):
    rodne_cislo = HiddenField(validators=[DataRequired()])


class DonorsOverrideForm(FlaskForm):
    rodne_cislo = StringField("Rodné číslo", validators=[DataRequired()])
    first_name = StringField("Jméno")
    last_name = StringField("Příjmení")
    address = StringField("Adresa")
    city = StringField("Město")
    postal_code = StringField("PSČ", validators=[NumericValidator(5)])
    kod_pojistovny = StringField("Pojišťovna", validators=[NumericValidator(3)])

    _fields_ = [
        "rodne_cislo",
        "first_name",
        "last_name",
        "address",
        "city",
        "postal_code",
        "kod_pojistovny",
    ]

    def init_fields(self, rodne_cislo):
        override = DonorsOverride.query.get(rodne_cislo)

        if override is not None:
            for field in self._fields_:
                data = getattr(override, field)
                if data is not None:
                    getattr(self, field).data = data

        self.rodne_cislo.data = rodne_cislo

    def get_field_data(self):
        field_data = {}
        for field in self._fields_:
            field_data[field] = getattr(self, field).data or None

        return field_data
