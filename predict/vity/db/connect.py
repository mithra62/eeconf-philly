import vity.config as vity_config
import MySQLdb
import MySQLdb.cursors

def db_obj():
    db = MySQLdb.connect(
    	host=vity_config.mysql['host'],
    	user=vity_config.mysql['user'],
    	passwd=vity_config.mysql['password'],
    	db=vity_config.mysql['db'],
        charset='utf8mb4',
    	cursorclass=MySQLdb.cursors.DictCursor)

    #we don't wanna do transaction level stuff
    #plus, dogshit slow with the level of mining
    db.autocommit(True)
    return db
