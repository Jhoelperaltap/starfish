from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])



class ItemForm(Form):
    name = StringField('Name', [validators.InputRequired()])
    description = StringField('Description', [validators.InputRequired()])
