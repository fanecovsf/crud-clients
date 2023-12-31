from flask import Flask, render_template, request, redirect, url_for
from flask_paginate import Pagination, get_page_args
from models.minalba import MsgMinalba, PlacasMinalba
from models.vibra import Cliente, Produto, Transportadora
from db_config import db
from sqlalchemy import exc, event


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/db_vibra'
app.config['SQLALCHEMY_DATABASE_URI_2'] = 'postgresql://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/db_minalba'
app.config['SQLALCHEMY_DATABASE_URI_3'] = 'postgresql://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/BD01-VIBRA'

app.config['SQLALCHEMY_BINDS'] = {
    'db_vibra': app.config['SQLALCHEMY_DATABASE_URI'],
    'db_minalba': app.config['SQLALCHEMY_DATABASE_URI_2'],
    'BD01-VIBRA': app.config['SQLALCHEMY_DATABASE_URI_3']
}

app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 300
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800

db.init_app(app=app)

with app.app_context():
    @event.listens_for(db.engine, "engine_connect")
    def on_connect(dbapi_connection, connection_record):
        if hasattr(dbapi_connection, 'ping'):
            cursor = dbapi_connection.cursor()
            try:
                cursor.execute("SELECT 1")
            except:
                cursor.close()
                dbapi_connection.close()
                raise exc.DisconnectionError()
            cursor.close()


@app.route('/')
def init():
    return 'Online'


@app.route('/clientes')
def table():
    search_term = request.args.get('search-name')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page='100')

    search_ope = request.args.get('drop')

    if search_ope == 'outbound':
        if search_term:
            clientes = db.session.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).filter_by(outbound=True).offset(offset).limit(per_page)
            total = db.session.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).filter_by(outbound=True).count()
        else:
            clientes = db.session.query(Cliente).filter_by(outbound=True).offset(offset).limit(per_page)
            total = db.session.query(Cliente).filter_by(outbound=True).count()

    elif search_ope == 'inbound':
        if search_term:
            clientes = db.session.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).filter_by(outbound=False).offset(offset).limit(per_page)
            total = db.session.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).filter_by(outbound=False).count()
        else:
            clientes = db.session.query(Cliente).filter_by(outbound=False).offset(offset).limit(per_page)
            total = db.session.query(Cliente).filter_by(outbound=False).count()  

    else:
        if search_term:
            clientes = db.session.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).offset(offset).limit(per_page)
            total = db.session.query(Cliente).filter(Cliente.nome.ilike(f'%{search_term}%')).count()
        else:
            clientes = db.session.query(Cliente).offset(offset).limit(per_page)
            total = db.session.query(Cliente).count()

    pagination = Pagination(page=page, total=total, record_name='clientes', per_page=per_page, css_framework='bootstrap4')

    return render_template('index.html', clientes=clientes, pagination=pagination)


@app.route('/clientes/edit/<codigo>', methods=['GET', 'POST'])
def edit(codigo):
    cliente = db.session.get(Cliente, codigo)
    if request.method == 'POST':
        cliente.modelo_de_negocio = request.form['modelo']
        cliente.tipo_de_cliente = request.form['tipo_cliente']
        db.session.commit()
        return redirect(url_for('table'))
    
    return render_template('edit.html', cliente=cliente)


@app.route('/placas-minalba')
def placas_minalba():
    search_term = request.args.get('search')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page='100')

    if search_term:
        placas = db.session.query(PlacasMinalba).filter(PlacasMinalba.placa.ilike(f'%{search_term}%')).offset(offset).limit(per_page)
        total = db.session.query(PlacasMinalba).filter(PlacasMinalba.placa.ilike(f'%{search_term}%')).count()
    else:
        placas = db.session.query(PlacasMinalba).offset(offset).limit(per_page)
        total = db.session.query(PlacasMinalba).count()

    pagination = Pagination(page=page, total=total, record_name='placas', per_page=per_page, css_framework='bootstrap4')

    return render_template('placas-minalba.html', placas=placas, pagination=pagination)


@app.route('/placas-minalba/edit/<placa>', methods=['GET', 'POST'])
def edit_placa(placa):
    placa = db.session.get(PlacasMinalba, placa)
    if request.method == 'POST':
        placa.classificacao = request.form['classificacao']
        db.session.commit()
        return redirect(url_for('placas_minalba'))
    
    return render_template('edit-placas-minalba.html', placa=placa)


