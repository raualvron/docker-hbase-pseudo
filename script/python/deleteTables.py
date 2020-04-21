import happybase
try:
    connection = happybase.Connection('localhost', timeout=None, autoconnect=True)
except Exception, e:
    print e
else:
    # Open the underlying transport to the HBase instance.
    # This method opens the underlying Thrift transport (TCP connection).
    # https://happybase.readthedocs.io/en/latest/api.html#happybase.Connection.open
    connection.open()
    tables = connection.tables()
    for t in tables:
        # disable_table(name)
        # Disable the specified table.
        # Parameters: name (str) - The table name
        # https://happybase.readthedocs.io/en/latest/api.html#happybase.Connection.disable_table
        connection.disable_table(t)

        # Delete the specified table.
        # New in version 0.5: disable argument
        # In HBase, a table always needs to be disabled before it can be deleted. If the disable argument is True, this method first disables the table if it wasnt already and then deletes it.
        # https://happybase.readthedocs.io/en/latest/api.html#happybase.Connection.delete_table
        connection.delete_table(t)
        print (t + " deleted")