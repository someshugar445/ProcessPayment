from flask import Flask, render_template, request, abort
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, \
    SubmitField
from wtforms.validators import ValidationError, InputRequired, Optional, \
    Email, EqualTo, Length
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'


class ProcessPaymentForm(FlaskForm):
    card_number = StringField(label=('CreditCardNumber'),
                              validators=[InputRequired(),
                                          Length(min=16, max=20)])
    card_holder = StringField(label=('CardHolder'),
                              validators=[InputRequired(),
                                          Length(max=30)])
    expiration_date = DateField(label=('ExpirationDate'),
                                validators=[InputRequired()])
    security_code = StringField(label=('SecurityCode'),
                                validators=[Optional(),
                                            Length(max=4)])
    amount = IntegerField(label=('Amount'),
                          validators=[InputRequired()])
    submit = SubmitField(label=('Submit'))


@app.route('/processpayment', methods=('GET', 'POST'))
def processpayment():
    try:
        form = ProcessPaymentForm(request.form)
        if request.method == 'GET':
            return json.dumps({'error': "method is not allowed"}), 400, {'ContentType': 'application/json'}
        if request.method == 'POST' and form.validate_on_submit():
            return f'''<h1> Welcome {form.card_holder.data} </h1>'''
        return render_template('index.html', form=form)
    except Exception as e:
        abort(e, 500)


if __name__ == '__main__':
    app.run(debug=True)
