import json
import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP
from model import Base

__author__ = 'leswing'

indexer = 0


class ParsedFile(Base):
    __tablename__ = 'parsed_file'

    def __init__(self):
        self.indexer = indexer
        self.timestamp = datetime.datetime.now()

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    indexer = Column(Integer)
    timestamp = Column(TIMESTAMP)

    def to_json(self):
        d = {
            "id": self.id,
            "filename": self.filename,
            "indexer": self.indexer,
            "timestamp": self.timestamp
        }
        return json.dumps(d)
