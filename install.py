import mysql.connector as mycn
HOST = "localhost"
uname = input("Enter username of MySQL:")
password = input("Enter password of MySQL:")
conn = mycn.connect(host=HOST,username=uname,passwd=password)
csr = conn.cursor()
csr.execute("create database SHOP;")
csr.execute("use SHOP;")
csr.execute("create table users(uid int(5) PRIMARY KEY AUTO_INCREMENT, uname varchar(20), passwd varchar(20));")
csr.execute("create table items(iid int(5) PRIMARY KEY AUTO_INCREMENT, itm_name varchar(20), itm_price float(10,2), itm_qty int(10));") 
conn.commit()
owner_name = input("Enter owner_name: ")
owner_password = input("Enter owner_password: ")
print("use owner_login in the shop.py to use owner privelages")
try:
    with open("credintials.py",'w') as file:
        file.write(f"""host='{HOST}'\nusername='{uname}'\npassword='{password}'\ndatabase='SHOP'\nowner_name='{owner_name}'\nowner_password='{owner_password}'""")
        file.close()
    print("INSTALLATION IS COMPLETED")
except Exception as e:
    print(e)
    print("INSTALLATION CAN'T be completed")
option = input("Do you want to start the program now??(Y/N): ")
if option.upper() == "Y":
    import shop
else:
    print("installation is successful you can now use the program in terminal.")
