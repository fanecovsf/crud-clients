from flask import Flask, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_args
#from models.models import db, Cliente, PlacasMinalbaMongo, PlacasMinalba
from models.models2 import Cliente, PlacasMinalbaMongo, PlacasMinalba, engine_1, engine_2, engine_3, session_1, session_2, session_3
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

with app.app_context():
    @event.listens_for(engine_1, "connect")
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
        clientes = session_1.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).offset(offset).limit(per_page).all()
        total = session_1.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).count()
    else:
        clientes = session_1.query(Cliente).limit(per_page).offset(offset).all()
        total = session_1.query(Cliente).count()

    pagination = Pagination(page=page, total=total, record_name='clientes', per_page=per_page, css_framework='bootstrap4')

    return render_template('index.html', clientes=clientes, pagination=pagination)


@app.route('/clientes/edit/<codigo>', methods=['GET', 'POST'])
def edit(codigo):
    cliente = session_1.query(Cliente).get(codigo)
    if request.method == 'POST':
        cliente.modelo_de_negocio = request.form['modelo']
        cliente.tipo_de_cliente = request.form['tipo_cliente']
        session_1.commit()
        return redirect(url_for('table'))
    
    return render_template('edit.html', cliente=cliente)


@app.route('/placas-minalba')
def placas_minalba():
    search_term = request.args.get('search')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page='100')

    if search_term:
        placas = session_3.query(PlacasMinalba).filter(PlacasMinalba.placa.ilike(f'%{search_term}%')).offset(offset).limit(per_page).all()
        total = session_3.query(PlacasMinalba).filter(PlacasMinalba.placa.ilike(f'%{search_term}%')).count()
    else:
        placas = session_3.query(PlacasMinalba).offset(offset).limit(per_page).all()
        total = session_3.query(PlacasMinalba).count()

    pagination = Pagination(page=page, total=total, record_name='placas', per_page=per_page, css_framework='bootstrap4')

    return render_template('placas-minalba.html', placas=placas, pagination=pagination)


@app.route('/placas-minalba/edit/<placa>', methods=['GET', 'POST'])
def edit_placa(placa):
    placa = session_3.query(PlacasMinalba).get(placa)
    if request.method == 'POST':
        placa.classificacao = request.form['classificacao']
        session_3.commit()
        return redirect(url_for('placas_minalba'))
    
    return render_template('edit-placas-minalba.html', placa=placa)

#Util
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def fill_placas_minalba():
    while True:
        time.sleep(7200)
        placas_distintas = session_2.query(PlacasMinalbaMongo.idVeiculo).filter(PlacasMinalbaMongo.nomeEmbarcador != 'MINALBA' and PlacasMinalbaMongo.nomeEmbarcador != '').distinct().all()

        for placa in placas_distintas:
            placa_existente = session_3.query(PlacasMinalba).filter_by(placa=placa[0]).first()
            if not placa_existente:
                placa_nova = PlacasMinalba(placa=placa[0], classificacao=None)
                session_3.add(placa_nova)

        session_3.commit()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)


#Constantes
#------------------------------------------------------------------------------------------------------------------------------------------------------------
THREAD_ATT = Thread(target=fill_placas_minalba)

