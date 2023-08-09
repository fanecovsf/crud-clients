from db_config import db

#Vibra
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Cliente(db.Model):
    __tablename__ = 'tb_clientes'
    __table_args__ = {'schema': 'sc_sap'}
    __bind_key__ = 'db_vibra'

    codigo = db.Column(db.String(), primary_key=True)
    nome = db.Column(db.String())
    modelo_de_negocio = db.Column(db.String())
    tipo_de_cliente = db.Column(db.String())
    outbound = db.Column(db.Boolean())

    def __init__(self, codigo, nome, modelo_de_negocio, tipo_cliente, outbound):
        self.codigo = codigo
        self.nome = nome
        self.modelo_de_negocio = modelo_de_negocio
        self.tipo_cliente = tipo_cliente
        self.outbound = outbound


class Produto(db.Model):
    __tablename__ = 'tb_produtos'
    __table_args__ = {'schema': 'sc_sap'}
    __bind_key__ = 'db_vibra'

    produto_codigo = db.Column(db.String(), primary_key=True)
    produto_nome = db.Column(db.String())
    produto_tipo = db.Column(db.String())
    produto_grupo = db.Column(db.String())
    produto_torre = db.Column(db.Boolean()) #True = Torre e False = Vibra

    def __init__(self, produto_codigo, produto_nome, produto_tipo, produto_grupo, produto_torre):
        self.produto_codigo = produto_codigo
        self.produto_nome = produto_nome
        self.produto_tipo = produto_tipo
        self.produto_grupo = produto_grupo
        self.produto_torre = produto_torre

    @staticmethod
    def query_filtered():
        return db.session.query(Produto).filter(Produto.produto_tipo != 'FORA DO ESCOPO')
    
    @staticmethod
    def group_list():
        grupos = db.session.query(Produto.produto_grupo).distinct().order_by(Produto.produto_grupo)
        lista_grupos = []

        for grupo in grupos:
            lista_grupos.append(grupo.produto_grupo)

        return lista_grupos