@app.route('/macros-minalba')
def macros_minalba():
    search_term = request.args.get('search')

    if search_term:
        macros = db.session.query(MsgMinalba).filter(MsgMinalba.msg_original.ilike(f'%{search_term}%')).order_by(MsgMinalba.msg_original)
    else:
        macros = db.session.query(MsgMinalba).order_by(MsgMinalba.msg_original)

    return render_template('macros-minalba.html', macros=macros)


@app.route('/macros-minalba/edit/<msg>', methods=['GET', 'POST'])
def edit_macros(msg):
    if not db.session.get(MsgMinalba, msg):
        msg = str(msg).replace('-','/')
        macro = db.session.get(MsgMinalba, msg)
    else:
        macro = db.session.get(MsgMinalba, msg)

    msgs = [
        'NÃO INFORMADO',
        'CHEGADA CLIENTE/CD',
        'EMERGENCIA',
        'FIM DE CHECK LIST',
        'PARADA PARA REFEIÇÃO',
        'FIM DE JORNADA',
        'INICIO DE CHECK LIST',
        'CHEGADA NA FABRICA',
        'INICIO DE JORNADA',
        'ABASTECIMENTO',
        'INICIO DE VIAGEM',
        'FATURAMENTO',
        'PARADA PARA DESCANSO',
        'PERNOITE',
        'CHEGADA GARAGEM',
        'CHEGADA NA OFICINA',
        'REINICIO DE VIAGEM',
        'SCRIPT: MANUTENÇÃO - FADEL',
        'TROCA DE MOTORISTA',
    ]

    msgs.sort()

    if request.method == 'POST':
        macro.msg_corrigida = request.form['nova']
        db.session.commit()
        return redirect(url_for('macros_minalba'))
    
    return render_template('edit-macros-minalba.html', macro=macro, msgs=msgs)


@app.route('/produtos')
def produtos():
    query = Produto.query_filtered()
    search_term = request.args.get('search-name')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page='100')

    if search_term:
        produtos = query.filter(Produto.produto_nome.ilike(f"%{search_term}%")).order_by(Produto.produto_codigo).offset(offset).limit(per_page)
        total = query.filter(Produto.produto_nome.ilike(f"%{search_term}%")).count()

    else:
        produtos = query.order_by(Produto.produto_codigo).offset(offset).limit(per_page)
        total = query.count()

    pagination = Pagination(page=page, total=total, record_name='produtos', per_page=per_page, css_framework='bootstrap4')

    return render_template('vibra-produtos.html', produtos=produtos, pagination=pagination)


@app.route('/produtos/edit/<codigo>', methods=['GET', 'POST'])
def edit_produto(codigo):
    produto = db.session.get(Produto, codigo)
    lista_grupos = Produto.group_list()

    if request.method == 'POST':
        if request.form['grupo_produto'] == 'None':
            grupo = None

        else:
            grupo = request.form['grupo_produto']

        produto.produto_grupo = grupo

        if request.form['torre'] == 'Torre':
            produto.produto_torre = True

        else:
            produto.produto_torre = False

        db.session.commit()

        return redirect(url_for('produtos'))
    
    return render_template('edit-produtos.html', produto=produto, lista_grupos=lista_grupos)


@app.route('/transportadoras')
def transportadoras():
    search_cod = request.args.get('search-cod')
    search_grupo = request.args.get('search-grupo')
    search_name = request.args.get('search-name')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page='100')

    query = Transportadora.query()

    if search_cod:
        query = query.filter(Transportadora.transportadora_codigo_sap.ilike(f'%{search_cod}%'))

    if search_grupo:
        query = query.filter(Transportadora.transportadora_grupo_atlas.ilike(f'%{search_grupo}%'))

    if search_name:
        query = query.filter(Transportadora.transportadora_nome_sap.ilike(f'%{search_name}%'))

    transportadoras = query.order_by(Transportadora.transportadora_codigo_sap).offset(offset).limit(per_page)
    total = query.count()

    pagination = Pagination(page=page, total=total, record_name='transportadoras', per_page=per_page, css_framework='bootstrap4')

    return render_template('vibra-transportadoras.html', transportadoras=transportadoras, pagination=pagination)


@app.route('/transportadoras/edit/<cod>', methods=['GET', 'POST'])
def edit_transportadoras(cod):
    transportadora = db.session.get(Transportadora, cod)

    if request.method == 'POST':
        transportadora.transportadora_grupo_atlas = request.form.get('grupo')
        db.session.commit()

        return redirect(url_for('transportadoras'))
    
    return render_template('edit-transportadoras.html', transportadora=transportadora)



if __name__ == '__main__':
    app.run(debug=True)
