import happybase
import sys
import csv
import time

# The families argument is a dictionary mapping column family names to a dictionary containing
# the options for this column family, e.g.
# Format type:
# families = {
#       '2013-12-01': dict(),
#       '2013-12-02': dict(),
#       '2013-12-03': dict(),
#        ...
#        ...
# }
def generate_families_dict():
    global time
    with open(path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        family_rows = dict()
        dates = []

        print ("Starting to create table and families:")
        time.sleep(5)

        for row in csv_reader:
            print(row)
            date = row[1].split(" ", 1)[0]
            if date not in dates:
                family_rows[date] = dict()
                dates.append(date)
        return family_rows

def generate_rowkey_column(columns, rows):
    global time
    try:
        dateset_table = connection.table('dataset')
    except Exception, e:
        print e
    else:
        print("Starting to store data on the database:")
        time.sleep(5)
        for row in range(int(rows)):
            with open(path, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                count = 1
                for row_csv in csv_reader:
                    sensor = str(int(row)+1) + str(row_csv[0])
                    date = row_csv[1].split(" ", 1)[0]
                    time = row_csv[1].split(" ", 1)[1]
                    measure = row_csv[2].strip()
                    count += 1
                    list_measures = []
                    for column in range(int(columns)):
                        list_measures.append(measure)
                    
                    column_value = dict()
                    column_value[date + ':' + time] =  ','.join(list_measures)
                    print ("Row number CSV: " + str(count) + " with values: " + sensor + " " + date + " " + time+ " " + ','.join(list_measures))

                    # put(row, data, timestamp=None, wal=True)
                    # Store data in the table.
                    # This method stores the data in the data argument for the row specified by row. The data argument is dictionary that maps columns to values. Column names must include a family and qualifier part, e.g. b'cf:col', though the qualifier part may be the empty string, e.g.
                    # DG1056626''2013-12-31 17:10':110.449997
                    # ROWKEY: sensor
                    # COLUMN FAMILY: date
                    # COLUMN KEY: time
                    # COLUMN VALUE: measures
                    # https://happybase.readthedocs.io/en/latest/api.html#happybase.Table.put
                    dateset_table.put(sensor, column_value)

        print("\n\n\n\n\nThe table DATASET has been created succesfully.")

if __name__ == "__main__":
    try:
        sys.argv[1]
    except IndexError:
        print("The path file must be introduced as part of the arguments")
        sys.exit(0)

    try:
        sys.argv[2]
    except IndexError:
        print("The number of rows must be introduced as part of the arguments")
        sys.exit(0)

    try:
        sys.argv[3]
    except IndexError:
        print("The number of columns must be introduced as part of the arguments")
        sys.exit(0)

    rows = sys.argv[2]
    columns = sys.argv[3]
    path = sys.argv[1]

    #Connection to an HBase Thrift server.
    # The host and port arguments specify the host name and TCP port of the HBase Thrift server to connect to.
    # Parameters:	
        # host (str) - The host to connect to
        # port (int) - The port to connect to
        # timeout (int) - The socket timeout in milliseconds (optional)
        # autoconnect (bool) - Whether the connection should be opened directly
    # https://happybase.readthedocs.io/en/latest/api.html#connection
    connection = happybase.Connection('localhost', timeout=None, autoconnect=True)
    # Open the underlying transport to the HBase instance.
    # This method opens the underlying Thrift transport (TCP connection).
    # https://happybase.readthedocs.io/en/latest/api.html#happybase.Connection.open
    connection.open()

    # Return a list of table names available in this HBase instance.
    # If a table_prefix was set for this Connection, only tables that have the specified prefix will be listed.
    # Returns:	The table names
    # Return type:	List of strings
    # https://happybase.readthedocs.io/en/latest/api.html#happybase.Connection.tables
    tables = connection.tables()

    if len(tables) > 0 and "dataset" in tables:
        print("The table DATASET already existed")
        sys.exit(0)
    else:
        families = generate_families_dict()
        # Create a table.
        # Parameters:       
        # name (str) - The table name
        # families (dict) - The name and options for each column family
        # https://happybase.readthedocs.io/en/latest/api.html#happybase.Connection.create_table
        connection.create_table(
            'dataset', families
        )
        generate_rowkey_column(columns, rows)


