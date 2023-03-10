import sqlite3
import tkinter
import datetime

#--------------Create hop database-----------------

cnt = sqlite3.connect("Shop_Final_Project.db")

#-----------Creat users table------------------------

#query = ''' CREATE TABLE users
#(id INTEGER PRIMARY KEY,
# username CHAR(15) NOT NULL,
# password CHAR(15) NOT NULL,
# address CHAR(15) NOT NULL)'''
#cnt.execute(query)
#print("Users table created successfully")
#cnt.close()

#------------Create product table-------------------

# query = ''' CREATE TABLE products
# (id INTEGER PRIMARY KEY,
# pname CHAR(15) NOT NULL,
# price REAL NOT NULL,
# qnt INTEGER NOT NULL)'''
# cnt.execute(query)
# print("Product table created successfully")
# cnt.close()

#-----------------Insert initial records into users table------------

# query = ''' INSERT INTO users (username,password,address) VALUES ("admin","123456789","none"); '''
# cnt.execute(query)
# cnt.commit()
# cnt.close()

#-----------------Insert initial record intos products table------------

# query = ''' INSERT INTO products (pname,price,qnt) VALUES ("Television","1500","25"); '''
# cnt.execute(query)
# cnt.commit()
# cnt.close()

#------------------Create final_shop table---------------

# query = '''CREATE TABLE final_shop(
# id INTEGER PRIMARY KEY,
# pid INTEGER NOT NULL,
# uid INTEGER NOT NULL,
# qnt INTEGER NOT NULL,
# date TEXT NOT NULL)'''
# cnt.execute(query)
# print("Finla_shop table created successsfully!")
# cnt.close()

#----------------------------  F U N C T I O N S  -----------------------------

#------------Login function---------------

def login():
    global user_id
    user = txt_user.get()
    pas = txt_pass.get()
    
    #----------validation------------
    if user == "" or pas == "":
        lbl_msg.configure(text="please fill the inputs",fg = "red")
        return
    #----------database search--------
    query = ''' SELECT * FROM users WHERE username = ? AND password = ?'''
    result = cnt.execute(query,(user,pas))
    rows = result.fetchall()
    if len(rows) == 0:
        lbl_msg.configure(text="Wrong Username or Password",fg = "red")
        return
    lbl_msg.configure(text="Welcome to Your Account!",fg = "green")
    user_id = rows[0][0]
    if user == "admin":    
        admin_btn.configure(state="active")
        lbl_msg.configure(text="Hi Admin :) ",fg = "green")
    txt_user.delete(0,"end")
    txt_pass.delete(0,"end")
    btn_login.configure(state = "disabled")
    btn_submit.configure(state="disabled")
    btn_logout.configure(state="active")
    btn_shop.configure(state="active")
    my_shop_btn.configure(state="active")

    
#----------------Logout function----------------

def logout():
    btn_login.configure(state="active")
    btn_submit.configure(state="active")
    btn_logout.configure(state= "disabled")
    btn_shop.configure(state="disabled")
    my_shop_btn.configure(state="disabled")
    admin_btn.configure(state="disabled")
    lbl_msg.configure(text="You are Logged out",fg = "green")

#----------------Submit function------------------
    
def get_submit_values():
    user = txt_user2.get()
    pas = txt_pass2.get()
    cpas = txt_cpas.get()
    addr = txt_addr.get()
    return (user,pas,cpas,addr)


def submit_validation():
    user,pas,cpas,addr = get_submit_values()
    if user == "" or pas == "" or cpas == "" or addr == "":
        lbl_msg2.configure(text="Please Fill the Inputs",fg="red")
        return False
    if len(pas) < 8:
        lbl_msg2.configure(text="Password Min Length is 8",fg="red")
        return False
    if pas != cpas:
        lbl_msg2.configure(text="Password and Confirmation Mismatch",fg="red")
        return False
    query = ''' SELECT * FROM users WHERE username = ?'''
    result = cnt.execute(query,(user,))
    rows = result.fetchall()
    if len(rows) != 0:
        lbl_msg2.configure(text="Username Alredy Exist!",fg = "red")
        return False
    return True
    
        
def final_submit():
    user,pas,cpas,addr = get_submit_values()
    result = submit_validation()
    if not result:
        return
    query = ''' INSERT INTO users (username,password,address) VALUES (?,?,?) '''
    cnt.execute(query,(user,pas,addr))
    cnt.commit()
    lbl_msg2.configure(text="Submit Done!",fg="green")
    txt_user2.delete(0,"end")
    txt_pass2.delete(0,"end")
    txt_cpas.delete(0,"end")
    txt_addr.delete(0,"end")

    
def submit():
    global txt_user2,txt_pass2,txt_cpas,txt_addr,lbl_msg2
    win_submit = tkinter.Toplevel(win)
    win_submit.title("Submit Panel")
    win_submit.geometry("350x300")
    win_submit.resizable(False,False)
    
    #---------widgets-------------
    
    lbl_user2 = tkinter.Label(win_submit,text="Username: ")
    lbl_user2.pack()
    txt_user2 = tkinter.Entry(win_submit,width=15)
    txt_user2.pack()
    
    lbl_pass2 = tkinter.Label(win_submit,text="Password: ")
    lbl_pass2.pack()
    txt_pass2 = tkinter.Entry(win_submit,width=15)
    txt_pass2.pack()
    
    lbl_cpas = tkinter.Label(win_submit,text="Password Confirmation: ")
    lbl_cpas.pack()
    txt_cpas = tkinter.Entry(win_submit,width=15)
    txt_cpas.pack()
    
    
    lbl_addr = tkinter.Label(win_submit,text="Address: ")
    lbl_addr.pack()
    txt_addr = tkinter.Entry(win_submit,width=50)
    txt_addr.pack()
    
    lbl_msg2 = tkinter.Label(win_submit,text="")
    lbl_msg2.pack(pady=10)
    
    btn_submit2 = tkinter.Button(win_submit,text="Submit Now",activeforeground="blue",cursor="hand2",command=final_submit)
    btn_submit2.pack()
    
    
    win_submit.mainloop()
    
#---------------Shop function---------------

def update_list():
    query = ''' SELECT * FROM products'''
    result = cnt.execute(query)
    rows = result.fetchall()
    lstbox.delete(0,"end")
    for item in rows:
        #lstbox.insert("end",str(item[0])+' '+ str(item[1]) +' '+'Price = '+ str(item[2])+' '+'Qnt =' + str(item[3]))
        lstbox.insert("end",f"Product_ID={item[0]} // Name={item[1]} // Price={item[2]} // Quantity={item[3]}" )

