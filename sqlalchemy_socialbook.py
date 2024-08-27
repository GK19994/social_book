from sqlalchemy import create_engine, MetaData, Table, select
import os

# Assuming you're using environment variables to store your DB credentials
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://gaurav:root@localhost:5432/mydb')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Example function to fetch data from a PostgreSQL table using SQLAlchemy
def fetch_data():
    # Create a connection
    with engine.connect() as connection:
        # Reflect the table you want to query
        metadata = MetaData()
        my_table = Table('accounts_customuser', metadata, autoload_with=engine)
        
        # Build a SELECT query
        query = select(my_table)

        # Execute the query and fetch the data
        result = connection.execute(query)

        # Print out the fetched data
        for row in result:
            print(row)

# Example usage
if __name__ == "__main__":
    fetch_data()
