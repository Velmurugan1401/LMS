#!/usr/bin/env python
# coding: utf-8

# In[40]:


from os.path import exists
import pandas as pd
from pandas import json_normalize
import json
import re
import uuid
import logging
import datetime

auth = {"Username":"Ravi", "Password":"1234"}
session_id = False

# Json path of books list
json_store_path = "C:/Users/VPS/Desktop/Tasks/LMS/LMS.json"

# Json path of borrows list
user_store_path = "C:/Users/VPS/Desktop/Tasks/LMS/Users.json"
logging.basicConfig(filename = "newfile.log", format = '%(asctime)s %(message)s')
book_data = {}
user_data = {}


# Checking credebtial for admin -------------------
def authchcek(username, password):
    
    global session_id
    
    # Check admin authentication
    logging.info("Checking gradantial")
    print("Checking credential for admin")
    if username == auth['Username'] and password == auth['Password']:
        session_id = True
        logging.info("Admin login successfully")
        return "Admin login successfully"
    else:
        session_id = False
        return "Invalit Username or password"

    
# Books Add section -----------------------------
def addbook():
    
    print("Enter book add section")
    global session_id
    content = {}
    
    # Check user login or not
    if session_id:
        print("Authendication sucess")
    else:
        return "Invalit authentication"
    
    # check the path file exits or not
    logging.info("Check the json path")
    if exists(json_store_path):
        
        # Get Books list and set
        book_data = open(json_store_path, 'r')
        book_data = json.load(book_data)
    else:
        book_data = {}

    Section_name = input("Enter the book section name: ")
    Section_name = Section_name if Section_name else "ALL_INONE"
    
    # Check section name found or not in books list
    if Section_name in book_data:
        content = book_data[Section_name] 
    else:
        print("Your enter section Not Found")
       
    # Get the book detalis
    Book_name = input("Enter the book Name: ")
    Book_count = input("How many books: ")
    content[Book_name] = Book_count
    book_data[Section_name] = content
    
    # add the books in the library
    Json_data = json.dumps(book_data, indent = 4)
    
    # Writing to sample.json
    with open(json_store_path, "w") as outfile:
         outfile.write(Json_data)
         outfile.close()   
    print("\n", Book_name, " Book added successfully to the section", Section_name)

    
# Books Search section -----------------------------
def Search_book():
    
    print("Enter the book search section")
    logging.info("Enter book searching function")
    
    # search the books in the library
    global json_store_path
    book_name = input("Enter the book name: ")
    if exists(json_store_path):
        with open(json_store_path) as f:
             data = json.load(f)
        Book = list(data.keys())
        Book_list = []
        for i in Book:
            Book_list = Book_list + list(data[i].keys())
        regexs = re.compile(".*"+ str(book_name) +"")
        newlist = list(filter(regexs.match, Book_list)) 
        print("Your searching book list is: ", newlist)
        
    else:
        print("No books Found!")
        return False
        
        
# Books list section -----------------------------
def listbook():
    logging.info("Enter books list function")
    
    global json_store_path
    if exists(json_store_path):
        with open(json_store_path) as f:
             data = json.load(f)
        df = list(data.keys())
        print("The below books are available in library")
        for i in df:
            print("\n", i, ":")
            for j,k in zip(list(data[i].keys()),list(data[i].values())):
                
                print (j, ", COUNT : ", k)
           # print(i, ":", list(data[i].keys()))
        
        return ""
    else:
        print("No books Found!")
        

# Books borrowers section -----------------------------
def listuser():
    
    global user_data
    if exists(user_store_path):
        user_data = open(user_store_path, 'r')
        user_data = json.load(user_data)
        for i in list(user_data.keys()):
            userdatas = list(user_data[i].keys())
            print("\nUser name : ", user_data[i]["name"])
            for j in userdatas[1:]:
                if user_data[i][j]["status"]:
                    print("The user return the", j, "book his return date : ", user_data[i][j]["returnDate"])
                else:
                    print("The user borrow the", j, "book his return date : ", user_data[i][j]["returnDate"])
                if "Fine_amound" in user_data[i][j]:
                    print("He has not return the book in specific date so he receive his fine amount :", 100)
                else:
                    print("No fine amount on this book")
    else:
        user_data = {}
        print("\n No users found")

        
