import happybase
import sys
import csv
import time
import collections

# Retrieve the column families for this table.
# Returns:	Mapping from column family name to settings dict
# Return type:	dict
# https://happybase.readthedocs.io/en/latest/api.html#happybase.Table.families
def get_families(table):
    tables = table.families()
    # Sort dates
    # https://stackoverflow.com/questions/3977310/sorting-a-dictionary-with-date-keys-in-python
    family_sorted = collections.OrderedDict(sorted(tables.items(), key=lambda t: t[0]))
    return family_sorted

# scan(row_start=None, row_stop=None, row_prefix=None, columns=None, filter=None, timestamp=None..
# Create a scanner for data in the table.
# This method returns an iterable that can be used for looping over the matching rows.
# Returns: generator yielding the rows matching the scan
# Return type: iterable of (row_key, row_data) tuples
# https://happybase.readthedocs.io/en/latest/api.html#happybase.Table.scan
def get_table_tuple(table, family):
    return table.scan(columns=[family], sorted_columns=True)

# row(row, columns=None, timestamp=None, include_timestamp=False)
# Retrieve a single row of data.
# Returns: Mapping of columns (both qualifier and family) to values
# Return type: dict
# https://happybase.readthedocs.io/en/latest/api.html#happybase.Table.row
def get_header(table, row, family):

    columns = table.row(row, columns=[family]).items()
    column_dates = [item[0].split(":", 1)[1] for item in columns]
    column_dates.sort()
    # 00:00 00:10 00:20 00:30 00:40 00:50..
    return "Sensor" + ",Dates," + ",".join(column_dates)

def get_tables(connection):
    # Return a list of table names available in this HBase instance.
    # If a table_prefix was set for this Connection, only tables that have the specified prefix will be listed.
    # Returns: The table names
    # Return type: List of strings
    # https://happybase.readthedocs.io/en/latest/api.html#happybase.Connection.tables
    tables = connection.tables()
    return tables

def create_file(name):
    return open(name + ".csv","w")

def get_table_by_name(connection, name):
    # table(name, use_prefix=True)
    # Return a table object.
    # Returns a happybase.Table instance for the table named name. This does not result in a round-trip to the server, and the table is not checked for existence.
    # Parameters:	
        # name (str) the name of the table
        # use_prefix (bool) whether to use the table prefix (if any)
    return connection.table(name)

if __name__ == "__main__":
    try:
        sys.argv[1]
    except IndexError:
        print("The number of rows must be introduced as part of the arguments")
        sys.exit(0)

    try:
        sys.argv[2]
    except IndexError:
        print("The number of columns must be introduced as part of the arguments")
        sys.exit(0)

    rows = sys.argv[1]
    columns = int(sys.argv[2])

    connection = happybase.Connection('localhost', timeout=None, autoconnect=True)
    connection.open()

    tables = get_tables(connection)

    if len(tables) > 0 and "dataset" in tables:
        table = get_table_by_name(connection, 'dataset')
        # 2013-12-01
        # 2013-12-03
        # 2013-12-02
        # 2013-12-05
        families = get_families(table)
        file_row = []
        header = get_header(table,'1DG1000420', families.items()[0][0])
        for family in families:
            file_path = create_file('/script/csv/output')
            # https://github.com/python-happybase/happybase/issues/12
            for sensor, column_family in get_table_tuple(table, family):
                if sensor.startswith(str(rows)):
                    measures_pos = []
                    for measures in table.cells(sensor, family):
                        measures = measures.split(",")
                    	if columns > len(measures):
                            	print("You are requesting a column which has not been created previously on create table")
                        	sys.exit(0)
                    	measures_pos.append(measures[columns-1])
                    file_row.append(sensor.replace(rows,"",1) + "," + family + "," + ",".join(measures_pos))
        file_row.sort()
        if len(file_row) == 0:
            print("You are requesting a row which has not been created previously on create table")
            sys.exit(0)
        
        if file_row is not None:
            print ("Starting to export the DB on a CSV file:")
            time.sleep(5)
<<<<<<< HEAD
            file_path.write('Sensor,' + 'Date,' + column_family.split(",") + '\n')
=======
            file_path.write(header + '\n')
>>>>>>> 75280e5106f004336f934b571078076b27948d24
            for line in file_row:
                print("CSV Row: " + line + '\n')
                file_path.write(line + '\n')
        file_path.close()