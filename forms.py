from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    artist = StringField("Buscar Artista", validators=[DataRequired()])
    submit = SubmitField("Buscar")
