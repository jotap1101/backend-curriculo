from datetime import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from validate_docbr import CPF

def validate_name(value, field_name):
    if not all(x.isalpha() or x.isspace() for x in value):
        raise ValidationError(_("%(field_name)s must contain only letters and spaces."), params={"field_name": field_name})
    
    if len(value) < 2:
        raise ValidationError(_("%(field_name)s must contain at least 2 characters."), params={"field_name": field_name})
    
def validate_date_of_birth(value):
    if value >= date.today():
        raise ValidationError(_("The date of birth must be in the past."))

def validate_cpf(value):
    cpf = CPF()

    if not cpf.validate(value):
        raise ValidationError(_("%(value)s is not a valid CPF."), params={"value": value})
    
def validate_rg(value):
    if not value.isdigit():
        raise ValidationError(_("RG must contain only numbers."))

    if len(value) < 8:
        raise ValidationError(_("RG must contain at least 8 characters."))