def final_shop():
    pid = pid_txt.get()
    pqnt = pqnt_txt.get()
    
    #-------------------Check product ID----------------
    if pid == "" or pqnt == "":
        msg_lbl.configure(text="please fill the blanks!",fg="red")
        return
    query = '''SELECT * FROM products WHERE id = ?'''
    result = cnt.execute(query,(pid,))
    rows = result.fetchall()
    if len(rows) == 0:
        msg_lbl.configure(text="wrong product ID",fg="red")
        return
    #-------------Check product quantity-------------------
    row = rows[0]
    real_qnt = row[3]
    
    if int(pqnt) > real_qnt:
        msg_lbl.configure(text="not enough product!",fg="red")
        return
    #-------insert data to final_shop table----------------
    
    now = datetime.date.today()
    date_string = now.strftime("%Y-%m-%d")
    query = '''INSERT INTO final_shop(pid,uid,qnt,date) VALUES (?,?,?,?)'''
    cnt.execute(query,(pid,user_id,pqnt,date_string))
    cnt.commit()
    
    new_qnt = real_qnt-int(pqnt)
    query = '''UPDATE products SET qnt = ? WHERE id = ?'''
    cnt.execute(query,(new_qnt,pid))
    cnt.commit()
    
    pid_txt.delete(0,"end")
    pqnt_txt.delete(0,"end")
    
    msg_lbl.configure(text = "shop saved successfully!",fg = "green")
    
    #------------ Update listbox -----------------
    
    update_list()
        
    
    
def shop():
    global pid_txt,pqnt_txt,msg_lbl,lstbox
    win_shop = tkinter.Toplevel(win)
    win_shop.title("Shop Panel")
    win_shop.geometry("400x350")
    win_shop.resizable(False,False)
    
    #--------list box--------
    lstbox = tkinter.Listbox(win_shop,width=100)
    lstbox.pack(pady=10)
    #lstbox.insert("end","salam")
    
    pid_lbl = tkinter.Label(win_shop,text="Product ID")
    pid_lbl.pack()
    
    pid_txt = tkinter.Entry(win_shop,width=20)
    pid_txt.pack()
    
    pqnt_lbl = tkinter.Label(win_shop,text="Product Quantity")
    pqnt_lbl.pack()
    
    pqnt_txt = tkinter.Entry(win_shop,width=20)
    pqnt_txt.pack()
    
    msg_lbl = tkinter.Label(win_shop,text="")
    msg_lbl.pack()
    
    final_shop_btn = tkinter.Button(win_shop,text="Final Shop",activeforeground="blue",cursor="hand2",command=final_shop)
    final_shop_btn.pack()
    
    #-----fech data from products table-------------
    update_list()
    win.mainloop()
    
#---------------My_shop function------------------
    
def my_shop():
    win_my_shop = tkinter.Toplevel(win)
    win_my_shop.title("My shop panel")
    win_my_shop.geometry("400x300")
    win_my_shop.resizable(False,False)
    
    lstbox2 = tkinter.Listbox(win_my_shop,width=100)
    lstbox2.pack(pady=10)
    
    query = '''SELECT products.pname,products.price,final_shop.qnt
    FROM final_shop
    JOIN
    products
    ON final_shop.pid=products.id
    WHERE final_shop.uid = ?'''
    result = cnt.execute(query,(user_id,))
    rows = result.fetchall()
    
    for item in rows:
        total_price = item[1]*item[2]
        lstbox2.insert("end",f"Name= {item[0]} // QNT= {item[2]} // Total Price= {total_price}" )
    
    win_my_shop.mainloop()
    
#----------------     A  D  M  I  N   F U N C T I O N S     -----------------------


def update_list_user():
    query = ''' SELECT * FROM users'''
    result = cnt.execute(query)
    rows = result.fetchall()
    lstbox.delete(0,"end")
    for item in rows:
        lstbox.insert("end",f"UserID= {item[0]}  //  Username= {item[1]}  //  Password= {item[2]}  //  Address= {item[3]}" )

def update_list_products():
    query = ''' SELECT * FROM products'''
    result = cnt.execute(query)
    rows = result.fetchall()
    lstbox.delete(0,"end")
    for item in rows:
        lstbox.insert("end",f"ProductID= {item[0]}  //  P_Name= {item[1]}  //  Price= {item[2]}  //  Quantity= {item[3]}" )

def user_info():
    global update_list_user,lstbox
    win_user_info = tkinter.Toplevel(win_admin)
    win_user_info.title("Users Information")
    win_user_info.geometry("450x350")
    win_user_info.resizable(False,False)
    
    #------------lstbox for information------------
    
    lstbox = tkinter.Listbox(win_user_info,width=100)
    lstbox.pack(pady=10)
    update_list_user()
    
    win_user_info.mainloop()
 
def final_add():
    txt_add_user_final = txt_add_user.get()
    txt_add_pas_final = txt_add_pas.get()
    txt_add_addr_final = txt_add_addr.get()
    if txt_add_user_final == "" and txt_add_pas_final == "" and txt_add_addr_final == "":
        msg_add_user.configure(text="Please fill the blanks!",fg="red")
        return
    if len(txt_add_pas_final) < 8:
        msg_add_user.configure(text="Password Min Length is 8",fg="red")
        return
    query = '''SELECT * FROM users WHERE username = ?'''
    result = cnt.execute(query,(txt_add_user_final,))
    rows = result.fetchall()
    if len(rows) != 0:
        msg_add_user.configure(text="Username already exist!",fg="red")
        return
    query = '''INSERT INTO users (username,password,address) VALUES(?,?,?)'''
    cnt.execute(query,(txt_add_user_final,txt_add_pas_final,txt_add_addr_final))
    cnt.commit()
    msg_add_user.configure(text="Add Done!",fg="green")
    txt_add_user.delete(0,"end")
    txt_add_pas.delete(0,"end")
    txt_add_addr.delete(0,"end")
    
    #-------Update users list----------
    
    update_list_user()

def add_user():
    global txt_add_user,txt_add_pas,txt_add_addr,msg_add_user,lstbox
    win_add_user = tkinter.Toplevel(win_admin_umanage)
    win_add_user.title("Add Users")
    win_add_user.geometry("500x400")
    win_add_user.resizable(False,False)
    
    #----------lstbox for add user--------------
    
    lstbox = tkinter.Listbox(win_add_user,width=100)
    lstbox.pack(pady=10)
    
    #----------widgets-------------------
    
    lbl_add_user = tkinter.Label(win_add_user,text="Username:")
    lbl_add_user.pack()
    
    txt_add_user = tkinter.Entry(win_add_user,width=15)
    txt_add_user.pack()
    
    lbl_add_pas = tkinter.Label(win_add_user,text="Password:")
    lbl_add_pas.pack()
    
    txt_add_pas = tkinter.Entry(win_add_user,width=15)
    txt_add_pas.pack()
    
    lbl_add_addr = tkinter.Label(win_add_user,text="Address:")
    lbl_add_addr.pack()
    
    txt_add_addr = tkinter.Entry(win_add_user,width=50)
    txt_add_addr.pack()
    
    msg_add_user = tkinter.Label(win_add_user,text="")
    msg_add_user.pack()

    btn_add_user = tkinter.Button(win_add_user,text="ADD",activeforeground="blue",cursor="hand2",command=final_add)    
    btn_add_user.pack()
    
    update_list_user()
    
    win_add_user.mainloop()
    
    
