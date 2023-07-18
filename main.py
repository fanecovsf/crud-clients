from flask import Flask, render_template, request, redirect, url_for, Response
from flask_paginate import Pagination, get_page_args
from models.models import db, Cliente


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/db_vibra'


@app.route('/')
def table():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page=100)
    clientes = Cliente.query.offset(offset).limit(per_page).all()

    pagination = Pagination(page=page, total=Cliente.query.count(), record_name='clientes', per_page=per_page, css_framework='bootstrap4')

    return render_template('index.html', clientes=clientes, pagination=pagination)


@app.route('/edit/<codigo>', methods=['GET', 'POST'])
def edit(codigo):
    cliente = Cliente.query.get(codigo)
    if request.method == 'POST':
        cliente.modelo_de_negocio = request.form['modelo']
        cliente.tipo_de_cliente = request.form['tipo_cliente']
        db.session.commit()
        return redirect(url_for('table'))
    
    return render_template('edit.html', cliente=cliente)


if __name__ == '__main__':
    db.init_app(app=app)
    app.run(debug=True)

