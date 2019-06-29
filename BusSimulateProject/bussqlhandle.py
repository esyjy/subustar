import pymssql

# Starting the connection for server
def start_server(_server, _user, _password, _database) :
    while True :
        try:
            conn = pymssql.connect(server = _server, user  = _user, password = _password, database = _database)
            return conn
        except Exception  as e :
            print(e)
            pass
conn = start_server('1.168.0.53:60000', 'cit', 'citcitcit', 'subustar')


query = '''
drop table if exists speed_table;

create table speed_table(
  speed int not null,
  time datetime primary key
);
insert into speed_table
values
(0, '2019-06-15 12:03:30')
'''

cursor = conn.cursor()
cursor.execute(query)
conn.commit()

query = "select * from speed_table"
cursor.execute(query)
row = cursor.fetchone()
print(row)

conn.close()