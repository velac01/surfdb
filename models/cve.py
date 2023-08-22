import gzip
import json
from io import BytesIO
import requests


import pandas as pd 

from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

JSON_DATA = "../data/nvdcve-1.1-2021.json.gz"


class Base(DeclarativeBase):
    pass


class Cve(Base):
    __tablename__ = "surf_cve"
    cve_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String(4000))
    cvss3_score: Mapped[float] = mapped_column(Float)
    cvss2_score: Mapped[float] = mapped_column(Float)

    def __init__(self, cve_id, description, cvss3_score, cvss2_score) -> None:
        self.cve_id = cve_id
        self.description = description
        self.cvss3_score = cvss3_score
        self.cvss2_score = cvss2_score

    def __repr__(self):
        return f"(CVE ID: {self.cve_id}) | Desc: {self.description} | CVSSv3: {self.cvss3_score} | CVSSv2: {self.cvss2_score}\n\n"


if __name__ == "__main__":
    with gzip.open(JSON_DATA, 'r') as f:
        raw = f.read()
    items = json.loads(raw.decode('utf-8'))["CVE_Items"]
    for i in range(10):
        curr_cve = items[i]
        curr_cve_id = curr_cve["cve"]["CVE_data_meta"]["ID"]
        print(curr_cve_id)
        curr_cve_description = curr_cve["cve"]["description"]["description_data"][0]["value"]
        # Parse Rejects
        if "** REJECT **" in curr_cve_description: 
            print("REJECT")
            continue
        impact = curr_cve.get("impact")
        if impact != {}:
            curr_cve_cvss3 = curr_cve["impact"]["baseMetricV3"]["cvssV3"]["baseScore"]
            curr_cve_cvss2 = curr_cve["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]
        else:
            curr_cve_cvss3, curr_cve_cvss2 = None, None
        print(
            Cve(
                cve_id=curr_cve_id,
                description=curr_cve_description,
                cvss3_score=curr_cve_cvss3,
                cvss2_score=curr_cve_cvss2
            )
        )
