import psycopg2 as sql
from fpdf import FPDF

user_name = "chad_evenrud"
pw = "Waterpolo1!"


# Connects to the PostgreSQL database.  The class will also add Tables for the application.
class ClientData:
    def __init__(self, username, password):
        try:
            self.con = sql.connect(f"dbname=MCE_Clients user={username} password={password}")
        except:
            print("User name or password does not match MCE_Clients Database")
        self.cursor = self.con.cursor()

    def create_tables(self):
        commands = ("""
                    CREATE TABLE IF NOT EXISTS Clients ( Client_ID INT PRIMARY KEY, Client_Name VARCHAR (255)
                     NOT  NULL, Address1 VARCHAR (255) NULL, Address2 VARCHAR (255) NULL , City VARCHAR (200) NULL ,
                      State VARCHAR (2)  NULL, ZIP VARCHAR (20) NULL)          
                    """
                    ,
                    """
                    CREATE TABLE IF NOT EXISTS Invoice (Record_ID SERIAL PRIMARY KEY, Invoice_Number VARCHAR (50) 
                    NOT NULL , Invoice_Date DATE NOT NULL,  Client_ID INTEGER NOT NULL, Received BIT NOT NULL)
                    """
                    ,
                    """
                    CREATE TABLE IF NOT EXISTS Invoice_Detail (Invoice_ID SMALLINT NOT NULL, 
                     Line_Number SMALLINT NOT NULL, Hours SMALLINT, Rate SMALLINT, Amount NUMERIC, 
                     Work_Description TEXT) 
                    """
                    ,
                    """
                    CREATE TABLE IF NOT EXISTS Contacts ( Contact_ID SERIAL PRIMARY KEY, Client_ID SMALLINT NOT NULL, 
                    First_Name VARCHAR (200) NOT NULL, Last_Name VARCHAR(200) NOT NULL, Email VARCHAR (200), 
                    Phone varchar (25))   
                    """)

        for x in commands:
            self.cursor.execute(x)
        self.con.commit()
        self.cursor.close()
        self.con.close()


# Adds new Client Records to the database
class Clients(ClientData):

    def client_table(self):
        client_records = []
        command = "SELECT * FROM clients"
        table_data = self.cursor.execute(command)
        review_data = self.cursor.fetchall()
        for x in review_data:
            client_records.append(x)
        return client_records

    def new_client(self):
        insert = "INSERT INTO clients(client_name, address1, address2, city, state, zip)"
        client_name = input("Enter Client Name: ")
        address = input("Address")
        city = input("Enter City: ")
        state = input("Enter State: ")
        zip = input("Enter Zip: ")
        l_values = (client_name, address, '', city, state, zip)
        command = f"""
                    {insert}
                    values{l_values}
                    """
        self.cursor.execute(command)
        self.con.commit()

    def client_contact(self, contact_name, contact_email, contact_phone):
        pass


# Creates an invoice record and invoice detail.

class Invoice(ClientData):

    def __init__(self, invoice_number, client, date):
        self.invoice_amount = 0
        self.client = client
        self.invoice_number = invoice_number
        self.date = date

    # Collects the invoice detail record line items.

    def invoice_detail(self):
        item_list = {}
        amount_list = []

        while True:
            line_number = input("Enter Line Number: ")
            if line_number == '' or line_number == 'Done'.lower():
                break
            else:
                hours = float(input("Enter hours: "))
                rate = float(input("Enter rate: "))
                work_description = input("Work description: ")
                amount = hours * rate
                amount_list.append(amount)
                item_list[line_number] = [
                    {"Description": work_description, "Rate": rate, "Hours": hours, "line_amount": amount}]
        for x in amount_list:
            self.invoice_amount += x
        for x in item_list.items():
            print(x[0], x[1][0]["Description"], x[1][0]["Rate"], x[1][0]["Hours"], x[1][0]["line_amount"])


# Generates a Invoice PDF document without having to commit data to the database.

class CreateInvoice(FPDF):

    def header(self):
        invoice = Invoice(input("Invoice #: "), input("Client Name: "), input("Invoice Date: "))
        self.image('Picture1.png', .5, .12, w=1)
        self.set_font('times', 'B', 20)
        self.cell(0, .5, 'Invoice ', ln=True, align="R")
        self.ln(.5)
        self.set_font('times', '', 13)
        self.multi_cell(0, .15, "Chad Evenrud \n3946 Nereis Dr. \nLa Mesa, CA, 91941")
        self.ln(.0)
        self.multi_cell(0, .15, "Date: {} \n Invoice #: {}".format(invoice.date, invoice.invoice_number), align="R")
        self.ln(.15)
        self.set_font('times', "BU", 14)
        self.cell(0, .2, "Invoice For", align="L", ln=True)
        self.set_font('times', "B", 13)
        self.cell(0, .15, invoice.client, align="L")
        self.ln(.2)

    def body(self):
        self.add_page()
        self.set_font('times', '', 12)
        self.cell(0, .15, 'ello', align="L")
        self.set_auto_page_break(auto=True, margin=.5)

    def footer(self):
        self.set_y(-.5)
        self.set_font('times', 'I', 10)
        self.cell(0, .5, 'Pg', align="C")


# # pdf = CreateInvoice('P','in', 'Letter')
# # pdf.body()
# # pdf.output('Invoice.pdf')
#
# #

clientsql = Clients(user_name, pw)
print(clientsql.new_client())

#
# test = Invoice("0001", "PBG", "01/01/2020")
# test.invoice_detail()
# print(test.invoice_amount)
