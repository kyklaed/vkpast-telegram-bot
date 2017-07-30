
import mysql.connector

class Addconfig:
    def __init__(self,database,table):
        self.connection = mysql.connector.connect(host="localhost", user='root', passwd='Cgbhn96%', db=database,
                                                  charset='utf8')
        self.cursor = self.connection.cursor()
        self.table = table

    def addtable(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS `%s` (
	`id` INTEGER(20) NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`city` VARCHAR(40),
	`mygroupid` INTEGER(20),
	`wheregroup` VARCHAR(250),
	`uservk` VARCHAR(40),
	`passvk` VARCHAR(40),
	`nametablelinks` VARCHAR(40),
	`spamtext`VARCHAR(400))""",(self.table, ))


    def addcitygroup(self,city):
        self.cursor.execute("INSERT INTO `%s` (`city`) VALUES (%s)",(self.table,city,))
        self.cursor.fetchone()
        self.connection.commit()

    def udate_nametablelinks(self,city):
        id_t=city+str(self.table)
        #id_t = city + "{0}".format(self.table,)
        self.cursor.execute("UPDATE `%s` SET nametablelinks = %s WHERE city = %s",(self.table,id_t,city ))
        self.cursor.fetchone()
        self.connection.commit()

    def addmygroup(self,mygroupid,city):
        self.cursor.execute("UPDATE `%s` SET mygroupid = %s WHERE city = %s",(self.table,mygroupid,city ))
        self.cursor.fetchone()
        self.connection.commit()

    def addwheregroup(self,wheregroup,city):
        self.cursor.execute("UPDATE `%s` SET wheregroup = %s WHERE city = %s",(self.table,wheregroup,city ))
        self.cursor.fetchone()
        self.connection.commit()

    def addspamuser(self,uservk,city):
        self.cursor.execute("UPDATE `%s` SET uservk = %s WHERE city = %s",(self.table,uservk,city ))
        self.cursor.fetchone()
        self.connection.commit()

    def addspampassword(self,passvk,city):
        self.cursor.execute("UPDATE `%s` SET passvk = %s WHERE city = %s",(self.table,passvk,city ))
        self.cursor.fetchone()
        self.connection.commit()

    def addspamtext(self,spamtext,city):
        self.cursor.execute("UPDATE `%s` SET spamtext = %s WHERE city = %s",(self.table,spamtext,city ))
        self.cursor.fetchone()
        self.connection.commit()

    def close(self):
        self.connection.close()

class Getconfig:
    def __init__(self,database,table):
        self.connection = mysql.connector.connect(host="localhost", user='root', passwd='Cgbhn96%', db=database,
                                                  charset='utf8')
        self.cursor = self.connection.cursor()
        self.table = table

    def get_config(self,city):
        self.cursor.execute('SELECT mygroupid, wheregroup,uservk,passvk,nametablelinks,city FROM `%s` WHERE city = %s',(self.table,city))
        return self.cursor.fetchone()

    def get_city_list(self):
        self.cursor.execute('SELECT city FROM `%s`',(self.table,))
        return self.cursor.fetchall()


class Addlinks:
    def __init__(self,database,table):
        self.connection = mysql.connector.connect(host="localhost", user='root', passwd='Cgbhn96%', db=database,
                                                  charset='utf8')
        self.cursor = self.connection.cursor()
        self.table = table

    def addtablelinks(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS {0} (
        `id` INTEGER(20) NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `linkuser` VARCHAR(100) NOT NULL,
        `linkpost` VARCHAR(100) NOT NULL,
        `datapost` VARCHAR(100),
        `mylinkpost` VARCHAR(100))""".format(self.table, ))


    def insert_db(self, val, val1):
        self.cursor.execute(
            "INSERT INTO {0} (`linkuser`, `linkpost`) VALUES (%s,%s)".format(self.table,),(val, val1))
        #self.cursor.fetchall()
        self.cursor.fetchone()
        self.connection.commit()

    def select_maxid(self):
        self.cursor.execute('SELECT max(id) FROM {0}'.format(self.table,))
        return self.cursor.fetchall()[0][0]

    def update_maxid(self, datapost, mylink, idmax):
        self.cursor.execute("UPDATE {0} SET datapost = %s, mylinkpost = %s WHERE id= %s".format(self.table,),(datapost, mylink, idmax))
        self.connection.commit()

    #def check_none(self, id_user):
        #self.cursor.execute("SELECT datapost FROM {0} WHERE linkuser = {1}".format(self.table,id_user))

    def delete_null(self,id_user):
        self.cursor.execute("DELETE FROM {0} WHERE linkuser = '{1}' and datapost is Null".format(self.table,id_user))
        self.connection.commit()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()



