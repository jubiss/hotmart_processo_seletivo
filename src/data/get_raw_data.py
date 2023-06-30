import mysql.connector
import pandas as pd

def get_data():
    # Create a connection to the database
    cnx = mysql.connector.connect(
        host='interview-2.ck1h5ksgzpiq.us-east-1.rds.amazonaws.com',
        port=3306,
        user='hotinterview',
        password='6cT4jk9QWPhQC9KXWKDd',
        database='innodb'
    )

    # Create a cursor object to interact with the database
    cursor = cnx.cursor()

    # Execute a sample query to get the column names
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'sales_data'"
    cursor.execute(query)

    # Fetch all column names from the result
    columns = [column[0] for column in cursor.fetchall()]

    # Execute a query to fetch the table data
    query = "SELECT * FROM sales_data"
    cursor.execute(query)

    # Fetch all rows from the result
    rows = cursor.fetchall()

    # Transform in Dataframe
    df = pd.DataFrame(rows, columns=columns)
    # Save table data to a CSV file

    df.to_csv(r'\data\raw\sales_data.csv')
    # Close the cursor and connection
    cursor.close()
    cnx.close()

if __name__ == "__main__":
    get_data()