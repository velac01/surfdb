from tqdm import tqdm

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
    likelihood_of_attack: Mapped[str] = mapped_column(String(50))
    typical_severity: Mapped[str] = mapped_column(String(50))

    def __init__(
        self,
        capec_id,
        name,
        status,
        description,
        likelihood_of_attack,
        typical_severity,
    ) -> None:
        self.capec_id = capec_id
        self.name = name
        self.status = status
        self.description = description
        self.likelihood_of_attack = likelihood_of_attack
        self.typical_severity = typical_severity

    def __repr__(self):
        return f"(CAPEC ID: {self.capec_id}) Name: {self.name} \n\n"


def parse_capec_csv(file):
    raw_capec_df = pd.read_csv(file, index_col=False)
    clean_capec_df = raw_capec_df[
        ["ID", "Name", "Status", "Description", "Related Weaknesses"]
    ].fillna("N/A")
    return clean_capec_df


def prepop_capec_data(session):
    raw_capec_df = pd.read_csv(data, index_col=False)
    clean_capec_df = raw_capec_df[
        [
            "ID",
            "Name",
            "Status",
            "Description",
            "Related Weaknesses",
            "Likelihood Of Attack",
            "Typical Severity",
        ]
    ].fillna("N/A")
    capecs = []
    for index, row in tqdm(
        clean_capec_df.iterrows(),
        desc="Writing CAPECs",
        colour="green",
        total=len(clean_capec_df.index),
    ):
        id = row["ID"]
        name = row["Name"]
        status = row["Status"]
        description = row["Description"]
        likelihood_of_attack = row["Likelihood Of Attack"]
        typical_severity = row["Typical Severity"]
        curr = Capec(
            capec_id=id,
            name=name,
            status=status,
            description=description,
            likelihood_of_attack=likelihood_of_attack,
            typical_severity=typical_severity,
        )
        capecs.append(curr)
    for capec in capecs:
        session.add(capec)
