import sqlite3

# Higher order function to create instances of models
# when performing single table queries

# Rules for using model_factory: 
# Your SQL statement must query a single table
# each column in the table must be specified in the SQL.
def model_factory(model_type):
    def create(cursor, row):
        instance = model_type()
        smart_row = sqlite3.Row(cursor, row)
        # smart_row.keys allows you to access the row keys, equivalent to row["id"]
        for col in smart_row.keys():
            # col is only id 
            setattr(instance, col, smart_row[col])
        return instance
    return create