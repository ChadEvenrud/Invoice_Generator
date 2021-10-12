import psycopg2 as sql


class ClientData:
    def __init__(self, username, password):
        try:
            con = sql.connect(f"dbname=MCE_Clients user={username} password=pass{password}")
        except:
            return print("User name or password does not match MCE_Clients Database")



class Clients:
    def __init__(self, client_name, address, city, state):
        self.client = client_name
        self.address = address
        self.city = city
        self.state = state


def invoice_amount(hours, rate):
    amount = float(hours) * float(rate)
    return amount


def work_description():
    description = input("Enter Work Description: ")
    return description


class Invoice:
    def __init__(self, invoice_number, date):
        self.invoice_number = invoice_number
        self.date = date


class CreateInvoice:
    pass