class Check_black_list:
    def __init__(self,database,table):
        self.connection = mysql.connector.connect(host="localhost", user='root', passwd='Cgbhn96%', db=database,
                                                  charset='utf8')
        self.cursor = self.connection.cursor()
        self.table = table

    def table_blacklist(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS {0} (
                `id` INTEGER(20) NOT NULL PRIMARY KEY AUTO_INCREMENT,
                `iduser` VARCHAR(100) NOT NULL)""".format(self.table,))

    def blacklist(self,id_user):
        self.cursor.execute('SELECT iduser FROM {0} WHERE iduser = "{1}"'.format(self.table, id_user))
        return self.cursor.fetchone()

    def add_id_to_blacklist(self,val):
        self.cursor.execute("INSERT INTO {0} (`iduser`) VALUES ({1})".format(self.table,val))
        self.cursor.fetchone()
        self.connection.commit()


class Check_spam_message:
    def __init__(self,database,table):
        self.connection = mysql.connector.connect(host="localhost", user='root', passwd='Cgbhn96%', db=database,
                                                  charset='utf8')
        self.cursor = self.connection.cursor()
        self.table = table

    def show_table(self):
        self.cursor.execute('SHOW TABLES')
        return self.cursor.fetchall()

    def use_spamtext(self,nametablelinks):
        self.cursor.execute('SELECT spamtext FROM `%s` WHERE nametablelinks = %s',(self.table,nametablelinks))
        return self.cursor.fetchall()


    def find_userid(self):
        self.cursor.execute(
            'SELECT linkuser,datapost,mylinkpost FROM {0} WHERE datapost = UNIX_TIMESTAMP(NOW()- SECOND(NOW()))'.format(self.table,))
        return self.cursor.fetchone()

    def count_userid(self,iduser):
        self.cursor.execute(
                'SELECT count(*) FROM {0} WHERE linkuser= %s'.format(self.table,),(iduser,))
        return self.cursor.fetchall()


class Random_vkpass:
    def __init__(self,database,table):
        self.connection = mysql.connector.connect(host="localhost", user='root', passwd='Cgbhn96%', db=database,
                                                  charset='utf8')
        self.cursor = self.connection.cursor()
        self.table = table

    def table_loginpass(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS {0} (
        `id` INTEGER(20) NOT NULL PRIMARY KEY AUTO_INCREMENT,
        `login` VARCHAR(100) NOT NULL,
        `pass` VARCHAR(100) NOT NULL)""".format(self.table, ))

    def set_loginpass(self,login,passs):
        self.cursor.execute("INSERT INTO `{0}` (`login`,`pass`) VALUES ('{1}','{2}')".format(self.table,login,passs))
        self.cursor.fetchone()
        self.connection.commit()

    def get_loginpass(self,ids):
        self.cursor.execute('SELECT login,pass,id FROM {0} WHERE id = {1}'.format(self.table,ids))
        return self.cursor.fetchall()

    def len_tabl(self):
        self.cursor.execute('SELECT count(id) FROM {0}'.format(self.table,))
        return self.cursor.fetchall()

    def update_pass(self,passs, idd):
        self.cursor.execute('UPDATE {0} SET pass = "{1}" WHERE id = {2}'.format(self.table,passs,idd))
        self.cursor.fetchone()
        self.connection.commit()

    def delete_loginpass(self,idus):
        self.cursor.execute("DELETE FROM {0} WHERE id = {1}".format(self.table,idus))






