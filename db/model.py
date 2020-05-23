from sqlalchemy import Column, VARCHAR, Integer, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(VARCHAR(5), nullable=False, unique=True)

    def __init__(self, code):
        self.code = code


class CompanyGroup(Base):
    __tablename__ = 'company_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class TagGroup(Base):
    __tablename__ = 'tag_group'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False, unique=True)
    company_group_id = Column(ForeignKey(CompanyGroup.id), nullable=False)

    def __init__(self, name, company_group_id):
        self.name = name
        self.company_group_id = company_group_id


class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False)
    company_group_id = Column(ForeignKey(CompanyGroup.id), nullable=False)
    language_id = Column(ForeignKey(Language.id), nullable=False)

    def __init__(self, name, company_group_id, language_id):
        self.name = name
        self.company_group_id = company_group_id
        self.language_id = language_id


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(45), nullable=False)
    language_id = Column(ForeignKey(Language.id), nullable=False)
    tag_group_id = Column(ForeignKey(TagGroup.id), nullable=False)

    def __init__(self, name, language_id, tag_group_id):
        self.name = name
        self.language_id = language_id
        self.tag_group_id = tag_group_id


class CompanyTag(Base):
    __tablename__ = 'company_tag'
    __table_args__ = (
        PrimaryKeyConstraint('company_group_id', 'tag_group_id'),
    )
    company_group_id = Column(ForeignKey(CompanyGroup.id), nullable=False)
    tag_group_id = Column(ForeignKey(TagGroup.id), nullable=False)

    def __init__(self, company_group_id, tag_group_id):
        self.company_group_id = company_group_id
        self.tag_group_id = tag_group_id
