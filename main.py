import psycopg2 as sql
from fpdf import FPDF


# Connects to the PostgreSQL database.  The class will also add Tables for the application.
class ClientData:
    def __init__(self, username, password):
        try:
            self.con = sql.connect(f"dbname=MCE_Clients user={username} password={password}")
        except:
            print("User name or password does not match MCE_Clients Database")
        self.cursor = self.con.cursor()

    def client_tables(self):
        commands = ("""
                    CREATE TABLE IF NOT EXISTS Clients ( Client_ID INT PRIMARY KEY, Client_Name VARCHAR(255), 
                    Address1 VARCHAR (255), Address2 VARCHAR (255), City VARCHAR (200), State VARCHAR (2), 
                    ZIP VARCHAR (20))          
                    """
                    ,
                    """
                    CREATE TABLE IF NOT EXISTS Invoice (Record_ID SERIAL Primary Key, Invoice_Number VARCHAR (50), 
                    Invoice_Date DATE,  Client_ID INTEGER , Received BIT)
                    """
                    ,
                    """
                    CREATE TABLE IF NOT EXISTS Invoice_Detail (Invoice_ID SMALLINT ,  Line_Number SMALLINT, 
                    Hours SMALLINT, Rate SMALLINT, Amount NUMERIC, Work_Description TEXT) 
                    """
                    ,
                    """
                    CREATE TABLE IF NOT EXISTS Contacts ( Contact_ID SERIAL PRIMARY KEY, Client_ID SMALLINT , 
                    First_Name VARCHAR (200) , Last_Name VARCHAR(200), Email VARCHAR (200), Phone varchar (25))   
                    """)

        for x in commands:
            self.cursor.execute(x)
        self.con.commit()
        self.cursor.close()
        self.con.close()


# Adds new Client Records to the database
class Clients:
    def __init__(self, client_name, address, city, state):
        self.client = client_name
        self.address = address
        self.city = city
        self.state = state

    def client_contact(self, contact_name, contact_email, contact_phone):
        pass


# Creates an invoice record and invoice detail.

class Invoice:

    def __init__(self, invoice_number, client, date):
        self.invoice_amount = 0
        self.invoice_number = invoice_number
        self.date = date

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


class CreateInvoice:
    pdf = FPDF('p', 'in', 'Letter')
    pdf.add_page()

    #Creat PDF Header
    pdf.set_font ('times', 'B', 20)

    pdf.cell(8, 1, 'Invoice')

    #Output
    pdf.output("Invoice.pdf")



pdf_test = CreateInvoice()

#
# test = ClientData("chad_evenrud", "Waterpolo1!")
# test.client_tables()
#
# # test = Invoice("0001", "PBG", "01/01/2020")
# test.invoice_detail()
# print(test.invoice_amount)
