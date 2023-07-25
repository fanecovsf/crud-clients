from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'tb_clientes'
    __table_args__ = {'schema': 'sc_sap'}

    codigo = db.Column(db.String(), primary_key=True)
    nome = db.Column(db.String())
    modelo_de_negocio = db.Column(db.String())
    tipo_de_cliente = db.Column(db.String())

    def __init__(self, codigo, nome, modelo_de_negocio, tipo_cliente):
        self.codigo = codigo
        self.nome = nome
        self.modelo_de_negocio = modelo_de_negocio
        self.tipo_cliente = tipo_cliente


class PlacasMinalbaMongo(db.Model):
    __tablename__ = 'Viagens'
    __table_args__ = {'schema': 'public'}
    __bind_key__ = 'db_minalba_mongodb'
    
    id = db.Column(db.String(1000), primary_key=True)
    idVeiculo = db.Column(db.String(1000))
    nomeEmbarcador = db.Column(db.String(1000))

    def __init__(self, idVeiculo, id, nomeEmbarcador):
        self.id = id
        self.idVeiculo = idVeiculo
        self.nomeEmbarcador = nomeEmbarcador


class PlacasMinalba(db.Model):
    __tablename__ = 'tb_placas'
    __table_args__ = {'schema': 'sc_placa'}
    __bind_key__ = 'db_minalba'

    placa = db.Column(db.String(255), primary_key=True)
    classificacao = db.Column(db.String(255))

    def __init__(self, placa, classificacao):
        self.placa = placa
        self.classificacao = classificacao