# Book exits or not--------------------------
def Bookinout(section_name, book_name):
    
    # search the books in the library
    logging.info("Checking book available or not")
    global json_store_path
    if exists(json_store_path):
        with open(json_store_path) as f:
             data = json.load(f)
        if section_name in data:
            
            # Check user borrow book is availabel or not
            if book_name in data[section_name]:
                
                # Check book count greater than zero or not
                if int(data[section_name][book_name]) != 0:
                    
                    return True
                else:
                    logging.info("No stock in library")
                    print("No stock in library")
                    return False
            else:
                print("No book Found")
                return False
    else:
        print("Check the path")
        return False

    
# Books borrow section -----------------------------
def borrowBook():
    
    global json_store_path
    global user_data
    global user_store_path
    
    listofbooks = listbook()
    print(listofbooks)
    
    # List all the books in the dictionary
    now = datetime.datetime.now()
    borrow_date = now.strftime("%d-%m-%Y")
    section_name = input("Enter the section name: ")
    book_name = input("Enter the book Name: ")
    
    #U_res = input("If you want to search Books Yes (or) No: \n")
    U_res = "no"
    if U_res == "Yes" or U_res == "yes":
        
        # Call Search function sent book name
        list_book = Search_book(section_name, book_name)
    else:
        bookIn = Bookinout(section_name, book_name)
        
        if bookIn:
            user_res = input("If u already in user yes or no : ")
            
            if user_res == "yes" or user_res == "Yes":
                
                # if user already exits get user id from user and update the user
                user_id = input("\n Enter your user id: ")
                returndate = input("Enter Return date Format:DD/MM/YYYY: ")
                obj = {"book_name":book_name, "return_date":returndate, "borrow_date":str(borrow_date)}
                exitsUser(user_id, obj)
                bookborrow(section_name, book_name)
                
            else:
                
                # if new user generate new id for user
                if exists(user_store_path):
                    users_info = open(user_store_path, 'r')
                    users_info = json.load(users_info)
                else:
                    users_info = {}
                    
                user_data = users_info
                user_id = str(uuid.uuid4())
                user_name = input("Enter Your name: ") 
                return_date = input("Enter Return date Format:DD/MM/YYYY: ")
                user_data[user_id] = {"name":user_name, book_name:{"returnDate":return_date,"borrow_date":str(borrow_date),"status":False}}
               
                # add the books in the library
                json_data = json.dumps(user_data, indent = 4)

                # Writing to sample.json
                with open(user_store_path, "w") as outfile:
                     outfile.write(json_data)
                     outfile.close()
                bookborrow(section_name, book_name)
                print("Your user id: ", user_id)
        else:
            print("No book Found")
            

# Already user exits or not checking --------------------
def exitsUser(user_id, obj):
    
    content = {}
    Users = open(user_store_path, 'r')
    Users = json.load(Users)    
    content = Users[user_id]
    
    # Update the borrower list 
    print("Update the exits user")
    logging.info("User exits add the books")
    content[obj["book_name"]] = {"returnDate":obj["return_date"],"borrow_date":obj["borrow_date"],"status":False}
    Users[user_id] = content
    Json_data = json.dumps(Users, indent = 4)
    
    # Store the borrower list
    print("Store the user specific location")
    with open(user_store_path, "w") as outfile:
        outfile.write(Json_data)
        outfile.close()


# User able to check there borrow book-------------
def checkfineamount():
    
    global user_data
    user_id = input("Enter your user id: ")
    if exists(user_store_path):
        user_data = open(user_store_path, 'r')
        user_data = json.load(user_data)
        userdatas = list(user_data[user_id].keys())
        print("\nUser name : ", user_data[user_id]["name"])
        for j in userdatas[1:]:
            if user_data[user_id][j]["status"]:
                print("Book name: ", j, "Return date: ", user_data[user_id][j]["returnDate"], "Status: Book Already Returned" )
            else:
                print("Book name: ", j, ", Return date: ", user_data[user_id][j]["returnDate"], ", Status: Book Not Return")
            if "Fine_amound" in user_data[user_id][j]:
                print("Fine amount: ", 100)
            else:
                print("Fine amount: ", 0)
    else:
        user_data = {}
        print("\n No users found")
        
        
# Change Book count --------------------
def bookborrow(section_name, book_name):
    
    global json_store_path
    Books = open(json_store_path, 'r')
    Books = json.load(Books)
    
    # Get book from book list so reduce count of book
    print("Reduce book when use borrow one book")
    Books[section_name][book_name] = str(int(Books[section_name][book_name]) - 1)
    Json_data = json.dumps(Books, indent = 4)
    with open(json_store_path, "w") as outfile:
        outfile.write(Json_data)
        outfile.close()

        
