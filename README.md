![SurfDB Logo](./static/SurfDB-Logo.png)

SurfDB is the database that will power the surfaceer application.

## Getting started, below there will be a Windows version of instructions
## as well as a MAC version of instructions please follow them accordingly

### Prerequistes (Windowns Version)
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
5. Add .env file to the repository and add variables 
    ```dosini
    DB_USER_NAME=<DB_USER_NAME>
    DB_PASS_WORD=<DB_PASS_WORD>
    DB_URL=<DB_URL>
    DB_NAME=<DB_NAME>
    ```

### Prerequistes (MAC Version) 
### You can use Homebrew, pip or pipx, whichever you prefer!
1. Install python version 3.6+
    ```sh
    brew install python3 
    ```
2. Install mysql, mysql shell and mysql workbench (Optional)
    ```
    brew install mysql
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
2. Install virtualenv (Recommended but Optional) 
    ```sh
    brew install virtualenv
    ```
3. Start the virtual environment 
    ```sh
    source ./env/bin/Activate
    ```
4. Install the required modules 
    ```sh
    brew install -r ./requirements.txt
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
- Add all the CWEs - Use pandas to drop duplicate IDs when reading in all the CWE csv files (Done)
- Refactor! This will be good for Austin :
