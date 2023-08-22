import gzip
import json
from io import BytesIO
import requests

from tqdm import tqdm

from sqlalchemy import String, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


JSON_DATA = "../data/nvdcve-1.1-2021.json.gz"


class Base(DeclarativeBase):
    pass


class Cve(Base):
    __tablename__ = "surf_cve"
    cve_id: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[str] = mapped_column(String(4000))
    cvss3_score: Mapped[float] = mapped_column(Float)
    cvss2_score: Mapped[float] = mapped_column(Float)

    def __init__(self, cve_id, description, cvss3_score, cvss2_score) -> None:
        self.cve_id = cve_id
        self.description = description
        self.cvss3_score = cvss3_score
        self.cvss2_score = cvss2_score

    def __repr__(self):
        return f"(CVE ID: {self.cve_id}) | Desc: {self.description} \nCVSSv3: {self.cvss3_score} | CVSSv2: {self.cvss2_score}\n\n"

def load_cve_json_by_year(year):
    if int(year) > 2023 or int(year) < 1999: 
        print("Invalid Year")
        exit()
    JSON_DATA = f"data/cve/nvdcve-1.1-{year}.json.gz"
    with gzip.open(JSON_DATA, "r") as f:
        raw = f.read()
    cve_data = json.loads(raw.decode("utf-8"))["CVE_Items"]
    return cve_data
    
def prepop_cve_data(year, session):
    items = load_cve_json_by_year(year)
    # Working for 10
    for i in tqdm(range(len(items)), desc=f"Writing CVEs from year {year}", colour="green"):
        curr_cve = items[i]
        curr_cve_id = curr_cve["cve"]["CVE_data_meta"]["ID"]
        curr_cve_description = curr_cve["cve"]["description"]["description_data"][0][
            "value"
        ]
        # Parse Rejects
        if "** REJECT **" in curr_cve_description:
            # print("REJECT")
            continue
        impact = curr_cve.get("impact")
        if impact != {}:
            curr_cve_cvss3 = impact.get("baseMetricV3")
            curr_cve_cvss2 = impact.get("baseMetricV2")
            if curr_cve_cvss3 is not None: 
                curr_cve_cvss3 = curr_cve_cvss3["cvssV3"]["baseScore"]
            if curr_cve_cvss2 is not None: 
                curr_cve_cvss2 = curr_cve_cvss2["cvssV2"]["baseScore"]
        else:
            curr_cve_cvss3, curr_cve_cvss2 = None, None
        session.add(
            Cve(
                cve_id=curr_cve_id,
                description=curr_cve_description,
                cvss3_score=curr_cve_cvss3,
                cvss2_score=curr_cve_cvss2,
            )
        )
    session.commit()


if __name__ == "__main__":
    years = ["2021", "2022", "2023"]
    for year in years: 
        cve_data = load_cve_json_by_year(year)
        print("\n")
        for i in tqdm(range(len(cve_data)), desc=f"Parsing CVE for {year}"):
            curr_cve = cve_data[i]
            curr_cve_id = curr_cve["cve"]["CVE_data_meta"]["ID"]
            curr_cve_description = curr_cve["cve"]["description"]["description_data"][0][
                "value"
            ]
            # Parse Rejects
            if "** REJECT **" in curr_cve_description:
                # print("REJECT")
                continue
            impact = curr_cve.get("impact")
            if impact != {}:
                curr_cve_cvss3 = impact.get("baseMetricV3")
                curr_cve_cvss2 = impact.get("baseMetricV2")
                if curr_cve_cvss3 is not None: 
                    curr_cve_cvss3 = curr_cve_cvss3["cvssV3"]["baseScore"]
                if curr_cve_cvss2 is not None: 
                    curr_cve_cvss2 = curr_cve_cvss2["cvssV2"]["baseScore"]
            else:
                curr_cve_cvss3, curr_cve_cvss2 = None, None
            # print(
            #     Cve(
            #         cve_id=curr_cve_id,
            #         description=curr_cve_description,
            #         cvss3_score=curr_cve_cvss3,
            #         cvss2_score=curr_cve_cvss2,
            #     )
            # )
