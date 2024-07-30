import mysql.connector 
mydb=mysql.connector.connect(host="localhost",user="root",passwd="***")
mycursor=mydb.cursor()
mycursor.execute("create database if not exists viveenakhatri")
mycursor.execute("use viveenakhatri")

def base():
    mycursor.execute("""create table if not exists Product(Product_id int Primary Key,Product_name varchar(20),
                    Price int, Qnty int )""")
    mycursor.execute('''create table if not exists BillDetails (ID int(10) Primary key,Username varchar(20),
                    Product_id int,
                    Qnt int, Phn_no varchar(10),Email varchar(25),Mode_of_payment varchar(15),
                    Foreign key(Product_id) references Product(Product_id))''')
    
    
base()


    
#insert function
def insert():
    sql="select MAX(ID) from BillDetails"
    mycursor.execute(sql)
    res=mycursor.fetchone()
    if res[0]==None:
        ID=1
    else:
        ID=res[0]+1
    
    print("<<<<<< YOUR BILL ID IS: ",ID,">>>>>>>>")    
    Username=input("enter the Username:")
    Product_id=int(input("enter product id:"))
    s="select Qnty from Product where Product_id=%s" %(Product_id)
    mycursor.execute(s)
    result=mycursor.fetchone()
    print("Avail quantity {0}".format(result[0]))
    s="select Price from Product where Product_id=%s" %(Product_id)
    mycursor.execute(s)
    myresult=mycursor.fetchone()
    
    print("₹{0}".format(myresult[0]))
    
    Qnt=int(input("enter the quantity"))
    if Qnt<=result[0]:  
        Phn_no=int( input("enter the phone no:"))
        Email=input("enter your email id:")
        Mode_of_payment = input("enter the mode of payment:")
        sql="Insert into BillDetails values(%s,%s,%s,%s,%s,%s,%s)"
        val=(ID,Username,Product_id,Qnt,Phn_no,Email,Mode_of_payment)
        print("<<<<<<<<<< ORDER IS PLACED >>>>>>>>>>")
        mycursor.execute(sql,val)
        new_qty=result[0]-Qnt
        sql="update Product set Qnty=%s where Product_id=%s"
        v=(new_qty,Product_id)
        mycursor.execute(sql,v)
        
        mydb.commit()
    
    else:
        print("THIS MUCH QNT IS NOT AVAILABLE")


            
    
def Product_insert():
    adid=int(input("enter the admin id: "))
    pss=input("enter the password: ")
    if adid==123456 and pss=="olopcs":
        print("**********MATCHED**********")
        x=int(input("how many product you want to add"))
        for i in range(x):
            sql="select MAX(Product_id) from Product"
            mycursor.execute(sql)
            res=mycursor.fetchone()
            if res[0]==None:
                Product_id=100
            else:
                Product_id=res[0]+1
            Product_name=input("enter product name: ")
            Price=int(input("enter price INR: "))
            Qnty=int(input("enter Qnty available: "))
            
            sql="Insert into Product values(%s,%s,%s,%s)"
            val=(Product_id,Product_name,Price,Qnty)
            print("<<<<<<<<<<<successfully stored>>>>>>>>>>>>")
            mycursor.execute(sql,val)
            mydb.commit()
    else:
        print("********INCORRECT********")
        main_menu()


    
        
    
    

#update function
    
def update():
    ID = int(input("enter the ID:"))
    sql="select * from BillDetails where ID=%s"
    val=(ID,)
    mycursor.execute(sql,val)
    myresult=mycursor.fetchone()
    Username = input("enter the Username [s for old]:")
    if Username=='s':
        Username=myresult[1]
    Product_id = int(input("enter the Product id [0 for old]:"))
    if Product_id==0:
        Product_id=myresult[2]
    Qnt=int(input("enter the Qnt [0 for old]:"))
    if Qnt==0:
        Qnt=myresult[3]
    Phn_no= int(input("enter the phone no [0 for old]:"))
    if Phn_no==0:
        Phn_no=myresult[4]
    Email = input("enter the email id [s for old]:")
    if Email=='s':
        Email=myresult[5]
    Mode_of_payment = input("enter the mode of payment [s for old]:")
    if Mode_of_payment=='s':
        Mode_of_payment=myresult[6]
    sql = '''update BillDetails set Username=%s,Product_id=%s,Qnt=%s,
               Phn_no=%s,Email=%s,mode_of_payment=%s where ID=%s'''
    val = (Username,Product_id,Qnt,Phn_no,Email,Mode_of_payment,ID)
    print("<<<<<<<<<<<ORDER IS UPDATED >>>>>>>>>>")
    mycursor.execute(sql,val)
    mydb.commit()

