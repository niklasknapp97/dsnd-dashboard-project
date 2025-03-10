from sqlite3 import connect, DatabaseError
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file
db_path = Path(__file__).parent / "employee_events.db"


# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    def pandas_query(self, sql_query: str):
        """Execute an SQL query and return the result as a Pandas DataFrame."""
        with connect(db_path) as connection:
            return pd.read_sql_query(sql_query, connection)

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    def query(self, sql_query: str):
        """Execute an SQL query and return the result as a list of tuples."""
        with connect(db_path) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            return cursor.fetchall()
    

# Decorator to handle database connections
def query(func):
    """
    Decorator that runs a standard SQL execution
    and returns a list of tuples.
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)  # Get the SQL query string
        try:
            with connect(db_path) as connection:
                cursor = connection.cursor()
                cursor.execute(query_string)
                return cursor.fetchall()
        except DatabaseError as e:
            print(f"Database error: {e}")
            return None

    return run_query
