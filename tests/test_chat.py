import unittest
import csv
from src.chat import *
from src.chat_ops import *
from src.swen344_db_utils import connect


class TestChat(unittest.TestCase):            

    def test_build_user(self):
        """rebuild the user table"""
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        cur.execute('SELECT * FROM user_table')
        self.assertNotEqual([], cur.fetchall(), "no rows in user_table")
        conn.close()
    
    def test_build_chat(self):
        """rebuild the chat table"""
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        cur.execute('SELECT * FROM chat_table')
        self.assertNotEqual([], cur.fetchall(), "no rows in chat_table")
        conn.close()

    
    def test_user_abbott(self):
        """Checks for User Abbott"""
        conn = connect()
        cur = conn.cursor()
        rebuildTables() 
        cur.execute("SELECT NAME FROM user_table WHERE NAME = 'Abbott'")

        self.assertEqual('Abbott', cur.fetchone()[0], "Abbott not found")
        conn.close()

    def test_user_costello(self):
        """Checks for User Costello"""
        conn = connect()
        cur = conn.cursor()
        rebuildTables() 
        cur.execute("SELECT NAME FROM user_table WHERE NAME = 'Costello'")

        self.assertEqual('Costello', cur.fetchone()[0], "Costello not found")
        conn.close()
    
    def test_user_count(self):
        """Counts total number of users"""
        conn = connect()
        cur = conn.cursor()
        rebuildTables() 
        cur.execute("SELECT * FROM user_table")
        self.assertEqual(5, cur.rowcount, "Wrong number of users, 5 expected")
        conn.close()

    def test_chat_count(self):
        """Counts total number of chat messages"""
        conn = connect()
        cur = conn.cursor()
        rebuildTables() 
        cur.execute("SELECT * FROM chat_table")
        self.assertEqual(185, cur.rowcount, "Wrong number of messages, 185 expected")
        conn.close()

    def test_chat_specific(self):
        """Find all messages from the years 1934-1946 from Larry, Curly, and Moe"""
        conn = connect()
        cur= conn.cursor()
        rebuildTables()
        cur.execute("SELECT * FROM chat_table WHERE DATE BETWEEN 1934 AND 1946 AND SENDER_NAME IN ('Curly', 'Larry', 'Moe')")
        self.assertEqual(8, cur.rowcount, "Wrong number of messages, 8 expected")
        conn.close()

    def test_suspend_true(self): 
        """Checks that Curly is Suspended"""
        conn = connect()
        cur= conn.cursor()
        rebuildTables()
        cur.execute("SELECT SUSPEND FROM user_table WHERE NAME = 'Curly'")
        self.assertEqual(True, cur.fetchone()[0], "Curly Should be Suspended")
        conn.close()

    def test_suspend_false(self): 
        """Checks that Moe is NOT Suspended"""
        conn = connect()
        cur= conn.cursor()
        rebuildTables()
        cur.execute("SELECT SUSPEND FROM user_table WHERE NAME = 'Moe'")
        self.assertEqual(False, cur.fetchone()[0], "Moe Should not be Suspended")
        conn.close()

    def test_add_user(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        add_user(6, 'Bob', 'bob@yahoo.com', False, 'NA')
        cur.execute("SELECT NAME FROM user_table WHERE NAME = 'Bob'")
        self.assertEqual('Bob', cur.fetchone()[0], "User Bob is not found")
        conn.close()

    def test_update_email(self):
        conn = connect()
        cur = conn.cursor()
        add_user(6, 'Bob', 'bob@yahoo.com', False, 'NA')
        update_email('Bob', 'bobby@outlook.com')
        cur.execute("SELECT EMAIL FROM user_table WHERE NAME = 'Bob'")
        self.assertEqual('bobby@outlook.com', cur.fetchone()[0], "User Bob's email has not been updated")
        conn.close()

    def test_delete_user(self):
        conn = connect()
        cur = conn.cursor()
        add_user(6, 'Bob', 'bob@yahoo.com', False, 'NA')
        delete_user('Bob')
        cur.execute("SELECT NAME FROM user_table WHERE NAME = 'Bob'")
        self.assertIsNone(cur.fetchone(), "User Bob is found")
        conn.close()

    def test_suspend_curly(self):
        conn = connect()
        cur = conn.cursor()
        suspend_user(True, 'Curly', '03-03-2070')
        cur.execute("SELECT SUSPEND FROM user_table WHERE NAME = 'Curly'")
        self.assertEqual(True, cur.fetchone()[0], "Curly was not suspended")
        conn.close()
    
    def test_suspend_message(self):
        conn = connect()
        cur = conn.cursor()
        suspend_user(True, 'Curly', '03-03-2070')
        send_chat('Curly','Joe','test','1990')
        cur.execute("SELECT CHAT FROM chat_table WHERE DATE = '1990'")
        self.assertIsNone(cur.fetchone(), "Chat is found")

    def test_unsuspend(self):
        conn = connect()
        cur = conn.cursor()
        suspend_user(False, 'Curly', 'NA')
        cur.execute("SELECT SUSPEND FROM user_table WHERE NAME = 'Curly'")
        self.assertEqual(False, cur.fetchone()[0], "Curly was not suspended")
        conn.close()
    
    def test_suspend_message(self):
        conn = connect()
        cur = conn.cursor()
        suspend_user(False, 'Curly', 'NA')
        send_chat('Curly','Joe',"test", 1990)
        cur.execute("SELECT DATE FROM chat_table WHERE SENDER_NAME = 'Curly' AND RECEIVER_NAME = 'Joe'")
        self.assertEqual(1990, cur.fetchone()[0], "Chat is not found")
        conn.close()
    
    def test_find_chat(self):
        conn = connect()
        cur = conn.cursor()
        rebuildTables()
        chat = chats_between_users('Abbott', 'Costello')
        nat_chat = chat_from_word("%Naturally%")
        total = set(chat).intersection(nat_chat)
        self.assertEqual(3, len(total), "Naturally wasn't found 5 times")
        conn.close()