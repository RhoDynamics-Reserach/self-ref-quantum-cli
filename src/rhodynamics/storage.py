from sqlalchemy import create_engine, Column, String, Float, JSON, Integer
try:
    from sqlalchemy.orm import declarative_base, sessionmaker
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
import os
import json
import numpy as np
import datetime

Base = declarative_base()

class DBAgent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    objective = Column(String)
    zeta = Column(Float)
    tau_m = Column(Float)
    knowledge_vector = Column(JSON)
    created_at = Column(String)

class DBHistory(Base):
    __tablename__ = "interaction_history"
    id = Column(Integer, primary_key=True)
    agent_name = Column(String)
    zeta = Column(Float)
    s_int = Column(Float)
    timestamp = Column(String)

class StorageManager:
    def __init__(self, db_path="rho_vault.db"):
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def log_interaction(self, agent_name, zeta, s_int=0.0):
        session = self.Session()
        try:
            log = DBHistory(
                agent_name=agent_name,
                zeta=float(zeta),
                s_int=float(s_int),
                timestamp=str(datetime.datetime.now())
            )
            session.add(log)
            session.commit()
        finally:
            session.close()

    def get_history(self, agent_name):
        session = self.Session()
        try:
            return session.query(DBHistory).filter(DBHistory.agent_name == agent_name).all()
        finally:
            session.close()

    def save_agent(self, agent):
        session = self.Session()
        try:
            db_agent = session.query(DBAgent).filter(DBAgent.name == agent.name).first()
            if not db_agent:
                db_agent = DBAgent(name=agent.name)
                session.add(db_agent)
            
            db_agent.zeta = float(agent.zeta)
            db_agent.tau_m = float(agent.tau_m)
            db_agent.knowledge_vector = agent.knowledge_vector.tolist()
            db_agent.objective = getattr(agent, 'objective', "Quantum Researcher")
            session.commit()
        finally:
            session.close()

    def get_all_agents(self):
        session = self.Session()
        try:
            return session.query(DBAgent).all()
        finally:
            session.close()

    def delete_agent(self, name):
        session = self.Session()
        try:
            session.query(DBAgent).filter(DBAgent.name == name).delete()
            session.commit()
        finally:
            session.close()

    def clear_all(self):
        """Purges all agents and histories from the vault."""
        session = self.Session()
        try:
            session.query(DBAgent).delete()
            session.query(DBHistory).delete()
            session.commit()
        finally:
            session.close()
