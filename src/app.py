from flask import Flask, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, IntegerField, validators

from src import config, results
from src.validator import validate_cep, validate_cpf

application = Flask(__name__)
application.secret_key = config.FLASK_SECRET
csrf = CSRFProtect(application)

### FlaskForm set up
class CalculateForm(FlaskForm):
    """flask_wtf form class"""
    cep = StringField(
        u'CEP de entrega',
        [
            validators.InputRequired(message="Campo obrigatório. Por favor, preencha com um CEP válido."),
            validate_cep
        ]
    )
    cpf = StringField(
        u'CPF do organizador',
        [
            validators.InputRequired("Campo obrigatório. Por favor, preencha com um CPF válido."),
            validate_cpf
        ]
    )
    qtd_convidados = IntegerField(
        u'Quantidade de convidados',
        [
            validators.InputRequired("Campo obrigatório. Por favor, preencha com um número válido."),
            validators.NumberRange(min=1, max=127, message="Campo obrigatório. Por favor, forneça um valor no intervalo [%(min)s, %(max)s]")
        ]
    )


@application.route("/")
def home():
    "Home screen"
    form = CalculateForm()
    return render_template("view-form.html", form=form)


@application.route("/", methods=['POST'])
def calculate():
    "Calculate Churrasco"
    form = CalculateForm()
    if form.validate_on_submit():
        flash("Successfully calculated!")
        return render_template("view-results.html", info=results.calculate())
    else:
        return render_template("view-form.html", form=form), 400