def final_del():
    txt_del_id_final = txt_del_id.get()
    txt_del_user_final = txt_del_user.get()
    if txt_del_id_final == "" and txt_del_user_final == "":
        msg_del_user.configure(text="At least one blank must be filled!",fg="red")
        return
    if len(txt_del_id_final) != 0 and len(txt_del_user_final) != 0:
        msg_del_user.configure(text="You must choose one methode not both!",fg="red")
        return
    if len(txt_del_id_final) != 0 and len(txt_del_user_final) == 0:
        query = '''SELECT * FROM users WHERE id=?'''
        result = cnt.execute(query,(txt_del_id_final,))
        rows = result.fetchall()
        if len(rows) == 0:
            msg_del_user.configure(text="ID doesn't exist!",fg="red")
        else:
            query = '''DELETE FROM users WHERE id = ?'''
            cnt.execute(query,(txt_del_id_final,))
            cnt.commit()
            msg_del_user.configure(text="Delete done!",fg="green")
            txt_del_id.delete(0,"end")
            #------Update list--------
            update_list_user()
    if len(txt_del_id_final) == 0 and len(txt_del_user_final) != 0:
        query = '''SELECT * FROM users WHERE username=?'''
        result = cnt.execute(query,(txt_del_user_final,))
        rows = result.fetchall()
        if len(rows) == 0:
            msg_del_user.configure(text="Username doesn't exist!",fg="red")
        else:
            query = '''DELETE FROM users WHERE username = ?'''
            cnt.execute(query,(txt_del_user_final,))
            cnt.commit()
            msg_del_user.configure(text="Delete done!",fg="green")
            txt_del_user.delete(0,"end")
            
            #------Update list--------
            
            update_list_user()
    
def del_user():
    global txt_del_id,txt_del_user,msg_del_user,lstbox
    win_del_user = tkinter.Toplevel(win_admin_umanage)
    win_del_user.title("Delete Users")
    win_del_user.geometry("500x400")
    win_del_user.resizable(False,False)
    
    #----------lstbox for add user--------------
    
    lstbox = tkinter.Listbox(win_del_user,width=100)
    lstbox.pack(pady=10)
    
    #----------widgets-------------------
    
    lbl_del_warn = tkinter.Label(win_del_user,text="To delete any User, you can choose one of the following two methods.",fg="blue")
    lbl_del_warn.pack()
    
    lbl_del_id = tkinter.Label(win_del_user,text="User ID:")
    lbl_del_id.pack()
    
    txt_del_id = tkinter.Entry(win_del_user,width=15)
    txt_del_id.pack()
    
    lbl_del_warn2 = tkinter.Label(win_del_user,text="or")
    lbl_del_warn2.pack()
    
    lbl_del_user = tkinter.Label(win_del_user,text="Username:")
    lbl_del_user.pack()
    
    txt_del_user = tkinter.Entry(win_del_user,width=15)
    txt_del_user.pack()
    
    msg_del_user = tkinter.Label(win_del_user,text="")
    msg_del_user.pack()

    btn_del_user = tkinter.Button(win_del_user,text="DELETE",activeforeground="blue",cursor="hand2",command=final_del)    
    btn_del_user.pack()
    
    update_list_user()
    
    win_del_user.mainloop()
    
def final_edit():
    txt_edit_pas_final = txt_edit_pas.get()
    txt_edit_addr_final = txt_edit_addr.get()
    txt_edit_id_final2 = txt_edit_id.get()
    
    
    if txt_edit_pas_final == "" and txt_edit_addr_final == "":
        msg_edit_final.configure(text="At least one blank must be filled!",fg="red")
        return
    
    if len(txt_edit_pas_final) != 0 and len(txt_edit_addr_final) != 0:  
        if len(txt_edit_pas_final) < 8:
            msg_edit_final.configure(text="Password Min Length is 8",fg="red")
            return
        if len(txt_edit_addr_final) < 3:
            msg_edit_final.configure(text="Address Min Length is 3",fg="red")
            return
        query = '''UPDATE users SET password = ? WHERE id = ?'''
        cnt.execute(query,(txt_edit_pas_final,txt_edit_id_final2))
        cnt.commit()
        query = '''UPDATE users SET address = ? WHERE id = ?'''
        cnt.execute(query,(txt_edit_addr_final,txt_edit_id_final2))
        cnt.commit()
        msg_edit_final.configure(text="Edit done!",fg="green")
        txt_edit_pas.delete(0,"end")
        txt_edit_addr.delete(0,"end")
        
        update_list_user()
        
    if len(txt_edit_pas_final) != 0 and len(txt_edit_addr_final) ==0:
        if len(txt_edit_pas_final) < 8:
            msg_edit_final.configure(text="Password Min Length is 8",fg="red")
            return
        query = '''UPDATE users SET password = ? WHERE id = ? '''
        cnt.execute(query,(txt_edit_pas_final,txt_edit_id_final2))
        cnt.commit()
        
        msg_edit_final.configure(text="Edit done!",fg="green")
        txt_edit_pas.delete(0,"end")
        
        update_list_user()
    else:
        if len(txt_edit_addr_final) < 3:
            msg_edit_final.configure(text="Address Min Length is 3",fg="red")
            return
        query = '''UPDATE users SET address = ? WHERE id = ? '''
        cnt.execute(query,(txt_edit_addr_final,txt_edit_id_final2))
        cnt.commit()
        
        msg_edit_final.configure(text="Edit done!",fg="green")
        txt_edit_addr.delete(0,"end")
        
        update_list_user()
    
    
def next_step():
    global lstbox,txt_edit_pas,txt_edit_addr,msg_edit_final
    txt_edit_id_final = txt_edit_id.get()
    if txt_edit_id_final == "":
        msg_edit_id.configure(text="Please fill the blank!",fg="red")
        return
    query = '''SELECT * FROM users WHERE id = ?'''
    result = cnt.execute(query,(txt_edit_id_final,))
    rows = result.fetchall()
    if len(rows) == 0:
        msg_edit_id.configure(text="ID doesn't exist!",fg="red")
        return
    #----------------------------------------------------
    win_edit_final = tkinter.Toplevel(win_edit_user)
    win_edit_final.title("Final Edit")
    win_edit_final.geometry("500x400")
    
    #----------lstbox for edit user--------------

    lstbox = tkinter.Listbox(win_edit_final,width=100)
    lstbox.pack(pady=10)
    
    #----------------widgets-----------------------
    lbl_edit_final = tkinter.Label(win_edit_final,text="You can change Password or Address or both of them for any User.",fg="blue")
    lbl_edit_final.pack(pady=5)
    
    lbl_edit_pas = tkinter.Label(win_edit_final,text="Change Password:")
    lbl_edit_pas.pack(pady=5)
    
    txt_edit_pas = tkinter.Entry(win_edit_final,width=15)
    txt_edit_pas.pack()
    
    lbl_edit_addr = tkinter.Label(win_edit_final,text="Change Address:")
    lbl_edit_addr.pack(pady=5)
    
    txt_edit_addr = tkinter.Entry(win_edit_final,width=50)
    txt_edit_addr.pack()
    
    msg_edit_final = tkinter.Label(win_edit_final,text="")
    msg_edit_final.pack()
    
    btn_edit_final = tkinter.Button(win_edit_final,text="Edit",activeforeground="blue",cursor="hand2",command=final_edit)
    btn_edit_final.pack(pady=5)
    
    update_list_user()
    
    win_edit_final.mainloop()
    
    
    
    
