from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from repository import RepoWrapper

Base = declarative_base()
engine = create_engine('postgresql://@localhost/pregit', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class AuditMixin(object):
    created_at = Column(DateTime, default=(datetime.now))
    updated_at = Column(DateTime, default=(datetime.now), onupdate=(datetime.now))


class BaseMixin(object):
    _repr_hide = [
     'created_at', 'updated_at']

    @classmethod
    def query(cls):
        return session.query(cls)

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by(cls, **kw):
        return (cls.query.filter_by)(**kw).first()

    @classmethod
    def get_or_create(cls, **kwargs):
        instance = (session.query(cls).filter_by)(**kwargs).first()
        if instance:
            return instance
        instance = cls(**kwargs)
        session.add(instance)
        session.commit()
        return instance

    def __repr__(self):
        values = ', '.join(('%s=%r' % (n, getattr(self, n)) for n in self.__table__.c.keys() if n not in self._repr_hide))
        return '%s(%s)' % (self.__class__.__name__, values)


class Repository(Base, BaseMixin):
    __tablename__ = 'repository'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String, unique=True)
    path = Column(String)
    description = Column(String)

    def git_repo(self):
        return RepoWrapper(self.path)


class Merge(Base, BaseMixin):
    __tablename__ = 'merge'
    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey(Repository.id))
    repository = relationship(Repository)
    commit_source_hash = Column(String)
    commit_dest_hash = Column(String, unique=True)
    commit_hash_a = Column(String)
    commit_hash_b = Column(String)
    diff_a = Column(String)
    diff_b = Column(String)

class CommitFile(Base, BaseMixin):
    __tablename__ = 'commit_file'
    id = Column(Integer, primary_key=True)
    path = Column(String)
    source_content = Column(String)
    dest_content = Column(String)
    diff = Column(String)
    UniqueConstraint('merge_id', 'path', name='commit_file_merge_id_path_idx')


if __name__ == '__main__':
    Base.metadata.create_all(engine)
