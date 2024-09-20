import sqlite3 as sql
from functions import *
import tkinter as tk


sql_connection = sql.connect('user_data.db')
cursor = sql_connection.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS userdatas 
               (username, pack_name, description, cards)""")

def get_records(username):
    user_packs = cursor.execute(f"""SELECT rowid, * FROM userdatas WHERE username='{username}'""")
    sql_connection.commit()
    return user_packs

def add_record(pack_info, pack_label, save_button, pack_entry, description_entry, x_button):
    pack_label.pack(side=tk.RIGHT, padx=90)
    save_button.configure(state='disabled')
    pack_entry.configure(state='disabled')
    description_entry.configure(state='disabled')
    x_button.configure(state='disabled')
    final_info = (pack_info[0], pack_info[1], pack_info[2], pack_info[3])
    cursor.execute(f"""INSERT INTO userdatas VALUES (?, ?, ?, ?)""", final_info)
    sql_connection.commit()

def update_record(row_id, pack_name, description, cards_list):
    cards = card_compressor(card_class_to_list(cards_list))
    cursor.execute(f"""UPDATE userdatas SET pack_name="{pack_name}",
                                            description="{description}",
                                            cards="{cards}"
                        WHERE rowid={row_id}""")
    sql_connection.commit()

def remove_record(pack_id: int):
    cursor.execute(f"""DELETE from userdatas WHERE rowid={pack_id}""")
    sql_connection.commit()



