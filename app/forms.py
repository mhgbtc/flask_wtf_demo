import re
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectMultipleField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    ValidationError
)


# example of a custom validator
def validate_jamesbond(form, jamesbond):
    jamebond_rule = '[a-zA-Z]+007$'
    match = re.search(jamebond_rule, jamesbond.data)
    if not match:
        raise ValidationError(
            'Error, you are not 007'
        )


properties_choices = [
    ('prop1', 'prop1'),
    ('prop2', 'prop2'),
    ('prop3', 'prop3'),
]


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


class ItemForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    properties = SelectMultipleField(
        'properties', validators=[DataRequired(), validate_property],
        choices=properties_choices
     )
    submit = SubmitField("Create Item")


class ItemEditForm(ItemForm):
    submit = SubmitField("Edit Item")