def edit_user():
    global win_edit_user,lstbox,txt_edit_id,msg_edit_id
    win_edit_user = tkinter.Toplevel(win_admin_umanage)
    win_edit_user.title("Edit Users")
    win_edit_user.geometry("500x400")
    
    #----------lstbox for edit user--------------

    lstbox = tkinter.Listbox(win_edit_user,width=100)
    lstbox.pack(pady=10)
    
    #----------------widgets-----------------------
    
    lbl_msg_edit = tkinter.Label(win_edit_user,text="To edit User's Information ,input User's ID form table above or your Database. ",fg="blue")
    lbl_msg_edit.pack()
    
    lbl_edit_id = tkinter.Label(win_edit_user,text="User ID:")
    lbl_edit_id.pack()
    
    txt_edit_id = tkinter.Entry(win_edit_user,width=15)
    txt_edit_id.pack()
    
    msg_edit_id = tkinter.Label(win_edit_user,text="")
    msg_edit_id.pack()
    
    btn_edit_user = tkinter.Button(win_edit_user,text="Next Step",activeforeground="blue",cursor="hand2",command=next_step)
    btn_edit_user.pack()
    
    
    update_list_user()
    
    win_edit_user.mainloop()
    
def user_manage():
    global win_admin_umanage
    win_admin_umanage = tkinter.Toplevel(win_admin)
    win_admin_umanage.title("Users Management")
    win_admin_umanage.geometry("300x200")
    win_admin_umanage.resizable(False,False)
    
    #--------widgets-----------
    lbl_umanage_question = tkinter.Label(win_admin_umanage,text="What do you want to do?",fg="blue")
    lbl_umanage_question.pack(pady=30)
    
    btn_umanage_add = tkinter.Button(win_admin_umanage,text="Add User",activeforeground="blue",cursor="hand2",command=add_user)
    btn_umanage_add.place(x=30,y=100)
    
    btn_umanage_del = tkinter.Button(win_admin_umanage,text="Delete User",activeforeground="blue",cursor="hand2",command=del_user)
    btn_umanage_del.place(x=110,y=100)
    
    btn_umanage_edit = tkinter.Button(win_admin_umanage,text="Edit User",activeforeground="blue",cursor="hand2",command=edit_user)
    btn_umanage_edit.place(x=200,y=100)
    
    
    win_admin_umanage.mainloop()
    
    
def product_info():
    global update_list_products,lstbox
    win_pro_info = tkinter.Toplevel(win_admin)
    win_pro_info.title("Products Information")
    win_pro_info.geometry("400x300")
    win_pro_info.resizable(False,False)
    
    #------------lstbox for information------------
    
    lstbox = tkinter.Listbox(win_pro_info,width=100)
    lstbox.pack(pady=10)
    
    update_list_products()
    
    win_pro_info.mainloop()
    
def final_add_product():
    txt_add_pname_final = txt_add_pname.get()
    txt_add_price_final = txt_add_price.get()
    txt_add_qnt_final = txt_add_qnt.get()
    
    if txt_add_pname_final == "" and txt_add_price_final == "" and txt_add_qnt_final == "":
        msg_add_pro.configure(text="Please fill the blanks!",fg="red")
        return
    if txt_add_pname_final == "" or txt_add_price_final == "" or txt_add_qnt_final == "":
        msg_add_pro.configure(text="Please fill all the blanks!",fg="red")
        return
    query = '''SELECT * FROM products WHERE pname = ?'''
    result = cnt.execute(query,(txt_add_pname_final,))
    rows = result.fetchall()
    if len(rows) != 0:
        msg_add_pro.configure(text="Product already exist!",fg="red")
        return
    query = '''INSERT INTO products (pname,price,qnt) VALUES(?,?,?)'''
    cnt.execute(query,(txt_add_pname_final,txt_add_price_final,txt_add_qnt_final))
    cnt.commit()
    msg_add_pro.configure(text="Add Done!",fg="green")
    txt_add_pname.delete(0,"end")
    txt_add_price.delete(0,"end")
    txt_add_qnt.delete(0,"end")
    
    #-------Update users list----------
    
    update_list_products()

def add_product():
    global txt_add_pname,txt_add_price,txt_add_qnt,msg_add_pro,lstbox
    win_add_pro = tkinter.Toplevel(win_pro_manage)
    win_add_pro.title("Add Products")
    win_add_pro.geometry("500x400")
    win_add_pro.resizable(False,False)
    
    #----------lstbox for add user--------------
    
    lstbox = tkinter.Listbox(win_add_pro,width=100)
    lstbox.pack(pady=10)
    
    #----------widgets-------------------
    
    lbl_add_pname = tkinter.Label(win_add_pro,text="Product Name:")
    lbl_add_pname.pack()
    
    txt_add_pname = tkinter.Entry(win_add_pro,width=15)
    txt_add_pname.pack()
    
    lbl_add_price = tkinter.Label(win_add_pro,text="Product Price:")
    lbl_add_price.pack()
    
    txt_add_price = tkinter.Entry(win_add_pro,width=15)
    txt_add_price.pack()
    
    lbl_add_price = tkinter.Label(win_add_pro,text="Product Quantity:")
    lbl_add_price.pack()
    
    txt_add_qnt = tkinter.Entry(win_add_pro,width=50)
    txt_add_qnt.pack()
    
    msg_add_pro = tkinter.Label(win_add_pro,text="")
    msg_add_pro.pack()

    btn_add_pro = tkinter.Button(win_add_pro,text="ADD",activeforeground="blue",cursor="hand2",command=final_add_product)    
    btn_add_pro.pack()
    
    update_list_products()
    
    win_add_pro.mainloop()
    
    
def final_del_pro():
    txt_del_pid_final = txt_del_pid.get()
    txt_del_pname_final = txt_del_pname.get()
    if txt_del_pid_final == "" and txt_del_pname_final == "":
        msg_del_pro.configure(text="At least one blank must be filled!",fg="red")
        return
    if len(txt_del_pid_final) != 0 and len(txt_del_pname_final) != 0:
        msg_del_pro.configure(text="You must choose one methode not both!",fg="red")
        return
    if len(txt_del_pid_final) != 0 and len(txt_del_pname_final) == 0:
        query = '''SELECT * FROM products WHERE id=?'''
        result = cnt.execute(query,(txt_del_pid_final,))
        rows = result.fetchall()
        if len(rows) == 0:
            msg_del_pro.configure(text="ID doesn't exist!",fg="red")
        else:
            query = '''DELETE FROM products WHERE id = ?'''
            cnt.execute(query,(txt_del_pid_final,))
            cnt.commit()
            msg_del_pro.configure(text="Delete done!",fg="green")
            txt_del_pid.delete(0,"end")
            
            #------Update list--------
            
            update_list_products()
    if len(txt_del_pid_final) == 0 and len(txt_del_pname_final) != 0:
        query = '''SELECT * FROM products WHERE pname=?'''
        result = cnt.execute(query,(txt_del_pname_final,))
        rows = result.fetchall()
        if len(rows) == 0:
            msg_del_pro.configure(text="Product Name doesn't exist!",fg="red")
        else:
            query = '''DELETE FROM products WHERE pname = ?'''
            cnt.execute(query,(txt_del_pname_final,))
            cnt.commit()
            msg_del_pro.configure(text="Delete done!",fg="green")
            txt_del_pname.delete(0,"end")
            
            #------Update list--------
            
            update_list_products()
    
