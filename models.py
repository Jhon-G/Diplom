from sqlalchemy import (Column, Date, String,
                        Integer, exists, BOOLEAN
                        )
from db import Base, concert_db


class Event(Base.Base):
    __tablename__ = 'information about the event'

    id = Column(Integer, primary_key=True)
    place_name = Column(String, unique=True)
    event_info = Column(String)
    event_date = Column(Date)

    def add_event(self, name, concert, concert_date):
        event = Event(place_name=name, event_info=concert, event_date=concert_date)

        concert_db.db_session.add(event)
        concert_db.db_session.commit()

    def get_event(self, name):
        event = Event.query.filter(Event.place_name == name)
        for info in event:
            print(info.place_name)
            concert = info.event_info
            concert_date = info.event_date
            return concert, concert_date

    def update_event(self, name, concert, concert_date):
        event = Event.query.filter(Event.place_name == name)
        for info in event:
            info.event_info = concert
            info.event_date = concert_date
            concert_db.db_session.commit()

    def is_exists(self, name):
        db_session = concert_db.db_session
        exists_info = db_session.query(exists().where(Event.place_name == name)).scalar()
        return exists_info


class Users(Base.Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True)
    user_name = Column(String)
    mutabor = Column(BOOLEAN)
    random = Column(BOOLEAN)

    def all_incoming_user(self, chat_id, user_name):
        user = Users.is_exists(chat_id)
        if user is not True:
            user = Users(chat_id=chat_id, user_name=user_name)
            concert_db.db_session.add(user)
            concert_db.db_session.commit()

    def subscribe(self, chat_id, place_name, call):
        user = Users.query.filter(Users.chat_id == chat_id)
        for info in user:
            if place_name == 'Mutabor':
                info.mutabor = True
            elif place_name == 'Random':
                info.random = True
        concert_db.db_session.commit()
        return f'Вы подписались на {place_name}'

    def unsubscribe(self, chat_id, place_name, call):
        user = Users.query.filter(Users.chat_id == chat_id)
        for info in user:
            if place_name == 'Mutabor':
                info.mutabor = False
            elif place_name == 'Random':
                info.random = False
        concert_db.db_session.commit()
        return f'Вы отписались от {place_name}'

    def is_exists(chat_id):
        db_session = concert_db.db_session
        exists_info = db_session.query(exists().where(Users.chat_id == chat_id)).scalar()
        return exists_info

    def is_exists_subscribe(self, chat_id, user_name=''):
        user = Users.query.filter(Users.chat_id == chat_id)
        for info in user:
            mutabor = info.mutabor
            random = info.random
            if user_name != '':
                if mutabor and random is True:
                    return 'Вы подписаны на: mutabor, random'
                elif mutabor is True:
                    return 'Вы подписаны на mutabor'
                elif random is True:
                    return 'Вы подписаны на random'
                else:
                    return 'Вы еще не на что не подписаны'
            else:
                return mutabor, random

    def get_chat_id(self):
        user = Users.query.filter(Users.id)
        for info in user:
            return info.chat_id


if __name__ == "__main__":
    Base.Base.metadata.create_all(bind=concert_db.engine)
