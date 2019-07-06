import pymssql

# Starting the connection for server
def start_server(_server='1.168.0.53:60000', _user='cit',
                 _password='citcitcit', _database='subustar') :
    while True :
        try:
            conn = pymssql.connect(server = _server, user  = _user, password = _password, database = _database)
            return conn
        except Exception  as e :
            print(e)
            pass

def init_table(conn, cursor, tablename):
    query='drop table if exists '+tablename
    if tablename == "speed_table":
        query += '''
        create table speed_table(
          speed int not null,
          time datetime primary key,
          people int not null
        );
        '''
    elif tablename == "student_table":
        query += '''
        create table student_table(
            id nvarchar(50) primary key,
            pw nvarchar(50) not null,
            attendance nvarchar(50) not null,
            name nvarchar(20) not null
        );
        '''
    cursor.execute(query)
    conn.commit()
    return

'''
query = "select * from speed_table"
cursor.execute(query)
row = cursor.fetchone()
print(row)
conn.close()
'''