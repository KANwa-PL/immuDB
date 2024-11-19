from immudb import ImmudbClient
from faker import Faker

URL = "localhost:3322"  # immudb running on your machine
LOGIN = "immudb"  # Default username
PASSWORD = "immudb"  # Default password
DB = b"defaultdb"  # Default database name (must be in bytes)

def drop(client, table_name):
    try:
        client.sqlExec(f"""DROP TABLE {table_name};""")
    except:
        print(f"Can't drop. Table {table_name} does not exist...")


def create(client, table_name):
    try:
        client.sqlExec(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER AUTO_INCREMENT, 
                account_number VARCHAR[24] NOT NULL, 
                account_name VARCHAR[32],
                iban VARCHAR[28],
                address VARCHAR[64],
                amount FLOAT,
                type VARCHAR[10],
                PRIMARY KEY (id)
            );""")
    except:
        print(f"Error occurred. Couldn't create {table_name} table...")


def insert(client, table_name, transaction: dict):
    columns = ",".join(transaction.keys())
    values = ",".join(("'" + str(x) + "'") for x in transaction.values())
    client.sqlExec(f"""INSERT INTO {table_name} ({columns}) VALUES ({values});""")


def create_transactions(count):
    transactions = []
    faker = Faker(locale='pl_PL')
    for i in range(count):
        transaction = {}
        transaction.update({"account_number":faker.bban()})
        transaction.update({"account_name":str(faker.first_name() + " " + faker.last_name())})
        transaction.update({"iban":faker.iban()})
        transaction.update({"address":faker.address()})
        transaction.update({"amount":faker.random_number()})
        transaction.update({"type": faker.random_element(elements= ['sending', 'receiving'])})
        transactions.append(transaction)
    return transactions


def main():
    # Create a client instance...
    client = ImmudbClient(URL)
    client.login(LOGIN, PASSWORD, database=DB)

    # Drop existing table and create new table from scratch...
    drop(client, "Operations")
    create(client, "Operations")

    # Create n transactions
    transactions = create_transactions(110)

    # Insert predefined transactions into a table...
    for transaction in transactions:
        insert(client, table_name="Operations", transaction=transaction)

if __name__ == "__main__":
    main()
