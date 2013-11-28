from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from setting import DBSetting

Base = declarative_base()
engine_url = 'mysql://%s:%s@%s/%s' % (DBSetting.DBUser, 
                                      DBSetting.DBPassword, 
                                      DBSetting.DBUrl, 
                                      DBSetting.DBName)
engine = create_engine(engine_url)


plugin = sqlalchemy.Plugin(
  engine, # SQLAlchemy engine created with create_engine function.
  Base.metadata, # SQLAlchemy metadata, required only if create=True.
  keyword='db', # Keyword used to inject session database in a route (default 'db').
  create=True, # If it is true, execute `metadata.create_all(engine)` when plugin is applied (default False).
  commit=True, # If it is true, plugin commit changes after route is executed (default True).
  use_kwargs=False # If it is true and keyword is not defined, plugin uses **kwargs argument to inject session database (default False).
)


class Redeem(Base):
  __tablename__ = DBSetting.DBTable
  owner_email = Column(String(64), primary_key=True)
  redeem_code = Column(String(8), index=True)
  item_no = Column(Integer)
  receiver_email = Column(String(64), index=True)
  create_time = Column(DateTime)
  receive_time = Column(DateTime)
  receive_ip = Column(String(24))

  def __init__(self, 
               owner_email,
               redeem_code, 
               item_no):
    self.owner_email = owner_email
    self.redeem_code = redeem_code
    self.item_no = item_no
    self.receiver_email = None
    self.receive_time = None
    self.receive_ip = None