def del_product():
    global txt_del_pid,txt_del_pname,msg_del_pro,lstbox 
    win_del_pro = tkinter.Toplevel(win_pro_manage)
    win_del_pro.title("Delete Products")
    win_del_pro.geometry("500x400")
    win_del_pro.resizable(False,False)
    
    #----------lstbox for add user--------------
    
    lstbox = tkinter.Listbox(win_del_pro,width=100)
    lstbox.pack(pady=10)
    
    #----------widgets-------------------
    
    lbl_del_warn_pro = tkinter.Label(win_del_pro,text="To delete any Product, you can choose one of the following two methodes.",fg="blue")
    lbl_del_warn_pro.pack()
    
    lbl_del_pid = tkinter.Label(win_del_pro,text="Product ID:")
    lbl_del_pid.pack()
    
    txt_del_pid = tkinter.Entry(win_del_pro,width=15)
    txt_del_pid.pack()
    
    lbl_del_warn3 = tkinter.Label(win_del_pro,text="or")
    lbl_del_warn3.pack()
    
    lbl_del_pname = tkinter.Label(win_del_pro,text="Product Name:")
    lbl_del_pname.pack()
    
    txt_del_pname = tkinter.Entry(win_del_pro,width=15)
    txt_del_pname.pack()
    
    msg_del_pro = tkinter.Label(win_del_pro,text="")
    msg_del_pro.pack()

    btn_del_pro = tkinter.Button(win_del_pro,text="DELETE",activeforeground="blue",cursor="hand2",command=final_del_pro)    
    btn_del_pro.pack()
    
    update_list_products()
    
    win_del_pro.mainloop()

def final_edit_pro():
    txt_edit_price_final = txt_edit_price.get()
    txt_edit_qnt_final = txt_edit_qnt.get()
    txt_edit_id_final3 = txt_edit_pid.get()
    
    
    if txt_edit_price_final == "" and txt_edit_qnt_final == "":
        msg_edit_final_pro.configure(text="At least one blank must be filled!",fg="red")
        return
    
    if len(txt_edit_price_final) != 0 and len(txt_edit_qnt_final) != 0:  
        
        query = '''UPDATE products SET price = ? WHERE id = ?'''
        cnt.execute(query,(txt_edit_price_final,txt_edit_id_final3))
        cnt.commit()
        query = '''UPDATE products SET qnt = ? WHERE id = ?'''
        cnt.execute(query,(txt_edit_qnt_final,txt_edit_id_final3))
        cnt.commit()
        msg_edit_final_pro.configure(text="Edit done!",fg="green")
        txt_edit_price.delete(0,"end")
        txt_edit_qnt.delete(0,"end")
        
        update_list_products()
        
    if len(txt_edit_price_final) != 0 and len(txt_edit_qnt_final) ==0:
        
        query = '''UPDATE products SET price = ? WHERE id = ? '''
        cnt.execute(query,(txt_edit_price_final,txt_edit_id_final3))
        cnt.commit()
        
        msg_edit_final_pro.configure(text="Edit done!",fg="green")
        txt_edit_price.delete(0,"end")
        
        update_list_products()
    else:

        query = '''UPDATE products SET qnt = ? WHERE id = ? '''
        cnt.execute(query,(txt_edit_qnt_final,txt_edit_id_final3))
        cnt.commit()
        
        msg_edit_final_pro.configure(text="Edit done!",fg="green")
        txt_edit_qnt.delete(0,"end")
        
        update_list_products()
    
    
def next_step_pro():
    global lstbox,txt_edit_price,txt_edit_qnt,msg_edit_final_pro
    txt_edit_pid_final = txt_edit_pid.get()
    if txt_edit_pid_final == "":
        msg_edit_id_pro.configure(text="Please fill the blank!",fg="red")
        return
    query = '''SELECT * FROM products WHERE id = ?'''
    result = cnt.execute(query,(txt_edit_pid_final,))
    rows = result.fetchall()
    if len(rows) == 0:
        msg_edit_id_pro.configure(text="ID doesn't exist!",fg="red")
        return
    #----------------------------------------------------
    win_edit_final_pro = tkinter.Toplevel(win_edit_pro)
    win_edit_final_pro.title("Final Edit")
    win_edit_final_pro.geometry("500x400")
    
    #----------lstbox for edit user--------------

    lstbox = tkinter.Listbox(win_edit_final_pro,width=100)
    lstbox.pack(pady=10)
    
    #----------------widgets-----------------------
    lbl_edit_final_pro = tkinter.Label(win_edit_final_pro,text="You can change Product's Name or Product's Price or both of them for any Product.",fg="blue")
    lbl_edit_final_pro.pack(pady=5)
    
    lbl_edit_price = tkinter.Label(win_edit_final_pro,text="Change Price:")
    lbl_edit_price.pack(pady=5)
    
    txt_edit_price = tkinter.Entry(win_edit_final_pro,width=15)
    txt_edit_price.pack()
    
    lbl_edit_qnt = tkinter.Label(win_edit_final_pro,text="Change Quantity:")
    lbl_edit_qnt.pack(pady=5)
    
    txt_edit_qnt = tkinter.Entry(win_edit_final_pro,width=50)
    txt_edit_qnt.pack()
    
    msg_edit_final_pro = tkinter.Label(win_edit_final_pro,text="")
    msg_edit_final_pro.pack()
    
    btn_edit_final_pro = tkinter.Button(win_edit_final_pro,text="Edit",activeforeground="blue",cursor="hand2",command=final_edit_pro)
    btn_edit_final_pro.pack(pady=5)
    
    update_list_products()
    
    win_edit_final_pro.mainloop()
    
    
def edit_product():
    global win_edit_pro,lstbox,txt_edit_pid,msg_edit_id_pro
    win_edit_pro = tkinter.Toplevel(win_pro_manage)
    win_edit_pro.title("Edit Products")
    win_edit_pro.geometry("500x400")
    
    #----------lstbox for edit user--------------

    lstbox = tkinter.Listbox(win_edit_pro,width=100)
    lstbox.pack(pady=10)
    
    #----------------widgets-----------------------
    
    lbl_msg_edit_pro = tkinter.Label(win_edit_pro,text="To edit Product's Information ,input Product's ID form table above or your Database. ",fg="blue")
    lbl_msg_edit_pro.pack()
    
    lbl_edit_pid = tkinter.Label(win_edit_pro,text="Product ID:")
    lbl_edit_pid.pack()
    
    txt_edit_pid = tkinter.Entry(win_edit_pro,width=15)
    txt_edit_pid.pack()
    
    msg_edit_id_pro = tkinter.Label(win_edit_pro,text="")
    msg_edit_id_pro.pack()
    
    btn_edit_pro = tkinter.Button(win_edit_pro,text="Next Step",activeforeground="blue",cursor="hand2",command=next_step_pro)
    btn_edit_pro.pack()
    
    
    update_list_products()
    
    win_edit_pro.mainloop()
    
    
