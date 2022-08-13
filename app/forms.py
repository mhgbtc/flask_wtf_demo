import re
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectMultipleField,
    SubmitField,
    TelField
)
from wtforms.validators import (
    DataRequired,
    URL,
    ValidationError
)


def validate_fr_phone(form, phone):
    fr_phone_num = '^(\+33|0)[1-9](\d\d){4}$'
    match = re.search(fr_phone_num, phone.data)
    if not match:
        raise ValidationError(
            'Error, phone number must be in format xxx-xxx-xxxx'
        )


def validate_property(form, property):
    properties = [
        'prop1',
        'prop2',
        'prop3',
    ]
    for property in property.data:
        if property not in properties:
            raise ValidationError(
                'This property is not allowed'
            )


properties_choices = [
    ('prop1', 'prop1'),
    ('prop2', 'prop2'),
    ('prop3', 'prop3'),
]


class ItemForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    some_url = StringField(
        'some_url', validators=[DataRequired(), URL()]
    )
    phone = TelField(
        'phone',
        validators=[validate_fr_phone, DataRequired()]
    )
    properties = SelectMultipleField(
        'properties', validators=[DataRequired(), validate_property],
        choices=properties_choices
    )
    submit = SubmitField("Create Item")


class ItemEditForm(ItemForm):
    submit = SubmitField("Edit Item")
