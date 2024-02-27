from tkinter import *
import tkinter.messagebox as mb 
import mysql.connector 

mydb = mysql.connector.connect(user='root', password='iamcool1@3',
                              host='127.0.0.1',
                              database='address_book')
cursor = mydb.cursor()

root = Tk()
root.geometry('700x550')
root.resizable(0, 0)

lf_bg = 'Gray70'
cf_bg = 'Gray57'
rf_bg = 'Gray35'
frame_font = ('Garamond', 14)
heading_label = Label(root, text='CONTACT BOOK', font=("Noto Sans CJK TC", 15, "bold"), bg="Black", fg="White")
left_frame = Frame(root, bg=lf_bg)
center_frame = Frame(root, bg=cf_bg)
right_frame = Frame(root, bg=rf_bg)
name_strvar = StringVar()
phone_strvar = StringVar()
email_strvar = StringVar()
search_strvar = StringVar()
Label(left_frame, text='Name', bg=lf_bg, font=frame_font).place(relx=0.3, rely=0.05)
name_entry = Entry(left_frame, width=15, font=("Verdana", 11), textvariable=name_strvar)
name_entry.place(relx=0.1, rely=0.1)
Label(left_frame, text='Phone no.', bg=lf_bg, font=frame_font).place(relx=0.23, rely=0.2)
phone_entry = Entry(left_frame, width=15, font=("Verdana", 11), textvariable=phone_strvar)
phone_entry.place(relx=0.1, rely=0.25)
Label(left_frame, text='Email', bg=lf_bg, font=frame_font).place(relx=0.3, rely=0.35)
email_entry = Entry(left_frame, width=15, font=("Verdana", 11), textvariable=email_strvar)
email_entry.place(relx=0.1, rely=0.4)
Label(left_frame, text='Address', bg=lf_bg, font=frame_font).place(relx=0.28, rely=0.5)
address_entry = Text(left_frame, width=15, font=("Verdana", 11), height=5)

def clear_fields():
    global name_strvar,email_strvar,phone_strvar,address_entry
    name_strvar.set("")
    email_strvar.set("")
    phone_strvar.set("")
    address_entry.delete(1.0,END)

def list_contacts():
    global cursor
    cursor.execute("SELECT NAME FROM ADDRESS_BOOK.CONTACTS")
    address_list = cursor.fetchall()
    listbox.delete(0,END)
    for address in address_list:
        listbox.insert(END,address)

        

def view_record():
    global mydb
    search_string = listbox.get(ACTIVE)
    print(type(search_string))
    print(search_string)
    cursor.execute("select * from address_book.contacts where name like %s",("%"+ search_string[0] + "%", ))
    search_list = cursor.fetchall()[0]
    name_strvar.set(search_list[0])
    phone_strvar.set(search_list[2])
    email_strvar.set(search_list[1])
    address_entry.delete(1.0,END)
    address_entry.insert(END,search_list[3])
    
    

def search():
    global mydb
    search_string = str(search_strvar.get())
    cursor.execute("select * from address_book.contacts where name like %s",("%"+ search_string + "%", ))
    search_list = cursor.fetchall()
    listbox.delete(0,END)
    for item in search_list:
        listbox.insert(END,item[0])

def submit_record():
    global name_strvar,email_strvar,phone_strvar,address_entry
    global cursor
    name,email,phone,address = name_strvar.get(),email_strvar.get(),phone_strvar.get(),address_entry.get(1.0,END)
    if name == "" or email == "" or phone == "" or address == "" :
        mb.showerror("Error !", "Please fill in all the fields")
    else:
        insert_query = "insert into address_book.contacts(name,email,phone_number,address) values (%s,%s,%s,%s)"
        cursor.execute(insert_query,(name,email,phone,address))
        mydb.commit()
        mb.showinfo("Contact added","Contact stored successfully" )
        clear_fields()
        list_contacts()

def delete_all_records():
    global listbox, connector, cursor
    if not listbox.get(ACTIVE) :
        mb.showerror("No item selected", "You have not selected any items !")
    
    cursor.execute("delete from address_book.contacts ")
    mydb.commit()
    mb.showinfo("Contact deleted", "All contacts has been deleted")
    listbox.delete(0,END)
    list_contacts()

def delete_record():
    global listbox, connector, cursor
    if not listbox.get(ACTIVE) :
        mb.showerror("No item selected", "You have not selected any items !")
    
    cursor.execute("delete from address_book.contacts where name=%s",(listbox.get(ACTIVE)))
    mydb.commit()
    mb.showinfo("Contact deleted", "The desired contact has been deleted")
    listbox.delete(0,END)
    list_contacts()





search_entry = Entry(center_frame,width=15,font=("Verdana",12),textvariable=search_strvar).place(relx=0.13,rely=0.04)
Button(center_frame,text="Search",font=frame_font,width=15,command=search).place(relx=0.13,rely=0.14)
Button(center_frame,text="Add Record",font=frame_font,width=15,command=submit_record).place(relx=0.13,rely=0.24)
Button(center_frame,text="View Record",font=frame_font,width=15,command = view_record).place(relx=0.13,rely=0.34)
Button(center_frame,text="Clear Fields",font=frame_font,width=15,command=clear_fields).place(relx=0.13,rely=0.44)
Button(center_frame,text="Delete Record",font=frame_font,width=15,command=delete_record).place(relx=0.13,rely=0.54)
Button(center_frame,text="Delete All Records",font=frame_font,width=15,command=delete_all_records).place(relx=0.13,rely=0.64)
Label(right_frame,text="Saved Contacts",font=("Noto Sans CJK TC", 14),bg=rf_bg).place(relx=0.24,rely=0.04)
listbox = Listbox(right_frame,selectbackground="SkyBlue",bg="Gainsboro",font=("Helvetica",12),height=20,width=25)
listbox.place(relx=0.1,rely=0.15)
address_entry.place(relx=0.1, rely=0.55)
heading_label.pack(side=TOP, fill=X)
left_frame.place(relx=0, relheight=1, y=30, relwidth=0.3)
center_frame.place(relx=0.3, relheight=1, y=30, relwidth=0.3)
right_frame.place(relx=0.6, relheight=1, y=30, relwidth=0.4)

list_contacts()
root.mainloop()