def product_manage():
    global win_pro_manage
    win_pro_manage = tkinter.Toplevel(win_admin)
    win_pro_manage.title("Products Management")
    win_pro_manage.geometry("300x200")
    win_pro_manage.resizable(False,False)
    
    #--------widgets-----------
    lbl_pmanage_question = tkinter.Label(win_pro_manage,text="What do you want to do?",fg="blue")
    lbl_pmanage_question.pack(pady=30)
    
    btn_pmanage_add = tkinter.Button(win_pro_manage,text="Add Product",activeforeground="blue",cursor="hand2",command=add_product)
    btn_pmanage_add.place(x=20,y=100)
    
    btn_pmanage_del = tkinter.Button(win_pro_manage,text="Delete Product",activeforeground="blue",cursor="hand2",command=del_product)
    btn_pmanage_del.place(x=110,y=100)
    
    btn_pmanage_edit = tkinter.Button(win_pro_manage,text="Edit Product",activeforeground="blue",cursor="hand2",command=edit_product)
    btn_pmanage_edit.place(x=210,y=100)
    
    
    
    win_pro_manage.mainloop()
    
def buy_product():
    win_buy_sale = tkinter.Toplevel(win_sale)
    win_buy_sale.title("Purchase History")
    win_buy_sale.geometry("650x400")
    lstbox_buy = tkinter.Listbox(win_buy_sale,width=200)
    lstbox_buy.pack(pady=10)
    
    query = '''SELECT users.username,products.pname,products.price,final_shop.qnt,final_shop.date
    FROM final_shop
    JOIN
    users
    ON final_shop.uid=users.id
    JOIN
    products
    ON final_shop.pid = products.id
    '''
    result = cnt.execute(query)
    rows = result.fetchall()
    for item in rows:
        total_price = item[2]*item[3]
        lstbox_buy.insert("end",f"Username= {item[0]} // Product Name= {item[1]} // Quantity= {item[3]} // Total Price= {total_price} // Date= {item[4]}" )
    win_buy_sale.mainloop()
    
    
def best_buyer():
    win_best_buyer = tkinter.Toplevel(win_sale)
    win_best_buyer.title("Best Buyer")
    win_best_buyer.geometry("300x100")
    win_best_buyer.resizable(False,False)
    
    lstbox_best_buyer = tkinter.Listbox(win_best_buyer,width=100)
    lstbox_best_buyer.pack(pady=10)
    
    query = '''SELECT users.username, SUM(final_shop.qnt) as total_sales
            FROM final_shop
            JOIN users
            ON final_shop.uid = users.id
            GROUP BY users.username
            ORDER BY total_sales DESC
            LIMIT 10'''
    result = cnt.execute(query)
    rows = result.fetchall()
    lstbox_best_buyer.insert("end",f"The Best Buyer is: {rows[0][0]}  With Quantity: {rows[0][1]}")
    
    win_best_buyer.mainloop()
    
def best_product():
    win_best_sale = tkinter.Toplevel(win_sale)
    win_best_sale.title("Best Selling Product")
    win_best_sale.geometry("300x100")
    win_best_sale.resizable(False,False)
    
    lstbox_best = tkinter.Listbox(win_best_sale,width=100)
    lstbox_best.pack(pady=10)
    
    query = '''SELECT products.pname, SUM(final_shop.qnt) as total_sales
            FROM final_shop
            JOIN products
            ON final_shop.pid = products.id
            GROUP BY products.pname
            ORDER BY total_sales DESC
            LIMIT 10'''
    result = cnt.execute(query)
    rows = result.fetchall()
    lstbox_best.insert("end",f"The Best Selling Product is: {rows[0][0]}  With Quantity: {rows[0][1]}")
    
    win_best_sale.mainloop()
    
def show_details_purchase():
    txt_purch_sale_final = txt_purch_sale.get()
    if txt_purch_sale_final == "":
        lbl_msg_purch3.configure(text="Please fill the blank!",fg="red")
        return
    
    if txt_purch_sale_final not in rows_final_purch:
        lbl_msg_purch3.configure(text="Product doesn't exist!",fg="red")
        return
    
    #--------win show details info---------------
    
    win_purch_sale_final = tkinter.Toplevel(win_purch_sale)
    win_purch_sale_final.title("Details")
    win_purch_sale_final.geometry("700x200")
    win_purch_sale_final.resizable(False,False)
    
    lstbox_purch_final = tkinter.Listbox(win_purch_sale_final,width=200)
    lstbox_purch_final.pack(pady=10)
    
    query = '''SELECT users.username,products.pname,products.price,final_shop.qnt,final_shop.date
    FROM final_shop
    JOIN
    users
    ON final_shop.uid=users.id
    JOIN
    products
    ON final_shop.pid = products.id 
    '''
    result = cnt.execute(query)
    rows_purch = result.fetchall()
    for item in rows_purch:
        if txt_purch_sale_final in item:
            total_price = item[2]*item[3]
            lstbox_purch_final.insert("end",f"Username= {item[0]} // Product Name= {item[1]} // Purchased Quantity= {item[3]} // Total Price= {total_price} // Date= {item[4]}" )
    
    win_purch_sale_final.mainloop()
    
def purchased_product():
     global rows_final_purch,lbl_msg_purch3,txt_purch_sale,win_purch_sale
     win_purch_sale = tkinter.Toplevel(win_sale)
     win_purch_sale.title("Purchased Products")
     win_purch_sale.geometry("400x300")
     win_purch_sale.resizable(False,False)
     lstbox_purch = tkinter.Listbox(win_purch_sale,width=100)
     lstbox_purch.pack(pady=10)
     
     query = '''SELECT products.pname,products.qnt
     FROM final_shop
     JOIN
     products
     ON final_shop.pid=products.id
     '''
     result = cnt.execute(query)
     rows = result.fetchall()
     rows_final_purch = dict(rows)
     for k,v in rows_final_purch.items():
         lstbox_purch.insert("end",f"Product Name= {k} // Current Quantity= {v}" )  
     lbl_msg_purch = tkinter.Label(win_purch_sale,text="For purchased products details input the Product Name form table above",fg="blue")
     lbl_msg_purch.pack()
     
     lbl_msg_purch2 = tkinter.Label(win_purch_sale,text="Product Name:")
     lbl_msg_purch2.pack()
     
     txt_purch_sale = tkinter.Entry(win_purch_sale,width=15)
     txt_purch_sale.pack()
     
     lbl_msg_purch3 = tkinter.Label(win_purch_sale,text="")
     lbl_msg_purch3.pack()
     
     btn_purch_sale = tkinter.Button(win_purch_sale,text="Show Details",activeforeground="blue",cursor="hand2",command=show_details_purchase)
     btn_purch_sale.pack()
     
     win_purch_sale.mainloop()

