# Mohammad Hawat - Student ID: 24056361

import MySQLdb

def get_db_connection():
    return MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="hawat123",      
        db="ht_booking_db"
    )