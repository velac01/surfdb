import pandas as pd

from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

data = "data/3000.csv"


class Base(DeclarativeBase):
    pass


class Capec(Base):
    __tablename__ = "surf_capec"

    capec_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(4000))

    def __init__(self, capec_id, name, status, description) -> None:
        self.capec_id = capec_id
        self.name = name
        self.status = status
        self.description = description

    def __repr__(self):
        return f"(ID: {self.capec_id}) Name: {self.name} | Status: {self.status} | Desc: {self.description}\n\n"


def parse_capec_csv(file):
    raw_capec_df = pd.read_csv(file, index_col=False)
    clean_capec_df = raw_capec_df[
        ["ID", "Name", "Status", "Description", "Related Weaknesses"]
    ].fillna("N/A")
    return clean_capec_df


def prepop_capec_data(session):
    raw_capec_df = pd.read_csv(data, index_col=False)
    clean_capec_df = raw_capec_df[
        ["ID", "Name", "Status", "Description", "Related Weaknesses"]
    ].fillna("N/A")
    capecs = []
    for index, row in clean_capec_df.iterrows():
        id = row["ID"]
        name = row["Name"]
        status = row["Status"]
        description = row["Description"]
        curr = Capec(capec_id=id, name=name, status=status, description=description)
        capecs.append(curr)
    for capec in capecs:
        session.add(capec)