def show_details():
    txt_cst_sale_final = txt_cst_sale.get()
    if txt_cst_sale_final == "":
        lbl_msg_cst3.configure(text="Please fill the blank!",fg="red")
        return
    
    if txt_cst_sale_final not in rows_final:
        lbl_msg_cst3.configure(text="Username doesn't exist!",fg="red")
        return
    
    #--------win show details info---------------
    
    win_cst_sale_final = tkinter.Toplevel(win_sale)
    win_cst_sale_final.title("Details")
    win_cst_sale_final.geometry("700x200")
    win_cst_sale_final.resizable(False,False)
    
    lstbox_cst_final = tkinter.Listbox(win_cst_sale_final,width=200)
    lstbox_cst_final.pack(pady=10)
    
    query = '''SELECT users.username,products.pname,products.price,final_shop.qnt,final_shop.date
    FROM final_shop
    JOIN
    users
    ON final_shop.uid=users.id
    JOIN
    products
    ON final_shop.pid = products.id 
    '''
    result = cnt.execute(query)
    rows_cst = result.fetchall()
    for item in rows_cst:
        if txt_cst_sale_final in item:
            total_price = item[2]*item[3]
            lstbox_cst_final.insert("end",f"Username= {item[0]} // Product Name= {item[1]} // Quantity= {item[3]} // Total Price= {total_price} // Date= {item[4]}" )
    win_cst_sale_final.mainloop()
    
def custumers():
    global rows_final,lbl_msg_cst3,txt_cst_sale,win_cst_sale
    win_cst_sale = tkinter.Toplevel(win_sale)
    win_cst_sale.title("Custumers")
    win_cst_sale.geometry("400x300")
    win_cst_sale.resizable(False,False)
    lstbox_cst = tkinter.Listbox(win_cst_sale,width=100)
    lstbox_cst.pack(pady=10)
    
    query = '''SELECT users.username,users.address
    FROM final_shop
    JOIN
    users
    ON final_shop.uid=users.id
    '''
    result = cnt.execute(query)
    rows = result.fetchall()
    rows_final = dict(rows)
    for k,v in rows_final.items():
        lstbox_cst.insert("end",f"Username= {k} // Address= {v}" )  
    lbl_msg_cst = tkinter.Label(win_cst_sale,text="For purchase details input the Username form table above",fg="blue")
    lbl_msg_cst.pack()
    
    lbl_msg_cst2 = tkinter.Label(win_cst_sale,text="Username:")
    lbl_msg_cst2.pack()
    
    txt_cst_sale = tkinter.Entry(win_cst_sale,width=15)
    txt_cst_sale.pack()
    
    lbl_msg_cst3 = tkinter.Label(win_cst_sale,text="")
    lbl_msg_cst3.pack()
    
    btn_cst_sale = tkinter.Button(win_cst_sale,text="Show Details",activeforeground="blue",cursor="hand2",command=show_details)
    btn_cst_sale.pack()
    
    win_cst_sale.mainloop()
def product_sale():
    global win_sale
    win_sale = tkinter.Toplevel(win_admin)
    win_sale.title("Sales Management")
    win_sale.geometry("300x300")
    win_sale.resizable(False,False)
    
    #--------widgets-----------
    lbl_sale_question = tkinter.Label(win_sale,text="What do you want to know?",fg="blue")
    lbl_sale_question.pack(pady=30)
    
    btn_sale_buy = tkinter.Button(win_sale,text="Purchase History",activeforeground="blue",cursor="hand2",command=buy_product)
    btn_sale_buy.place(x=20,y=100)
    
    btn_sale_best = tkinter.Button(win_sale,text=" The Best Selling Product",activeforeground="blue",cursor="hand2",command=best_product)
    btn_sale_best.place(x=140,y=100)
    
    btn_sale_cst = tkinter.Button(win_sale,text="Customers",activeforeground="blue",cursor="hand2",command=custumers)
    btn_sale_cst.place(x=20,y=150) 
    
    btn_sale_purchased = tkinter.Button(win_sale,text=" Purchased Products",activeforeground="blue",cursor="hand2",command=purchased_product)
    btn_sale_purchased.place(x=140,y=150) 
    
    btn_sale_buyer = tkinter.Button(win_sale,text=" The Best Buyer",activeforeground="blue",cursor="hand2",command=best_buyer)
    btn_sale_buyer.place(x=20,y=200) 
    
    win_sale.mainloop()
    
    
    win_sale.mainloop()
 
def sale_date_history():
    win_date_his = tkinter.Toplevel(win_sale_date)
    win_date_his.title("Details")
    win_date_his.geometry("700x200")
    win_date_his.resizable(False,False)
    
    lstbox_sale_date = tkinter.Listbox(win_date_his,width=200)
    lstbox_sale_date.pack(pady=10)
    
    query = '''SELECT users.username,products.pname,products.price,final_shop.qnt,final_shop.date
    FROM final_shop
    JOIN
    users
    ON final_shop.uid=users.id
    JOIN
    products
    ON final_shop.pid = products.id 
    '''
    result = cnt.execute(query) 
    rows_date = result.fetchall()
    for item in rows_date:
            lstbox_sale_date.insert("end",f"Date= {item[4]} // Product Name= {item[1]} // Quantity= {item[3]}" )
    win_date_his.mainloop()

def best_date():
    win_best_date = tkinter.Toplevel(win_sale_date)
    win_best_date.title("The Best Selling Date")
    win_best_date.geometry("500x100")
    win_best_date.resizable(False,False)
    
    lstbox_best_date = tkinter.Listbox(win_best_date,width=200)
    lstbox_best_date.pack(pady=10)
    
    query = '''SELECT final_shop.date, SUM(final_shop.qnt) as total_sales
            FROM final_shop
            JOIN products
            ON final_shop.pid = products.id
            GROUP BY final_shop.date
            ORDER BY total_sales DESC
            LIMIT 10'''
    result = cnt.execute(query)
    rows = result.fetchall()

    lstbox_best_date.insert("end",f"The Best Selling Date is:  {rows[0][0]}  With Quantity:  {rows[0][1]}" )
    
    win_best_date.mainloop()
   


