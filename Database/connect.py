from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Bot.lig_bot_config import LigBotConfig

engine = create_engine('postgresql://{}:{}@{}/{}'.format(LigBotConfig.db_user, LigBotConfig.db_password, LigBotConfig.db_host, LigBotConfig.db_name), echo=True)

_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()
