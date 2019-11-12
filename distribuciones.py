#!/usr/bin/python3

from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField, DecimalField
from decimal import Decimal
from math import exp, e

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'qwertyuioplkjhgfdsxcvbnm'

class form_uniforme(Form):
    resul = IntegerField('resultados esperados :', validators=[validators.required()])

class form_binomial(Form):
    p = DecimalField('porcentaje exitos: ', validators=[validators.required()], places = 2)
    n = IntegerField('total de intentos', validators=[validators.required()])
    x = IntegerField('exitos esperados', validators=[validators.required()])

class form_hiper(Form):
    x = IntegerField('exitos esperados', validators=[validators.required()])
    n = IntegerField('muestra', validators=[validators.required()])
    K = IntegerField('exitos totales', validators=[validators.required()])
    N = IntegerField('Muestra total', validators=[validators.required()])

class form_poisson(Form):
    x = IntegerField('exitos esperados', validators=[validators.required()])
    lamb = IntegerField('exitos por unidad de tiempo', validators=[validators.required()])

def factorial(x):
    r=x
    i=x-1
    if x == 0:
        r=1
    else:
        while i > 0:
            r=i*r
            i=i-1
    return r
    
def combinacion(n, r):
    res=factorial(n) / (factorial(r) * factorial(n-r))
    return res

@app.route("/")
def index():
    return render_template('distribuciones.html')

@app.route("/uniforme/", methods=['GET', 'POST'])
def uniforme():
    form = form_uniforme(request.form)

    if request.method == 'POST':
        resul=form.resul.data
        prob=round(100/resul,2)
        return render_template('uniforme.html', form=form, prob=prob)
    else:
        return render_template('uniforme.html', form=form)

@app.route("/binomial", methods=['GET', 'POST'])
def binomial():
    form = form_binomial(request.form)

    if request.method == 'POST':
        p=form.p.data
        q=1-p
        x=form.x.data
        n=form.n.data
        prob= Decimal(combinacion(n,x)) * (p**x) * (q**(n-x))
        prob=round(prob*100,2)
        return render_template('binomial.html', form=form, prob=prob)

    return render_template('binomial.html', form=form)

@app.route("/hiper/", methods=['GET', 'POST'])
def hiper():
    form = form_hiper(request.form)

    if request.method == 'POST':
        x=form.x.data
        n=form.n.data
        K=form.K.data
        N=form.N.data
        prob= (combinacion(K,x)*combinacion((N-K),(n-x)))/combinacion(N,n)
        prob=round(prob*100,2)
        return render_template('hiper.html', form=form, prob=prob)
    else:
        return render_template('hiper.html', form=form)

@app.route("/poisson/", methods=['GET', 'POST'])
def poisson():
    form = form_poisson(request.form)

    if request.method == 'POST':
        x=form.x.data
        lamb=form.lamb.data
        prob=(exp(-lamb)*(lamb**x))/factorial(x)
        prob=round(prob*100,2)
        return render_template('poisson.html', form=form, prob=prob)
    else:
        return render_template('poisson.html', form=form)

if __name__=="__main__":
    app.run(host="0.0.0.0")
