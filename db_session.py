from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import db_model
import db_log

Base = declarative_base()
ENGINE = db_model.get_engine()
Base.metadata.bind = ENGINE
DBSession = sessionmaker(bind=ENGINE)

def insert_object(object):
    session = DBSession()
    try:
        session = DBSession()
        session.add(object)
        session.commit()
    except Exception as e:
        db_log.error('exxor at inserting object')
        db_log.error('error info: %s' % str(e))
        session.rollback()
    finally:
        session.close()

def insert_list_object(list_object):
    session = DBSession()
    try:
        session.bulk_save_objects(list_object)
        session.commit()
    except Exception as e:
        db_log.error('exxor at inserting %d objects' % len(list_object))
        db_log.error('error info: %s' % str(e))
        session.rollback()
    finally:
        #print 'close'
        session.close()

def get_user_by_id(user_id):
    session = DBSession()
    try:
        query = session.query(db_model.User).filter_by(user_id=user_id)
        records = query.all()
        return records
    except Exception as e:
        db_log.error('error info: %s' % str(e))
        db_log.error('error at get_user_by_id id of user: %s'%user_id)
        return {}
    finally:
        session.close()

def get_schedule_by_date(date):
    session = DBSession()
    try:
        query = session.query(db_model.LogCheck).filter_by(date=date)
        records = query.all()
        return records
    except Exception as e:
        db_log.error('error info: %s' % str(e))
        db_log.error('error at get_schedule_by_date with date: %s' % date)
        return {}
    finally:
        session.close()



if __name__ == '__main__':
    #init_user_into_database()
    pass