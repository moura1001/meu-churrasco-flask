from flask import Flask, render_template, render_template_string, url_for, redirect, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, IntegerField, validators
from src import config

application = Flask(__name__)
application.secret_key = config.FLASK_SECRET
csrf = CSRFProtect(application)

### FlaskForm set up
class CalculateForm(FlaskForm):
    """flask_wtf form class"""
    cep = StringField(
        u'CEP de entrega',
        [validators.InputRequired(message="Campo obrigatório. Por favor, preencha com um CEP válido.")]
    )
    cpf = StringField(
        u'CPF do organizador',
        [validators.InputRequired("Campo obrigatório. Por favor, preencha com um CPF válido.")]
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


@application.route("/calculate", methods=['POST'])
def calculate():
    "Save an employee"
    form = CalculateForm()
    if form.validate_on_submit():
        flash("Successfully calculated!")
        return redirect(url_for("home"))
    else:
        return render_template("view-form.html", form=form)