# Book return function ------------------
def ReturnBook():
    
    print("Enter books return function")
    logging.info("Entered books return function")
    content = {}
    user_id = input("Enter your user id: ")
    section_name = input("Enter the section name: ")
    book_name = input("Enter the book name: ")
    Books = open(json_store_path, 'r')
    Books = json.load(Books)
    
    # when user return thr book update the book count in books list
    Books[section_name][book_name] = str(int(Books[section_name][book_name]) + 1)
    Json_data = json.dumps(Books, indent = 4)
    with open(json_store_path, "w") as outfile:
        outfile.write(Json_data)
        outfile.close()
        
    logging.info("Book returned successfully")
    # once fince the book list update then update user status True for book returned
    Users = open(user_store_path, 'r')
    Users = json.load(Users)    
    content = Users[user_id]
    content[book_name]["status"] = True 
    Users[user_id] = content
    userdata = json.dumps(Users, indent = 4)
    with open(user_store_path, "w") as userfile:
        userfile.write(userdata)
        userfile.close()
    print("User return book successfully")

        
# Check duedate for borrowed books------------------
def checkduedate():
    
    print("Enter Due date check function")
    logging.info("Enter due date check function")
    content = {}
    users = open(user_store_path, 'r')
    users = json.load(users)   
    userlist = list(users.keys())
    now = datetime.datetime.now()
    
    # Set current date for book borrow date
    Borrow_date = now.strftime("%d/%m/%Y")
    userdata = users

    for i in userlist:
        user = list(users[i].keys())
        userdatas = users[i]
        content = users[i]
        user = user[1:]
        for j in user:
            
            # check the return date and status for user borrowed book return or not 
            # if book not return they get fine for book
            if userdatas[j]['returnDate'] <= Borrow_date and userdatas[j]['status'] != True:
                if "Fine_amound" in content[j]:
                    print("Already added fine")
                else:
                    content[j]['Fine_amound'] = 100
                    userdata[i] = content
                user_info = json.dumps(userdata, indent = 4)
                with open(user_store_path, "w") as userfile:
                    userfile.write(user_info)
                    userfile.close()
                logging.info("Fine amount added successfully")
                print(userdatas['name'], " is not submite book in correct date. fine amount added successfully")
            else:
                print("No Due date in user: ",userdatas['name'])
                logging.info("No fine pending book in users")

    
# ------------------------End ----------------------------

while True:
    gradiantial = input("Choice below: \n 1.User \n 2.Admin \n 3. Exit\n")

    if gradiantial == 'User' or gradiantial == "1":

        # perform some task in below
        print("user enter the function")
        u_choice = input("Choice below mention: \n 1.Return_book \n 2.Borrow \n 3.listbook \n 4.searchbook \n 5.checkborrowdetails \n\n")
        if u_choice == "Borrow" or u_choice == "1":
            borrowBook()
        elif u_choice == "Return_book" or u_choice == "2":
            ReturnBook()
        elif u_choice == "listbook" or u_choice == "3":
            listbook()
        elif u_choice == "searchbook" or u_choice == "4":
            Search_book()
        elif u_choice == "checkborrowdetails" or u_choice == "5":
            checkfineamount()
        else:
            print("Wrong choice")

    elif gradiantial == 'Admin' or gradiantial == "2":

        user_name = input("Enter the admin name: ")
        password = input("Enter the password: ")
        status = authchcek(user_name, password)
        print(status,"\n")

        # check session id for admin login or not
        if session_id:

            a_perform = input("\n Enter which perform you want to perform: \n 1.AddBook \n 2.ListBook \n 3.SearchBook \n 4.Listusers \n 5.checkduedate \n\n")
            if a_perform == "AddBook" or a_perform == "1":
                addbook()
            elif a_perform == "ListBook" or a_perform == "2":
                listbook()
            elif a_perform == "SearchBook" or a_perform == "3":
                Search_book()
            elif a_perform == "Listusers" or a_perform == "4":
                listuser()
            elif a_perform == "checkduedate" or a_perform == "5":
                checkduedate()
            else:
                print("\n Your enter wrong answare")

    elif gradiantial == "Exit" or gradiantial == "3":
        break
    else:
        print("Your choicen wrong answare\n")
    
    input("Press any Key to continue")

