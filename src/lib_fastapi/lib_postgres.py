from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

class Postgres():
    
    def __init__(self):
        pass
    
    def setDatabaseEngine(self, url: str = "postgresql://admin:admin123@meu_postgres/fastapi"):
        self.engine = create_engine(url)
        
    def setDatabaseSession(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def setDatabaseInstrumentation(self, tracer=None):
        # SQLAlchemyInstrumentor().instrument(engine=self.engine, 
        #                                     tracer_provider=tracer,
        #                                     enable_commenter=True, 
        #                                     commenter_options={})
        SQLAlchemyInstrumentor().instrument(engine=self.engine,
                                            enable_commenter=True, 
                                            commenter_options={})
        

class Exemplo(declarative_base()):
    __tablename__ = 'exemplo'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)