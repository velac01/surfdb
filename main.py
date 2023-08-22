from time import sleep, perf_counter

from db import create_session, start_engine
from models import prepop_capec_data
from models import prepop_cwe_data
from models import prepop_capec_cwe_data
from models import prepop_cwe_cve_data
from models import prepop_cve_data

if __name__ == "__main__":
    print("SurfDB Initiating...")
    sleep(2)

    t1 = perf_counter()
    
    print("Connecting to DB....")
    eng = start_engine()
    session = create_session(eng)
    print(session)
    print("Connected to DB!")
    sleep(1)
    
    print("Beginning Initiation...")
    # CAPECs
    print("Prepopulating CAPECs...")
    prepop_capec_data(session)
    print("\n\nCAPECs added")

    sleep(2)

    # CWEs
    print("Prepopulating CWEs...")
    prepop_cwe_data(session)
    print("\n\nCWEs added")

    session.commit()

    # CVEs
    print("Prepopulating CVEs")
    year = 2002
    while(year <= 2023):
        prepop_cve_data(year, session)
        year = year + 1
    print("CVEs added")
    sleep(2)

    print("Added Structure Tables...")
    sleep(3)
    print("Adding mapping tables...")

    #  CAPEC CWE MAP
    print("Prepopulating CAPEC and CWE mapping...")
    prepop_capec_cwe_data(session)
    print("\n\nCAPECs and CWE mapping added")
    sleep(2)

    # CWE CVE MAP
    print("Prepopulating CWE and CAPEC mapping ...")
    prepop_cwe_cve_data(session)
    print("\n\nCWE and CVE mapping added")

    session.commit()
    session.close()

    t2 = perf_counter()

    print(f"\n\nSurfDB Populated in {t2 - t1:0.4f} Seconds!")
