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
                     Client_ID INTEGER NOT NULL, Received BOOL NOT NULL)
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

    # Adds a new contact to the database.
    def add_contact(self):

        insert_command = "INSERT INTO contacts(client_id, first_name, last_name, email, phone)"
        client_list = 0
        print("List of current Clients and Client ID Numbers {}".format(self.client_records))
        company_name = input("Enter Company Name: ")
        first_name = input("Enter Contacts First Name: ")
        last_name = input("Enter Contacts Last Name: ")
        email = input("Enter email: ")
        phone = input("Enter phone: ")

        # Looks to make sure there is a client record in the database.  If there is it will create the contact record.
        for x in self.client_records:
            if company_name in x:
                client_list += 1
        if client_list > 0:
            client_id = x[0]
            values = (client_id, first_name, last_name, email, phone)
            self.cursor.execute(f"""
                                     {insert_command}
                                     Values{values}
                                                     """)
            self.con.commit()
        else:
            add_new_client = input(
                "This company does not exist in the database. \n Do you want to add a new client contact?: (y/n) ").lower()
            if add_new_client == 'y':
                self.new_client()
                command = "SELECT client_id, client_name FROM clients"
                table_data = self.cursor.execute(command)
                updated_client_data = self.cursor.fetchall()
                for x in updated_client_data:
                    if company_name in x:
                        client_id = x[0]
                        values = (client_id, first_name, last_name, email, phone)
                        self.cursor.execute(f"""
                                                    {insert_command}
                                                    Values{values}
                                                                  """)
                        self.con.commit()
            else:
                print("Can't add new contact without a current company record.")
                sys.exit()


class Invoice(Clients):
    def __init__(self):
        super().__init__()
        client_db_command = self.cursor.execute("SELECT client_id, client_name FROM clients")
        client_db_data = self.cursor.fetchall()
        current_client = []
        client_counter = 0
        for x in client_db_data:
            current_client.append(x)
        print("List Of Current Client Number nad Clients.{}".format(current_client))
        client_name = input("Enter Client Name: ")
        for x in current_client:
            if client_name in x:
                client_counter += 1
        if client_counter > 0:
            pass
        else:
            print("Client does not exist")
            new_record = input("Do you want to create a new Client?(y/n): ").lower()
            if new_record == 'y':
                self.new_client()
            else:
                print("Can't continue to enter an invoice.")
                sys.exit()
        invoice_date = input("Enter invoice date: ")
        invoice_data_command = self.cursor.execute("SELECT MAX(invoice_number) as RecentInvoice FROM invoice")
        invoice_data_db = self.cursor.fetchall()
        invoice_number = 0
        if invoice_data_db[0][0] == None:
            invoice_number = 100001
        else:
            invoice_number = invoice_data_db[0][0] + 1
        print("Invoice Number: ", invoice_number)
        client_id_data = self.cursor.execute(f"SELECT client_id FROM clients WHERE client_name = '{client_name}'")
        client_id = self.cursor.fetchall()[0][0]
        print("Client_ID: ", client_id)
        insert_command = "INSERT INTO invoice(client_id, invoice_date, invoice_number, received)"
        value = (client_id, invoice_date, invoice_number, False)
        self.cursor.execute(f"""
                                             {insert_command}
                                             Values{value}
                                                             """)
        self.con.commit()

        # creates the invoice detail
        self.cursor.execute(f"SELECT Record_ID FROM Invoice WHERE Invoice_Number = {invoice_number} ")
        invoice_record_number = self.cursor.fetchall()
        invoice_record_number = invoice_record_number[0][0]
        print("Invoice Record #: ", invoice_record_number)

        line_number: int = 1
        hours = input("Enter Hours: ")
        rate = input("Enter Rate: ")
        amount = float(hours) * float(rate)
        work_description = input("Enter work description: ")

        invoice_detail_command = "INSERT INTO invoice_detail(invoice_id, line_number, hours, rate, amount, work_description)"
        detail_value = (int(invoice_record_number), line_number, int(hours), int(rate), amount, work_description)
        self.cursor.execute(f"""
                                {invoice_detail_command}
                                Values{detail_value}
                                                        """)
        self.con.commit()

        while True:
            u_input = input("Do you want to create a anohter line item? (y/n): ").lower()
            if u_input == 'n':
                break
            else:
                line_number += 1
                hours = input("Enter Hours: ")
                rate = input("Enter Rate: ")
                amount = float(hours) * float(rate)
                work_description = input("Enter work description: ")

                invoice_detail_command = "INSERT INTO invoice_detail(invoice_id, line_number, hours, rate, amount, work_description)"
                detail_value = (
                int(invoice_record_number), line_number, int(hours), int(rate), amount, work_description)
                self.cursor.execute(f"""
                                                {invoice_detail_command}
                                                Values{detail_value}
                                                                        """)
                self.con.commit()


    def upate_invoice_detail(self):
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


l = Invoice()
