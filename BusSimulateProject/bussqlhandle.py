import pymssql
import datetime

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

#tname = tablename, consts = constraints
#테이블 만드는 함수
def create(conn, tname, domain, types, consts) :
    cursor = conn.cursor()
    query = 'drop table if exists ' + tname+";"
    query += "create table "+tname+"("
    for i in range(len(domain)) :
        query += domain[i] +" "+ types[i] +" "+ consts[i] + ","
    query = query[:-1] + ");"
    cursor.execute(query)
    conn.commit()
    return

#테이블 보는 함수
def select(conn, cols, tname) :
    cursor = conn.cursor()
    query = "select "
    for i in range(len(cols)) :
        query += cols[i] +", "
    query = query[:-2] + " from "+tname+";"
    cursor.execute(query)
    return cursor.fetchall()

#테이블에 값을 추가하는 함수
def insert(conn, tname, value) :
    cursor = conn.cursor()
    query = "insert into "+tname+" values("
    for i in range (len(value)) :
        query += value[i]+", "
    query = query[:-2] +")"
    cursor.execute(query)
    conn.commit()
    return

#테이블에 있는 특정한 값을 없애는 함수
def delete(conn, tname, field, value) :
    cursor = conn.cursor()
    query = "delete from "+tname+" where "+field+"="+value+";"
    cursor.execute(query)
    conn.commit()
    return

#2019-07-20 00:50:30.440
if __name__ == "__main__" :
    '''
    conn = start_server()
    create(conn, "test_table", ["a", "b"], ["int", "int"], ["not null", "primary key"])
    insert(conn, "speed_table", ["60", "'"+str(datetime.datetime.now())[:-3]+"'", "60"])
    select(conn, ["speed", "time"], "speed_table")
    delete(conn, "speed_table", "speed", "60")
    '''