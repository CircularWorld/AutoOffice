import pymysql

db =pymysql.connect('127.0.0.1','root','123456','AutoOffice',charset='utf8')
cur = db.cursor()

ins = 'insert into user_userprofile (username,nickname,password,phone,company_id)values(%s,%s,%s,%s,%s)'

userlist = [
    ('张小兰%s'% i,'icerain%s'%i,'81dc9bdb52d04dc20036dbd8313ed055','12312311222',2) for i in range(1,20)
]

print(userlist)
cur.executemany(ins,userlist)
db.commit()
cur.close()
db.close()

