import pymysql.cursors
from config_mysql import HOST, USER, PASS, DB, CHARSET

def add_player(user_id, name):
    progress = "yard"
    connection = pymysql.connect(
        host=HOST, user=USER, password=PASS, db=DB,
        charset=CHARSET, cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            check_user = "SELECT `progress`, `events` FROM `players` WHERE user_id=%s"
            cursor.execute(check_user, (user_id,))
            result = cursor.fetchone()
            if not result:
                add_user = "INSERT INTO `players` (`user_id`, `name`, `progress`, `events`) VALUES (%s, %s, %s, '')"
                cursor.execute(add_user, (user_id, name, progress))
                data = ["yard", '']
            else:
                data = [result['progress'], result['events']]
        connection.commit()
    finally:
        connection.close()
    return data


def update_user(user_id, progress, event):
    connection = pymysql.connect(
        host=HOST, user=USER, password=PASS, db=DB,
        charset=CHARSET, cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE players SET progress=%s, events=%s WHERE user_id=%s"
            if len(event) >= 50:
                events = event.split(' ')
                event = ' '.join(events[-4:])
            cursor.execute(sql, (progress, event, user_id))
        connection.commit()
    finally:
        connection.close()
    return True


def get_statistic():
    connection = pymysql.connect(
        host=HOST, user=USER, password=PASS, db=DB,
        charset=CHARSET, cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `users_quantity`"
            cursor.execute(sql)
            result = cursor.fetchone()
    finally:
        connection.close()
    return result["count"]