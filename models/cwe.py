import pandas as pd
import glob

from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

path = "data/cwe"
csv_files = glob.glob(path + "/*.csv")

class Base(DeclarativeBase):
    pass


class Cwe(Base):
    __tablename__ = "surf_cwe"

    cwe_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(4000))

    def __init__(self, cwe_id, name, description) -> None:
        self.cwe_id = cwe_id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"(CWE ID: {self.cwe_id}) Name: {self.name} Desc: {self.description}\n\n"


def prepop_cwe_data(session):
    df_list = (pd.read_csv(file, index_col=False) for file in csv_files)
    # Concatenate all DataFrames
    raw_cwe_df = pd.concat(df_list, ignore_index=True)
    clean_cwe_df = raw_cwe_df[
        ["ID", "Name", "Status", "Description", "Related Weaknesses"]
    ].drop_duplicates(subset=["ID"]).fillna("N/A")
    cwes = []
    for index, row in clean_cwe_df.iterrows():
        id = row["ID"]
        name = row["Name"]
        description = row["Description"]
        curr = Cwe(cwe_id=id, name=name, description=description)
        cwes.append(curr)
    session.add_all(cwes)
