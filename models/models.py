from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy

class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(self, app, options)
        options["pool_pre_ping"] = True

db = SQLAlchemy()

#Vibra
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
        

#Minalba
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class PlacasMinalba(db.Model):
    __tablename__ = 'tb_placas'
    __table_args__ = {'schema': 'sc_placa'}
    __bind_key__ = 'db_minalba'

    placa = db.Column(db.String(255), primary_key=True)
    classificacao = db.Column(db.String(255))

    def __init__(self, placa, classificacao):
        self.placa = placa
        self.classificacao = classificacao


class MsgMinalba(db.Model):
    __tablename__ = 'tb_macro_dimensao'
    __table_args__ = {'schema': 'sc_macros'}
    __bind_key__ = 'db_minalba'

    msg_original = db.Column(db.String(500), primary_key=True)
    msg_corrigida = db.Column(db.String(500))

    def __init__(self, msg_original, msg_corrigida):
        self.msg_original = msg_original
        self.msg_corrigida = msg_corrigida
