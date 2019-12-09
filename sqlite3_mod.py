import sqlite3,config

data_base = config.data_base

def create_table():
    con = sqlite3.connect(data_base)
    cu = con.cursor()
    cu.execute('create table rules (rules str not null,process str not null,ip str not null,time int not null,version str not null)')
    con.commit()
    cu.close()
    con.close()

def insert_data(rules,process,ip,time,version):
    con = sqlite3.connect(data_base)
    cu = con.cursor()
    cu.execute("insert into rules(rules,process,ip,time,version) values(\"%s\",\"%s\",\"%s\",\"%d\",\"%s\")" %(rules,process,ip,time,version))
    con.commit()
    cu.close()
    con.close()

def delete_data(i):
    con = sqlite3.connect(data_base)
    cu = con.cursor()
    data = cu.execute("delete from rules where time = {}".format(i))
    con.commit()
    cu.close()
    con.close()

if __name__ == '__main__':
    #create_table()
    #insert_data('dsafas','fdsafas',23124.1234)
