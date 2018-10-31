import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Unicode, DateTime, Date, Time
from sqlalchemy import types
from sqlalchemy.dialects.mysql.base import MSBinary
import uuid
from sqlalchemy.orm import relationship

Base = declarative_base()

class UUID(types.TypeDecorator):
    impl = MSBinary
    def __init__(self):
        self.impl.length = 16
        types.TypeDecorator.__init__(self,length=self.impl.length)

    def process_bind_param(self,value,dialect=None):
        if value and isinstance(value,uuid.UUID):
            return value.bytes
        elif value and not isinstance(value,uuid.UUID):
            raise 'value %s is not a valid uuid.UUID' % value
        else:
            return None

    def process_result_value(self,value,dialect=None):
        if value:
            return uuid.UUID(bytes=value)
        else:
            return None

    def is_mutable(self):
        return False

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    name = Column(Unicode(256), nullable=False)
    avatar = Column(String(256))

    def __init__(self, user_id, name, avatar):
        self.user_id = user_id
        self.name = name
        self.avatar = avatar

class LogCheck(Base):
    __tablename__ = 'log_check'
    uuid = Column('UUID', UUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey(User.user_id))
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    modify = Column(DateTime)

    user = relationship('user', foreign_keys='user.user_id')

    def __init__(self, user_id, date, start, end, modify):
        self.user_id = user_id
        self.date = date
        self.start_time = start
        self.end_time = end
        self.modify = modify

ACCESS_FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/access.txt'

def read_file_config():
    result = {}
    f = open(ACCESS_FILE_PATH, 'r')
    for line in f:
        temp = line.split(':')
        result[temp[0].strip()] = temp[1].strip()
    f.close()
    return result

CONFIG_DIC = read_file_config()

def get_engine():
    user_name = CONFIG_DIC['user']
    password = CONFIG_DIC['password']
    host = CONFIG_DIC['host']
    db_name = CONFIG_DIC['database']
    mysql_engine_str = 'mysql+mysqldb://%s:%s@%s/%s?charset=utf8mb4' % (user_name, password, host, db_name)
    engine = create_engine(mysql_engine_str, pool_recycle=3600 * 7)
    return engine

def create_database():
    engine = get_engine()
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    create_database()