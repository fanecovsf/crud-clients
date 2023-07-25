from sqlmodel import Field, SQLModel, create_engine, Session

#Constantes
#------------------------------------------------------------------------------------------------------------------------------------------------------------------
DATABASE_URL1 = 'postgresql+asyncpg://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/db_vibra'
DATABASE_URL2 = 'postgresql://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/db_minalba_mongodb'
DATABASE_URL3 = 'postgresql://postgres:pRxI65oIubsdTlf@4.228.57.67:5432/db_minalba'

engine_1 = create_engine(DATABASE_URL1)
engine_2 = create_engine(DATABASE_URL2)
engine_3 = create_engine(DATABASE_URL3)

session_1 = Session(engine_1)
session_2 = Session(engine_2)
session_3 = Session(engine_3)

class Cliente(SQLModel, table=True):
    __tablename__ = 'tb_clientes'
    __table_args__ = {'schema': 'sc_sap'}

    codigo: str = Field(primary_key=True)
    nome: str
    modelo_de_negocio: str
    tipo_de_cliente: str


class PlacasMinalbaMongo(SQLModel, table=True):
    __tablename__ = 'Viagens'
    __table_args__ = {'schema': 'public'}

    id: str = Field(primary_key=True)
    idVeiculo: str
    nomeEmbarcador: str


class PlacasMinalba(SQLModel, table=True):
    __tablename__ = 'tb_placas'
    __table_args__ = {'schema': 'sc_placa'}

    placa: str = Field(primary_key=True)
    classificacao: str
 