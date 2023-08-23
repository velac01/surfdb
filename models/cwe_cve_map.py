import re
import glob
from tqdm import tqdm

import pandas as pd

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


path = "data/cwe"
csv_files = glob.glob(path + "/*.csv")


class Base(DeclarativeBase):
    pass


class CweCveMap(Base):
    __tablename__ = "surf_cwe_cve_map"

    cwe_cve_map_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    cwe_id: Mapped[int] = mapped_column(Integer)
    cve_id: Mapped[str] = mapped_column(String)

    def __init__(self, cwe_id, cve_id) -> None:
        self.cwe_id = cwe_id
        self.cve_id = cve_id

    def __repr__(self):
        return f"(CWE ID: {self.cwe_id}) | (CVE ID: {self.cve_id})\n\n"

    def __eq__(self, other):
        return self.cwe_id == other.cwe_id and self.cve_id == other.cve_id


def is_valid_cve(cve_string):
    """
    Returns True if the given string is in a valid CVE format, False otherwise.

    Args:
      cve_string: The string to check.

    Returns:
      True if the string is in a valid CVE format, False otherwise.
    """

    cve_regex = r"CVE-(1999|2\d{3})-(0\d{2}[1-9]|[1-9]\d{3,})$"
    if not re.match(cve_regex, cve_string):
        return False
    return True


def prepop_cwe_cve_data(session):
    df_list = (pd.read_csv(file, index_col=False) for file in csv_files)
    raw_cwe_df = pd.concat(df_list, ignore_index=True)
    clean_cwe_df = raw_cwe_df[["ID", "Observed Examples"]]
    ccms = []
    for index, row in tqdm(
        clean_cwe_df.iterrows(),
        desc="Writing CWE CVE Map",
        colour="green",
        total=len(clean_cwe_df.index),
    ):
        id = row["ID"]
        oes = row["Observed Examples"]
        if not pd.isna(oes):
            oes = oes.split("::")
            oes = [i for i in oes if i != ""]
            for str in oes:
                lstr = str.split(":")
                for word in lstr:
                    if is_valid_cve(word):
                        curr = CweCveMap(cwe_id=id, cve_id=word)
                        if curr not in ccms:
                            print("Hi")
                            ccms.append(curr)
                        continue
    session.add_all(ccms)
