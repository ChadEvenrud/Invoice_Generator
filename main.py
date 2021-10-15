import psycopg2 as sql

# Connects to the PostgreSQL database.  The class will also add Tables for the application.
class ClientData:
    def __init__(self, username, password):
        try:
            self.con = sql.connect(f"dbname=MCE_Clients user={username} password={password}")
        except:
            print("User name or password does not match MCE_Clients Database")

    def client_tables(self):
        commands = """
        CREATE TABLE IF NOT EXISTS Clients ( ClientID SERIAL PRIMARY KEY, ClientName VARCHAR(255), Address1 VARCHAR (255), Address2 VARCHAR (255),
            City VARCHAR (200), State VARCHAR (2), ZIP VARCHAR (20))          
        """
        self.cursor = self.con.cursor()
        self.cursor.execute(commands)
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


class CreateInvoice(Invoice):
    pass


test = ClientData("chad_evenrud", "Waterpolo1!")
test.client_tables()

# test = Invoice("0001", "PBG", "01/01/2020")
# test.invoice_detail()
# print(test.invoice_amount)
