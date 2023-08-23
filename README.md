![SurfDB Logo](./static/SurfDB-Logo.png)

SurfDB is the database that will power the surfaceer application.

## Getting started 

### Prerequistes  
1. Install python version 3.6+
    ```sh
    python --version
    ```
2. Install mysql, mysql shell and mysql workbench (Optional)
    ```
    mysql --version 
    ```

### Installation 
1. Clone the repository 
    ```sh 
    git clone https://github.com/velac01/surfdb.git
    ```
2. Ensure you are in the correct directory 
    ```sh
    cd surfdb
    ```
2. Create a virtual environment (Recommended but Optional) 
    ```sh
    python -m venv ./env
    ```
3. Start the virtual environment 
    ```sh
    ./env/Scripts/Activate
    ```
4. Install the required modules 
    ```sh
    pip install -r ./requirements.txt
    ```
5. Add .env file to repository and add variables 
    ```dosini
    DB_USER_NAME=<DB_USER_NAME>
    DB_PASS_WORD=<DB_PASS_WORD>
    DB_URL=<DB_URL>
    DB_NAME=<DB_NAME>
    ```
### Prepopulate the database 
- Be sure have run the surfdb DDL before running the following command
- Adding data to the database can be done by running the following command 
    ```sh
    python main.py
    ```
- Confirm the data has been prepoulated by going into the DB

## TODOS
- Create the SQL Connection (Done)
- Install sqlalchemy (Done)
- Create the Models for surf tables (Done) 
- Insert the CAPEC Information (Done)
- Insert the CWE Information (Done)
- Insert the CWE/CAPEC Mapping (Done)
- Refactor db.py to be it's own module (Done)
- Add all the CWEs - Use pandas to drop duplicate IDs when reading in all the CWE csv files (Done)
- Refactor! This will be good for Austin :) 
