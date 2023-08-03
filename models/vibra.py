from db_config import db

#Vibra
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Cliente(db.Model):
    __tablename__ = 'tb_clientes'
    __table_args__ = {'schema': 'sc_sap'}

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

