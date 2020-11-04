from src.swen344_db_utils import connect

def add_user(UID, name, email, suspend, susp_date):
    conn = connect()
    cur = conn.cursor() 

    cur.execute("INSERT INTO user_table(UID, NAME, EMAIL, SUSPEND, SUSP_DATE) VALUES (%s, %s, %s, %s, %s)",(UID, name, email, suspend, susp_date))

    conn.commit()
    conn.close()

def update_email(name, email):
    conn = connect()
    cur = conn.cursor()

    cur.execute("UPDATE user_table SET EMAIL = %s WHERE NAME = %s ", (email, name))
    conn.commit()
    conn.close()

def delete_user(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM user_table  WHERE NAME = '" + name + "'")
    conn.commit()
    conn.close()

def suspend_user(suspend, name, date):
    conn = connect()
    cur = conn.cursor()

    cur.execute("UPDATE user_table SET SUSPEND = %s WHERE NAME = %s ", (suspend, name))
    cur.execute("UPDATE user_table SET SUSP_DATE = %s WHERE NAME = %s ", (date, name))
    conn.commit()
    conn.close()

def send_chat(sender, receiver, chat, date):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT SUSPEND FROM user_table WHERE NAME ='" + sender + "'")
    if cur.fetchone()[0] == True:
        cur.execute("SELECT SUSP_DATE FROM user_table WHERE NAME ='" + sender + "'")
        print("User cannot send messages until '" + cur.fetchone()[0])
    else: 
        cur.execute("INSERT INTO chat_table(SENDER_NAME, RECEIVER_NAME, CHAT, DATE) VALUES(%s, %s, %s, %s)", (sender, receiver, chat, date))
    conn.commit()
    conn.close()

def chats_between_users(sender, receiver):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chat_table WHERE (SENDER_NAME = %s AND RECEIVER_NAME = %s) OR (SENDER_NAME = %s AND RECEIVER_NAME = %s)", (sender, receiver, receiver, sender))
    chat_msg = cur.fetchall()
    conn.commit()
    conn.close()
    return chat_msg

def chat_from_word(word):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM chat_table WHERE CHAT LIKE '" + word + "'")
    chat_msg = cur.fetchall()
    conn.commit()
    conn.close()
    return chat_msg
