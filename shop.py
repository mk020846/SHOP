import os
from tabulate import tabulate
from datetime import datetime
import mysql.connector as mycn
from credintials import host , username , password , database, owner_name, owner_password
#------------------------------ FUNCTIONS ----------------------------------------------#
def make_connection():
    global connection
    connection = mycn.connect(host=host,username=username,passwd=password,database=database)
    cursor = connection.cursor()
    return cursor
def login_user(username,password):
    cursor = make_connection()
    cursor.execute(f"SELECT uname,passwd FROM users where uname='{username}';")
    data = cursor.fetchone()
    connection.close()
    if data != None:
        if password == data[1]:
            return True,username
        else:
            print("WRONG PASSWORD")
            return False
    else:
        print("WRONG USERNAME")
        return False
def signup_user(username,password):
    cursor = make_connection()
    try:
        cursor.execute(f"INSERT INTO users(uname,passwd) VALUES('{username}','{password}')")
        connection.commit()
        connection.close()
        print("ACCOUNT CREATED")
        global PROMPT
        PROMPT="SHOP>"
    except Exception as e:
        print(e)
        print("Your account cant be created")
def add_item(itm_name , itm_price , itm_qty ):
    cursor = make_connection()
    try:
        cursor.execute(f"INSERT INTO items(itm_name,itm_price,itm_qty) VALUES('{itm_name}','{itm_price}','{itm_qty}')")
        connection.commit()
        connection.close()
        print(f"ADDED ITEM {itm_name}")
    
    except Exception as e:
        print("ITEM COULDNT BE ADDED")
        print(e)
def update_qty(iod,magnitude,itm_id):
    cursor = make_connection()
    try:
        cursor.execute(f"UPDATE items SET itm_qty=itm_qty{iod}{magnitude} where iid='{itm_id}'")
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print("THE REQUESTED ACTION CANT BE DONE RIGHT NOW")
def search_item(itm_name):
    cursor = make_connection()
    cursor.execute(f"SELECT * FROM items WHERE itm_name like '%{itm_name}%'")
    data = cursor.fetchall()
    cols = ['ITEM ID','ITEM NAME','ITEM PRICE','ITEM QUANTITY']
    print(tabulate(data, cols))
    return True  
def List():
        cursor = make_connection()
        cursor.execute("SELECT * FROM items")
        data = cursor.fetchall()
        columns = ['ITEM ID','ITEM NAME','ITEM PRICE','ITEM QUANTITY']
        print(tabulate(data, headers=columns))
                
def handle_commands(command):
    if command.lower() == "login":
        result = login_user(input("ENTER YOUR USERNAME: "),input("ENTER YOUR PASSWORD: "))
        if result:
            global PROMPT
            global USER 
            USER = result[1]
            PROMPT = f"SHOP@{result[1]}>"
    elif command.lower() == "signup":
        signup_user(input("ENTER YOUR USERNAME: "),input("ENTER YOUR PASSWORD: "))
    elif command.lower() == "buy":
        if USER:
            cursor = make_connection()
            PROMPT=f"{USER}/buying>"
            print(PROMPT+"ENTER THE ITEM NAME YOU WANT TO BUY: ")
            item=input()
            items = search_item(item)
            connection.close()
            if items:
                cursor = make_connection()
                print(PROMPT+"NOW ENTER ITEM ID: ")
                itid = input()
                qty = input(PROMPT+"ENTER THE AMOUNT OF THE ITEM YOU WANT: ")
                cursor.execute(f"SELECT iid,itm_name,itm_price from items where iid='{itid}'")
                data = cursor.fetchone()
                try:
                    update_qty('-',qty,itid)
                    with open(f"logs/{USER}.log",'a') as log:
                        log.write(f"[ {datetime.now()} ] BOUGHT {qty} {data[1]} AT THE PRICE {data[2]} \n")
                        log.close()
                    with open(f"logs/owner_notify.log",'a') as log:
                        log.write(f"[ {datetime.now()} ] {USER} BOUGHT {qty} {data[1]} AT THE PRICE {data[2]} ITEM_ID is {data[0]} \n")
                    print("ITEM HAS BEEN BOOKED FOR YOU")
                except Exception as e:
                    print("INVALID ITEM ID")
        else:
            print("LOGIN FIRST")

    elif command.lower() == "search":
        if USER:
            PROMPT = f"{USER}/searching>"
            search_item(itm_name=input(f"{PROMPT}ENTER THE ITEM NAME: "))
        else:
            print("LOGIN FIRST")
    elif command.lower() == "owner_login":
        username_and_password = input("ENTER USERNAME: "),input("ENTER PASSWROD: ")
        if username_and_password[0] == owner_name and username_and_password[1] == owner_password:
            USER = "OWNER"
            PROMPT = "{___OWNER___}>>"
            print(owner_menu)
        else:
            print("WRONG USENAME OR PASSWORD")

    elif command.lower() == "help":
        if USER == "OWNER":
            print(owner_menu)
        else:
            print(menu)
    elif command.lower() == "clear":
        os.system("clear")
    elif command.lower() == "add_item":
        if USER == "OWNER":
            tprompt = PROMPT
            PROMPT = "ADDING_ITEM>"
            add_item(input(PROMPT+"ENTER ITEM NAME: "),input(PROMPT+"ENTER ITEM PRICE:"),input(PROMPT+"ENTER ITEM QUANTITY: "))
            PROMPT = tprompt
        else:
            print(f"INVALID COMMAND '{command}'")
    elif command.lower() == "update_stock":
        List()
        if USER == 'OWNER':
            iod = input(PROMPT+"INCREASE( I ) or DECREASE ( D )").lower() 
            if iod.upper() == 'I':
                update_qty('+',input("ENTER AMOUNT INCREASED FOR THIS ITEM: "),input("ENTER ITEM ID: "))
            else:
                update_qty('-',input("ENTER AMOUNT DECREASED FOR THIS ITEM: "),input("ENTER ITEM ID: "))
        else:
            print(f"INVALID COMMAND '{command}'")
    elif command.lower() == "recent_orders":
        with open("logs/owner_notify.log") as log:
            data = log.readlines()
            for x in data:
                print(x)
    elif command.lower() == "history":
        try:
            with open(f"logs/{USER}.log") as log:
                data = log.readlines()
                for x in data:
                    print(x)
        except:
            print("YOU BOUGHT NOTHING FOR NOW")
    elif command.lower() == "list":
        List()

    else:   
        print(f"INVALID COMMAND '{command}'")
#------------------------------------------------------------------------------------------------#
#______________________________________MAIN__PROGRAM______________________________________________#
menu = """              WELCOME TO OUR SHOP
            WHAT WOULD YOU LIKE TO DO?
TO LOGIN TYPE :- login
TO SIGNUP TYPE:- signup
TO LIST ALL ITEMS TYPE:- list
TO BUY ANYTHING TYPE:- buy
TO SEARCH A PRODUCT TYPE:- search
TO SEE YOUR ORDER HISTORY TYPE:- history
TO EXIT TYPE:- EXIT
TO PRINT THIS MENU:- help
TO CLEAR TERMINAL TYPE:- clear
            """
owner_menu = """
TO ADD A ITEM TYPE:- add_item
TO UPDATE STOCK TYPE:- update_stock
TO GET RECENT ORDERS TYPE:- recent_orders
"""
USER = False
print(menu)
PROMPT="SHOP>"
while True:
    command = input(PROMPT)
    if command.lower() == "exit":
        break
    else:
        handle_commands(command)
