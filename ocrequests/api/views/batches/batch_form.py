from api.forms.arguments.date_arg import DateArg
from api.forms.arguments.email_arg import EmailAddressArg

batch_form = [
    EmailAddressArg(name="email_address"),
    DateArg(name="arrival_date"),
    DateArg(name="departure_date"),
]
