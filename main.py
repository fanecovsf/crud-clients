from flask import Flask, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_args
from models.models import db, Cliente, PlacasMinalbaMongo, PlacasMinalba
from sqlalchemy import exc
from sqlalchemy import event
from threading import Thread
import time


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/db_vibra'
app.config['SQLALCHEMY_DATABASE_URI_2'] = 'postgresql://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/db_minalba_mongodb'
app.config['SQLALCHEMY_DATABASE_URI_3'] = 'postgresql://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/db_minalba'

app.config['SQLALCHEMY_BINDS'] = {
    'db_vibra': app.config['SQLALCHEMY_DATABASE_URI'],
    'db_minalba_mongodb': app.config['SQLALCHEMY_DATABASE_URI_2'],
    'db_minalba': app.config['SQLALCHEMY_DATABASE_URI_3'],
}

app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30

db.init_app(app=app)

with app.app_context():
    @event.listens_for(db.engine, "engine_connect")
    def on_connect(dbapi_connection, connection_record):
        if isinstance(dbapi_connection, exc.DBAPIError):
            cursor = dbapi_connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()


@app.route('/')
def init():
    return 'Online'


@app.route('/clientes')
def table():
    search_term = request.args.get('search')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page='100')

    if search_term:
        clientes = Cliente.query.filter(Cliente.nome.ilike(f'%{search_term}%')).offset(offset).limit(per_page).all()
        total = Cliente.query.filter(Cliente.nome.ilike(f'%{search_term}%')).count()
    else:
        clientes = Cliente.query.offset(offset).limit(per_page).all()
        total = Cliente.query.count()

    pagination = Pagination(page=page, total=total, record_name='clientes', per_page=per_page, css_framework='bootstrap4')

    return render_template('index.html', clientes=clientes, pagination=pagination)


@app.route('/clientes/edit/<codigo>', methods=['GET', 'POST'])
def edit(codigo):
    cliente = Cliente.query.get(codigo)
    if request.method == 'POST':
        cliente.modelo_de_negocio = request.form['modelo']
        cliente.tipo_de_cliente = request.form['tipo_cliente']
        db.session.commit()
        return redirect(url_for('table'))
    
    return render_template('edit.html', cliente=cliente)


@app.route('/placas-minalba')
def placas_minalba():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page='100')

    placas = PlacasMinalba.query.offset(offset).limit(per_page).all()
    total = PlacasMinalba.query.count()

    pagination = Pagination(page=page, total=total, record_name='placas', per_page=per_page, css_framework='bootstrap4')

    return render_template('placas-minalba.html', placas=placas, pagination=pagination)

#Util
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def fill_placas_minalba():
    while True:
        time.sleep(7200)
        placas_distintas = db.session.query(PlacasMinalbaMongo.idVeiculo).filter(PlacasMinalbaMongo.nomeEmbarcador != 'MINALBA' and PlacasMinalbaMongo.nomeEmbarcador != '').distinct().all()

        for placa in placas_distintas:
            placa_existente = PlacasMinalba.query.filter_by(placa=placa[0]).first()
            if not placa_existente:
                placa_nova = PlacasMinalba(placa=placa[0], classificacao=None)
                db.session.add(placa_nova)

        db.session.commit()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)


#Constantes
#------------------------------------------------------------------------------------------------------------------------------------------------------------
THREAD_ATT = Thread(target=fill_placas_minalba)