def show_details_pr():
    txt_best_period_start_final = txt_best_period_start.get()
    txt_best_period_end_final = txt_best_period_end.get()
    if txt_best_period_start_final == "" and txt_best_period_end_final == "":
        lbl_msg_period3.configure(text="Please fill the blanks!",fg="red")
        return
    if txt_best_period_start_final == "" or txt_best_period_end_final == "":
        lbl_msg_period3.configure(text="Please fill the all blanks!",fg="red")
        return
    
    win_best_date_pr_final = tkinter.Toplevel(win_best_date_pr)
    win_best_date_pr_final.title("The Best Selling Products based on Period")
    win_best_date_pr_final.geometry("500x200")
    win_best_date_pr_final.resizable(False,False)
    
    lbl_msg_best_date_pr = tkinter.Label(win_best_date_pr_final,text="Number one is the best seller product in this period of time! ",fg="green")
    lbl_msg_best_date_pr.pack()
    
    lstbox_best_date_pr = tkinter.Listbox(win_best_date_pr_final,width=200)
    lstbox_best_date_pr.pack(pady=10)
    
    query = '''SELECT products.pname, SUM(final_shop.qnt) as total_sales
           FROM final_shop
           JOIN products
           ON final_shop.pid = products.id
           WHERE final_shop.date BETWEEN ? AND ?
           GROUP BY products.pname
           ORDER BY total_sales DESC
           LIMIT 10'''
           
    result = cnt.execute(query,(txt_best_period_start_final,txt_best_period_end_final))    
    rows = result.fetchall()
    rows = dict(rows)
    sorted_qnt = sorted(rows.items(), key=lambda x:x[1], reverse=True)
    
    for item in sorted_qnt:
        lstbox_best_date_pr.insert("end",f"Product Name= {item[0]}   //   With Quantity = {item[1]}")

    win_best_date_pr_final.mainloop()
    
def best_date_period():
    global win_best_date_pr,txt_best_period_start,txt_best_period_end,lbl_msg_period3
    win_best_date_pr = tkinter.Toplevel(win_sale_date)
    win_best_date_pr.title("The Best Selling Products based on Preiod")
    win_best_date_pr.geometry("400x200")
    win_best_date_pr.resizable(False,False)
    
    lbl_msg_period = tkinter.Label(win_best_date_pr,text="Please input your intended Period LIKE EXAMPLE BELOW!",fg="blue")
    lbl_msg_period.pack(pady=10)
    
    lbl_msg_period2 = tkinter.Label(win_best_date_pr,text="Start_date and End_date: year-month-day(1998-02-08)",fg="red")
    lbl_msg_period2.pack()
    
    lbl_msg_period_start = tkinter.Label(win_best_date_pr,text="Start_date:")
    lbl_msg_period_start.pack()
    
    
    txt_best_period_start = tkinter.Entry(win_best_date_pr,width=15)
    txt_best_period_start.pack()
    
    lbl_msg_period_end = tkinter.Label(win_best_date_pr,text="End_date:")
    lbl_msg_period_end.pack()
    
    txt_best_period_end = tkinter.Entry(win_best_date_pr,width=15)
    txt_best_period_end.pack()
    
    lbl_msg_period3 = tkinter.Label(win_best_date_pr,text="")
    lbl_msg_period3.pack() 
    
    btn_best_period = tkinter.Button(win_best_date_pr,text="Show Details",activeforeground="blue",cursor="hand2",command=show_details_pr)
    btn_best_period.pack()
    
    win_best_date_pr.mainloop()
    
def sale_date():
    global win_sale_date
    win_sale_date = tkinter.Toplevel(win_admin)
    win_sale_date.title("Sales Date Management")
    win_sale_date.geometry("300x300")
    win_sale_date.resizable(False,False)
    
    #--------widgets-----------
    
    lbl_sale_date_question = tkinter.Label(win_sale_date,text="What do you want to know?",fg="blue")
    lbl_sale_date_question.pack(pady=30)
    
    btn_sale_buy = tkinter.Button(win_sale_date,text="Sales Date History",activeforeground="blue",cursor="hand2",command=sale_date_history)
    btn_sale_buy.place(x=20,y=100)
    
    btn_best_date = tkinter.Button(win_sale_date,text="The Best Selling Date",activeforeground="blue",cursor="hand2",command=best_date)
    btn_best_date.place(x=140,y=100)
    
    btn_best_date_pr = tkinter.Button(win_sale_date,text="The Best Selling Products based on Period",activeforeground="blue",cursor="hand2",command=best_date_period)
    btn_best_date_pr.place(x=20,y=150)
    
    win_sale_date.mainloop()
    
#------------Admin Panel-----------------------------------
    
def admin_panel():
    global txt_pname,txt_price,txt_qnt,lbl_msg_admin,win_admin
    win_admin = tkinter.Toplevel(win)
    win_admin.title("Admin Panel")
    win_admin.geometry("350x250")
    win_admin.resizable(False,False)
    
    #-----------widgets-----------------
    
    btn_admin_usersinfo = tkinter.Button(win_admin,text="Users Information",activeforeground="blue",cursor="hand2",command=user_info)
    btn_admin_usersinfo.place(x=30,y=50)
    
    btn_admin_umanage = tkinter.Button(win_admin,text="Users Management",activeforeground="blue",cursor="hand2",command=user_manage)
    btn_admin_umanage.place(x=200,y=50)
    
    btn_admin_pinfo = tkinter.Button(win_admin,text="Products Information",activeforeground="blue",cursor="hand2",command=product_info)
    btn_admin_pinfo.place(x=30,y=90)
    
    btn_admin_pmanage = tkinter.Button(win_admin,text="Products Management",activeforeground="blue",cursor="hand2",command=product_manage)
    btn_admin_pmanage.place(x=200,y=90)
    
    btn_admin_sale = tkinter.Button(win_admin,text="Sales Management",activeforeground="blue",cursor="hand2",command=product_sale)
    btn_admin_sale.place(x=30,y=130)
    
    btn_admin_sale_date = tkinter.Button(win_admin,text="Sales Date Management",activeforeground="blue",cursor="hand2",command=sale_date)
    btn_admin_sale_date.place(x=200,y=130)
    
    win_admin.mainloop()

    

#---------------   M  A  I  N--------------------

win = tkinter.Tk()
win.title("SHOP")
win.geometry("400x300")
win.resizable(False,False)

lbl_user = tkinter.Label(win,text="Username: ")
lbl_user.pack(pady=10)
txt_user = tkinter.Entry(win,width=15)
txt_user.pack()

lbl_pass = tkinter.Label(win,text="Password: ")
lbl_pass.pack()
txt_pass = tkinter.Entry(win,width=15)
txt_pass.pack()

lbl_msg = tkinter.Label(win,text="")
lbl_msg.pack(pady=10)

btn_login = tkinter.Button(win,text="Login",activeforeground="blue",cursor="hand2",command=login)
btn_login.place(x=110,y=140)

btn_logout = tkinter.Button(win,text="Logout",state = "disabled",activeforeground="blue",cursor="hand2",command=logout)
btn_logout.place(x=170,y=140)

btn_submit = tkinter.Button(win,text="Submit",activeforeground="blue",cursor="hand2",command=submit)
btn_submit.place(x=240,y=140)

btn_shop = tkinter.Button(win,text="Shop",state="disabled",activeforeground="blue",cursor="hand2",command=shop)
btn_shop.place(x=110,y=170)

my_shop_btn = tkinter.Button(win,text="My shop",state="disabled",activeforeground="blue",cursor="hand2",command=my_shop)
my_shop_btn.place(x=170,y=170)

admin_btn = tkinter.Button(win,text="Admin Panel",state="disabled",activeforeground="blue",cursor="hand2",command=admin_panel)
admin_btn.place(x=240,y=170)

win.mainloop() 



