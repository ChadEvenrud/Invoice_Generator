import psycopg2 as sql
from fpdf import FPDF
import sys

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
                    CREATE TABLE IF NOT EXISTS Clients ( Client_ID SERIAL PRIMARY KEY, Client_Name VARCHAR (255)
                     NOT  NULL, Address1 VARCHAR (255) NULL, Address2 VARCHAR (255) NULL , City VARCHAR (200) NULL ,
                      State VARCHAR (2)  NULL, ZIP VARCHAR (20) NULL)          
                    """
                    ,
                    """
                    CREATE TABLE IF NOT EXISTS Invoice (Record_ID SERIAL PRIMARY KEY, Invoice_Number INT DEFAULT 000001,
                     Invoice_Date DATE NOT NULL, 
                     Client_ID INTEGER NOT NULL, Received BIT NOT NULL)
                    """
                    ,
                    """
                    CREATE TABLE IF NOT EXISTS Invoice_Detail (Invoice_ID SMALLINT NOT NULL, 
                     Line_Number SMALLINT NOT NULL, Hours SMALLINT, Rate SMALLINT, Amount NUMERIC, 
                     Work_Description TEXT) 
                    """
                    ,
                    """
                    CREATE TABLE IF NOT EXISTS Contacts ( Contact_ID  SERIAL PRIMARY KEY , Client_ID SMALLINT NOT NULL, 
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

    def __init__(self):
        super().__init__(user_name, pw)
        self.client_records = []
        self.command = "SELECT client_id, client_name FROM clients"
        self.table_data = self.cursor.execute(self.command)
        self.review_data = self.cursor.fetchall()
        for x in self.review_data:
            self.client_records.append(x)

    # Creates a new client record in the data tables
    def new_client(self):
        insert = "INSERT INTO clients(client_name, address1, address2, city, state, zip)"
        client_name = input("Enter Client Name: ")
        address = input("Address: ")
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

#Adds a new contact to the database.
    def add_contact(self):
        print("List of current Clients and Client ID Numbers {}".format(self.client_records))
        current_client = 0
        client_name = input("Client Name: ")

# Looks to see if the client exist in the database.
        for x in self.client_records:
            if client_name in x:
                current_client +=1
        if current_client == 0:
            print("The Client does not exist.")
            if input("Do you want to add a new client contact?: (y/n) ").lower() == 'y':
                self.new_client()
                command = "SELECT client_id, client_name FROM clients"
                table_data = self.cursor.execute(command)
                self.updated_client_data = self.cursor.fetchall()
                print(self.updated_client_data)
            else:
                print("Can't add new contact without a current company record.")
                sys.exit()
        updated_clients = []

#Adds the client contact to the database.
        for x in self.updated_client_data:
            updated_clients.append(x)
        contact_first_name = input("Contact First Name: ")
        contact_last_name = input("Contact Second Name: ")
        email = input("Email Address: ")
        phone = input("Enter Phone: ")
        client_id = ''
        for x in updated_clients:
            if client_name in x:
                client_id = x[0]
                insert_command = "INSERT INTO contacts(client_id, first_name, last_name, email, phone)"
                values = (client_id, contact_first_name, contact_last_name, email, phone)
                self.cursor.execute(f"""
                                        {insert_command}
                                        Values{values}
                                            """)
                self.con.commit()



class Invoice(ClientData):

    def invoice_record(self, client, date):
        client = client
        date = date
        invoice_table_command = "SELECT MAX(invoice_number) FROM invoice"
        self.cursor.execute(invoice_table_command)
        last_invoice = self.cursor.fetchall()
        client_table_command = "SELECT client_id, client_name FROM clients"
        self.cursor.execute(client_table_command)
        data = self.cursor.fetachall()
        current_clients = []
        for x in data:
            current_clients.append(x)
        return current_clients

    # Collects the invoice detail record line items.

    def invoice_detail(self):
        item_list = {}
        amount_list = []
        line_count = 1

        while True:
            line_number = input("Enter Invoice Line (1 = Yes, 2 =No/Done): ")
            if line_number == 2 or line_number == "":
                break
            else:
                hours = float(input("Enter hours: "))
                rate = float(input("Enter rate: "))
                work_description = input("Work description: ")
                amount = hours * rate
                amount_list.append(amount)
                item_list[line_count] = [
                    {"Description": work_description, "Rate": rate, "Hours": hours, "line_amount": amount}]
                line_count += 1
        print(item_list)
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


test = Clients()
test.add_contact()

