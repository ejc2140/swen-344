from src.swen344_db_utils import connect
import csv, os, sys

def rebuildTables():
    conn = connect()
    cur = conn.cursor()
    drop_user = """
        DROP TABLE IF EXISTS user_table
    """
    create_user = """
        CREATE TABLE user_table(
            UID VARCHAR(40),
            NAME VARCHAR(40),
            EMAIL VARCHAR(40),
            SUSPEND BOOLEAN DEFAULT FALSE,
            SUSP_DATE VARCHAR(40)
        )
    """

    drop_chat = """
        DROP TABLE IF EXISTS chat_table
    """
    create_chat = """
        CREATE TABLE chat_table(
            SENDER_NAME VARCHAR(40),
            RECEIVER_NAME VARCHAR(40),
            CHAT VARCHAR(400),
            DATE INT 
        )
    """
    cur.execute(drop_user)
    cur.execute(create_user)
    cur.execute(drop_chat)
    cur.execute(create_chat)

    test_feed_user(cur)
    test_feed_chat(cur) 

    conn.commit()
    conn.close()
    
def test_feed_user(cur): 
    """feeds data into table"""
    abbott = "INSERT INTO user_table (UID, NAME, EMAIL, SUSPEND, SUSP_DATE) VALUES ('1', 'Abbott', 'who@rit.edu', 'FALSE', 'NA')"
    costello = "INSERT INTO user_table (UID, NAME, EMAIL, SUSPEND, SUSP_DATE) VALUES ('2', 'Costello', 'what@rit.edu', 'FALSE', 'NA')"
    moe = "INSERT INTO user_table (UID, NAME, EMAIL, SUSPEND, SUSP_DATE) VALUES ('3', 'Moe', 'mo@gmail.com', 'FALSE', 'NA')"
    curly = "INSERT INTO user_table (UID, NAME, EMAIL, SUSPEND, SUSP_DATE) VALUES ('4', 'Curly', 'cr@gmail.com', 'TRUE', '01-01-2060')"
    larry = "INSERT INTO user_table (UID, NAME, EMAIL, SUSPEND, SUSP_DATE) VALUES ('5', 'Larry', 'la@gmail.com', 'FALSE', 'NA')"

    cur.execute(abbott) 
    cur.execute(costello)
    cur.execute(moe)
    cur.execute(curly)
    cur.execute(larry)

def test_feed_chat(cur):
    with open(os.path.join(sys.path[0], 'tests/test_data.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        i = 1

        for row in csv_reader:
            ID_num = i 
            SENDER_NAME = row[0]
            RECEIVER_NAME = row[1]
            CHAT = row[2]
            if row[3].isdigit():
                DATE = int(row[3])
            else: 
                DATE = 0
                
            cur.execute("INSERT INTO chat_table(SENDER_NAME, RECEIVER_NAME, CHAT, DATE) VALUES (%s, %s, %s, %s)", (SENDER_NAME, RECEIVER_NAME, CHAT, DATE))
            i += 1 