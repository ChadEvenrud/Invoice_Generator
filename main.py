import psycopg2 as sql


class ClientData:
    def __init__(self, username, password):
        try:
            self.con = sql.connect(f"dbname=MCE_Clients user={username} password={password}")
        except:
            print("User name or password does not match MCE_Clients Database")


    def client_tables(self):
        commands = """
        CREATE TABLE Clients ( ClientID SERIAL PRIMARY KEY, ClientName VARCHAR(255), Address1 VARCHAR (255), Address2 VARCHAR (255),
            City VARCHAR (200), State VARCHAR (2), ZIP VARCHAR (20))          
        """
        self.cursor = self.con.cursor()
        self.cursor.execute(commands)


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
        self.invoice_number = invoice_number
        self.date = date

    @staticmethod
    def invoice_detail():
        item_list = {}
        amount_list = []
        while True:
            line_number = input("Enter Line Number: ")
            if line_number == '' or line_number == 'Done'.lower():
                break
            else:
                hours = input("Enter hours: ")
                rate = input("Enter rate: ")
                work_description = input("Work description: ")
                amount = float(hours) * float(rate)
                amount_list.append(amount)
                item_list[line_number] = [
                    {"Description": work_description, "Rate": rate, "Hours": hours, "line_amount": amount}]
        return item_list

            


    # @staticmethod
    # def work_description():
    #     description = input("Enter Work Description: ")
    #     return description


class CreateInvoice(Invoice):
    pass

