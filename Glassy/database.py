import sqlite3


class Database:
    def __init__(self):
        self.con = sqlite3.connect('Glassy.db')
        self.cursor = self.con.cursor()
        self.create_users_table() #create the tasks table
        self.create_cust_records_table()
        self.create_expenses_table()
        self.create_sales_table()
        self.create_purchases_table()
        
    #USERS TABLE(username,password)
    def create_users_table(self):
        """Create users table"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY AUTOINCREMENT, username varchar(50) NOT NULL, pass varchar(20) NOT NULL)")
        self.con.commit()
    #customer_records(name,phone_number)
    def create_cust_records_table(self):
        """Create cust_records table"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS cust_records(id integer PRIMARY KEY AUTOINCREMENT, customer_name varchar(50) NOT NULL, phone varchar(16) NOT NULL)")
        self.con.commit()
    #expenses TABLE
    def create_expenses_table(self):
        """Create expenses table"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS expenses(id integer PRIMARY KEY AUTOINCREMENT, expense varchar(50) NOT NULL, amount integer(50) NOT NULL)")
        self.con.commit()
    #sales table
    def create_sales_table(self):
        """Create sales table"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sales(id integer PRIMARY KEY AUTOINCREMENT, quantity  integer(50) NOT NULL, gauge varchar(20) NOT NULL,unit_price integer(50) NOT NULL,colour varchar(20) NOT NULL)")
        self.con.commit()
    #purchases/stock table
    def create_purchases_table(self):
        """Create purchases table"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS purchases(id integer PRIMARY KEY AUTOINCREMENT, gauge varchar(50) NOT NULL, quantity integer(20) NOT NULL,unit_price integer(20) NOT NULL,supplier varchar(16) NOT NULL)")
        self.con.commit()
    #Task remainder table
    def create_task_table(self):
        """Create tasks table"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, due_date varchar(50), completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))")
        self.con.commit()

    def create_task(self, task, due_date=None):
        """Create a task"""
        self.cursor.execute("INSERT INTO tasks(task, due_date, completed) VALUES(?, ?, ?)", (task, due_date, 0))
        self.con.commit()

        # GETTING THE LAST ENTERED ITEM SO WE CAN ADD IT TO THE TASK LIST
        created_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0", (task,)).fetchall()
        return created_task[-1]

    def get_tasks(self):
        """Get all completed and uncomplete tasks"""
        uncomplete_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 0").fetchall()
        completed_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 1").fetchall()
        # return the tasks to be added to the list when the application starts
        return completed_tasks, uncomplete_tasks



    def mark_task_as_complete(self, taskid):
        """Mark tasks as complete"""
        self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (taskid,))
        self.con.commit()

    def mark_task_as_incomplete(self, taskid):
        """Mark task as uncomplete"""
        self.cursor.execute("UPDATE tasks SET completed=0 WHERE id=?", (taskid,))
        self.con.commit()

        # return the task text
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id=?", (taskid,)).fetchall()
        return task_text[0][0]

    def delete_task(self, taskid):
        """Delete a task"""
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self.con.commit()

    def close_db_connection(self):
        self.con.close()
    #check if user is in db or not
    def verify_user(self,username,password):
        self.cursor.execute('SELECT count(*) from users WHERE username="%s" AND pass="%s"' % (username, password))
        data=self.cursor.fetchone()
        count=data[0]
        
        return count
    #create user
    def create_user(self,username,password):
        if username !='' and password!='' or username is not None and password is not None: 
            self.cursor.execute("INSERT INTO users(username, pass) VALUES(?, ?)",(username, password))
            self.con.commit() 
            self.con.close()   
    #get username from db
    def get_username(self,username,password):
         
        self.cursor.execute('SELECT count(*) from users WHERE username="%s" AND pass="%s"' % (username, password))
        data=self.cursor.fetchone()
        self.con.close()
        return data[1:] 
    #create /add customer
    def add_customer(self,name,phone):
        if name !='' and phone!='' or name is not None and phone is not None: 
            self.cursor.execute("INSERT INTO cust_records(customer_name , phone) VALUES(?, ?)",(name, phone))
            self.con.commit() 
            self.con.close() 
    #create /add sales
    def add_sales(self,quantity,gauge,unitprice,colour):
        if quantity !='' and gauge!='' and unitprice!='' and colour!='': 
            self.cursor.execute("INSERT INTO sales(quantity,gauge,unit_price,colour) VALUES(?,?,?,?)",(quantity,gauge,unitprice,colour))
            self.con.commit() 
            self.con.close()
    #delete sales record 
    def delete_sales(self,cust_id):
        """Delete sales"""
        self.cursor.execute("DELETE FROM sales WHERE id=?", (cust_id,))
        self.con.commit()
        self.con.close()
     #get all customers
    def all_sales(self):
        self.cursor.execute('SELECT * from sales')
        records=self.cursor.fetchall()
        self.con.close()
        return records
    #-------------------------------create /add purchases--------------------------------------------------------------
    def add_purchase(self,gauge,quantity,unitprice,supplier):
        if quantity !='' and gauge!='' and unitprice!='' and supplier!='': 
            self.cursor.execute("INSERT INTO purchases(gauge,quantity,unit_price,supplier) VALUES(?,?,?,?)",(gauge,quantity,unitprice,supplier))
            self.con.commit() 
            self.con.close()
    #delete purchases record 
    def delete_purchases(self,cust_id):
        """Delete purchases"""
        self.cursor.execute("DELETE FROM purchases WHERE id=?", (cust_id,))
        self.con.commit()
        self.con.close()
     #get all purchases
    def all_purchases(self):
        self.cursor.execute('SELECT * from purchases')
        records=self.cursor.fetchall()
        self.con.close()
        return records
    
#--------------------------ADD EXPENSES----------------------------------------------------------------------
    #add expenses
    def add_expense(self,exp_type,amount):
        if exp_type!='' and amount!='' or exp_type is not None and amount is not None:
            self.cursor.execute("INSERT INTO expenses(expense , amount) VALUES(?, ?)",(exp_type,amount))
            self.con.commit() 
            self.con.close()  
    #get all customers
    def all_customers(self):
        self.cursor.execute('SELECT * from cust_records')
        records=self.cursor.fetchall()
        self.con.close()
        return records
    #all expenses
    def all_expenses(self):
        self.cursor.execute('SELECT * from expenses')
        records=self.cursor.fetchall()
        self.con.close()
        return records
    #delete customer record 
    def delete_customer(self,cust_id):
        """Delete a customer"""
        self.cursor.execute("DELETE FROM cust_records WHERE id=?", (cust_id,))
        self.con.commit()
        self.con.close()
    #update customer's details
    def update_customer(self,customer_name, phone,id):
        self.cursor.execute("UPDATE cust_records SET customer_name=?, phone=? WHERE id=?",(customer_name, phone,id))
        self.con.commit()
        self.con.close()
        
        
        