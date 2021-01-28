from sqlalchemy import Column, Date, String, Integer, exists
from db import concert_base, concert_db


class Event(concert_base.Base):
    __tablename__ = 'information about the event'

    id = Column(Integer, primary_key=True)
    place_name = Column(String, unique=True)
    event_info = Column(String)
    event_date = Column(Date)

    def add_event(name, concert, concert_date):
        event = Event(place_name=name, event_info=concert, event_date=concert_date)

        concert_db.db_session.add(event)
        concert_db.db_session.commit()

    def get_event(self, name):
        event = self.query.filter(Event.place_name == name)
        for info in event:
            print(info.place_name)
            concert = info.event_info
            concert_date = info.event_date
            return concert, concert_date

    def update_event(self, name, concert, concert_date):
        event = self.query.filter(Event.place_name == name)
        for info in event:
            info.event_info = concert
            info.event_date = concert_date
            concert_db.db_session.commit()

    def exsits(self, name):
        db_session = concert_db.db_session
        exists_info = db_session.query(exists().where(Event.place_name == name)).scalar()
        return exists_info


if __name__ == "__main__":
    concert_base.Base.metadata.create_all(bind=concert_db.engine)
