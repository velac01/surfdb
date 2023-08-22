from tqdm import tqdm
import pandas as pd

from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

data = "data/3000.csv"


class Base(DeclarativeBase):
    pass


class CapecCweMap(Base):
    __tablename__ = "surf_capec_cwe_map"

    capec_cwe_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    capec_id: Mapped[int] = mapped_column(Integer)
    cwe_id: Mapped[int] = mapped_column(Integer)

    def __init__(self, capec_id, cwe_id) -> None:
        self.capec_id = capec_id
        self.cwe_id = cwe_id

    def __repr__(self):
        return f"(CAPEC ID: {self.capec_id}) | (CWE ID: {self.cwe_id})\n\n"


def prepop_capec_cwe_data(session):
    raw_capec_df = pd.read_csv(data, index_col=False)
    clean_capec_df = raw_capec_df[["ID", "Related Weaknesses"]]
    ccms = []
    for index, row in tqdm(
        clean_capec_df.iterrows(),
        desc="Writing CAPEC CWE Map",
        colour="green",
        total=len(clean_capec_df.index),
    ):
        id = row["ID"]
        rws = row["Related Weaknesses"]
        if not pd.isna(rws):
            rws = rws.split("::")
            rws = [i for i in rws if i != ""]
            for rw in rws:
                curr = CapecCweMap(capec_id=id, cwe_id=rw)
                ccms.append(curr)
        session.add_all(ccms)
    
