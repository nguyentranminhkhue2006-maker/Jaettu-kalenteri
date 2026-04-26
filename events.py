import db
from datetime import datetime

def get_all_classes():
    sql="SELECT title, value FROM classes ORDER BY id"
    result=db.query(sql)

    classes={}
    for title, value in result:
        if title not in classes:
            classes[title]=[]
        classes[title].append(value)

    return classes

def add_event(event_name, date_time, description, user_id, classes):
    date_time=date_time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO events (event_name, date_time, description, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [event_name, date_time, description, user_id])

    event_id= db.last_insert_id()

    sql="INSERT INTO event_classes (event_id, title, value) VALUES (?,?,?)"
    for title, value in classes:
        db.execute(sql, [event_id,title, value])

    return event_id

def add_comment(event_id, user_id, content):
    sql="INSERT INTO comments (event_id, user_id, content) VALUES (?,?,?)"
    db.execute(sql, [event_id, user_id, content])

def get_comments(event_id):
    sql=""" SELECT comments.content, users.id user_id, users.username FROM comments, users 
            WHERE comments.event_id=? AND comments.user_id=users.id
            ORDER BY comments.id DESC"""
    return db.query(sql, [event_id])

def get_classes(event_id):
    sql="SELECT title, value FROM event_classes WHERE event_id=?"
    return db.query(sql,[event_id])

def event_count():
    sql="SELECT COUNT(*) FROM events"
    return db.query(sql)[0][0]

def get_events(page, page_size):
    sql=""" SELECT events.id, events.date_time, events.event_name, users.id user_id, users.username
            FROM events, users
            WHERE events.user_id=users.id
            ORDER BY events.date_time
            LIMIT ? OFFSET ?"""
    limit=page_size
    offset=page_size*(page-1)
    return db.query(sql,[limit,offset])

def get_event(event_id):
    sql= """SELECT events.id, events.date_time, events.event_name, events.description, users.username, users.id user_id
            FROM events, users
            WHERE events.user_id = users.id AND events.id = ?"""
    result= db.query(sql,[event_id])
    return result[0] if result else None

def update_event(event_id, date_time, description, classes):
    date_time=date_time.strftime("%Y-%m-%d %H:%M:%S")
    sql="""UPDATE events SET date_time = ?, description = ?
                         WHERE id = ?"""
    db.execute(sql, [date_time, description, event_id])

    sql="DELETE FROM event_classes WHERE event_id=?"
    db.execute(sql,[event_id])

    sql="INSERT INTO event_classes (event_id, title, value) VALUES (?,?,?)"
    for title, value in classes:
        db.execute(sql, [event_id,title, value])

def cancel_event(event_id):
    sql="DELETE FROM event_classes WHERE event_id=?"
    db.execute(sql, [event_id])
    sql="DELETE FROM comments WHERE event_id=?"
    db.execute(sql, [event_id])
    sql="DELETE FROM events WHERE id=?"
    db.execute(sql, [event_id])

def find_event(query, classes, start_time, end_time):
    conditions=[]
    params=[]

    if classes:
        for title in classes:
            conditions.append("event_classes.title=? AND event_classes.value=?")
            params.extend([title, classes[title]])

    if start_time and end_time:
        conditions.append("date_time BETWEEN ? AND ?")
        params.extend([start_time, end_time])
    elif start_time and not end_time:
        conditions.append("date_time > ?")
        params.append(start_time)
    elif end_time and not start_time:
        conditions.append("date_time < ?")
        params.append(end_time)

    if query:
        conditions.append("(event_name LIKE ? OR description LIKE ?)")
        params.extend(["%"+query+"%","%"+query+"%"])

    sql="""SELECT DISTINCT events.id, event_name FROM events LEFT JOIN event_classes ON events.id=event_classes.event_id"""
    if conditions:
        sql+=" WHERE " + " AND ".join(conditions)
    sql+=" ORDER BY events.id DESC"

    return db.query(sql,params)