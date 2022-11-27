from sqlalchemy import TIMESTAMP, Column, String, Integer, Sequence, select
from ..database import get_async_session
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'
    account_id = Column(Integer, Sequence('account_account_id_seq'), primary_key=True)
    login = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    frequent_flyer_id = Column(Integer)
    update_ts = Column(TIMESTAMP(timezone=True))