#delete function
def delete():
    ID=int(input("enter the ID:"))
  
    u="select Qnt,Product_id from BillDetails where ID=%s"%(ID)
    mycursor.execute(u)
    result=mycursor.fetchone()
    print("".format(result[0]))
    Product_id=result[1]
    x="select Qnty from Product where Product_id=%s"%(Product_id)
    mycursor.execute(x)   
    data=mycursor.fetchone()
    adqty=data[0]
    tot_Qty=adqty+result[0]
    sql="update Product set Qnty=%s where Product_id=%s"
    v=(tot_Qty,Product_id)
    mycursor.execute(sql,v)
    mydb.commit()
    sql = "delete from BillDetails where ID=%s"
    val = (ID,)
    print("********** ORDER IS CANCELLED **********")
    mycursor.execute(sql,val)
    mydb.commit()
    
            

#display function
def display():
     ID=int(input("Enter the Purchase ID whose records are to be displayed:"))
     sql="Select*from BillDetails where ID=%s"
     val=(ID,)
     mycursor.execute(sql,val)
     myresult=mycursor.fetchone()
     print("ID:               ",myresult[0])
     print("Username:         ",myresult[1])
     print("Product_name :    ",myresult[2])
     print("Qnt :             ",myresult[3])
     print("Phn_no:           ",myresult[4])
     print("Email:            ",myresult[5])
     print("Mode_of_payment : ",myresult[6])


def item_display():
    mycursor.execute("select * from Product")
    myresult=mycursor.fetchall()
    print('|','-'*42,'|')

    print('| Product_id | Product_name  | Price  | Qnty |')
    print('|','-'*42,'|')
    for x in myresult:
        print("|{0:^12}| {1:^14}|{2:^8}|{3:^6}|".format(x[0],x[1],x[2],x[3]))
        print('|','-'*42,'|')

    print("")
   


def bill():
    ID=int(input("Enter the ID whose bill is to be displayed:"))
    
    st="select Qnt,Product_id from BillDetails where ID= %s " %(ID)
    mycursor.execute(st )
    myresult=mycursor.fetchone()
    print("".format(myresult[0]))
    Product_id=myresult[1]
 
    pt="select Price from Product where Product_id= %s " %(Product_id )
    mycursor.execute(pt )
    myresultt=mycursor.fetchone()
    print("".format(myresultt[0]))
    a=myresult[0]*myresultt[0]
    print("          ======================================================          ")
    print("                  Quantity:            ",myresult[0] )
    print("                  Price per item INR:  ",myresultt[0])
    print("                  Total Amount:        ","₹", a)
    print("          ======================================================          ")
    
    
    
    
    
   
#Product use only
def buyers_display():
    adid=int(input("enter the Admin id: "))
    pss=input("enter the password: ")
    if adid==123456 and pss=="olopcs":
        print("**********MATCHED**********")
        def show():
            
            mycursor.execute("select * from BillDetails")
            myresult=mycursor.fetchall()
            print('|','='*69,'|')
            print('| ID | Usename | Product_id | Qnt | Phone_no | Email  | Mode_of_payment |')
            print('|','='*69,'|')
            for x in myresult:
                print("|{0:^4}|{1:^9}|{2:^12}|{3:^5}|{4:^10}| {5:^7}| {6:^16}|".format(x[0],x[1],x[2],x[3],x[4],x[5],x[6]))
                print('|','='*69,'|')
            print("")
        show()
    else:
        print("********INCORRECT*********")

def main_menu():
    print("-----------------------------------WELCOME TO EXPORT HOUSE-----------------------------------------")
    print("***************************************************************************************************")
    print("|   1. Buy Product                  2. Update Order           3. Cancel Order                      |")
    print("|   4. View Order                   5. Display bill           6. Display available product         |")
    print(" ----------------------------------------ADMIN USE--------------------------------------------------")
    print("|   10. Display Buyers              11. Add Product Details                                        |")
    print("------------------------------------ 0. To Exit-----------------------------------------------------")
    
    
    
  

while True:
    main_menu()
    ch=int(input("enter the choice:"))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if ch==1:
        item_display()
        print("select the item from above list")
        insert()
    elif ch==2:
        update()
    elif ch==3:
        delete()
    elif ch==4:
        display()
    elif ch==5:
        bill()
    elif ch==10:
        buyers_display()
    elif ch==11:
        Product_insert()
    elif ch==6:
        item_display()
    elif ch==0:
        exit()
     































































