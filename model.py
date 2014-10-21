import sqlite3

DB = None
CONN = None

class Melon(object):
    """A wrapper object that corresponds to rows in the melons table."""
    def __init__(self, id, melon_type, common_name, price, imgurl, flesh_color, rind_color, seedless):
        self.id = id
        self.melon_type = melon_type
        self.common_name = common_name
        self.price = price
        self.imgurl = imgurl
        self.flesh_color = flesh_color
        self.rind_color = rind_color
        self.seedless = bool(seedless)

    def price_str(self):
        return "$%.2f"%self.price

    def __repr__(self):
        return "<Melon: %s, %s, %s>"%(self.id, self.common_name, self.price_str())

class Customer(object):

    def __init__(self, email, password):
      self.email = email
      self.password = password

    def __repr__(self):
      return "<Customer: %s, %s>"%(self.email, self.password)

def connect():
    conn = sqlite3.connect("melons.db")
    cursor = conn.cursor()
    return cursor

def get_melons():
    """Query the database for the first 30 melons, wrap each row in a Melon object (i.e. create a melon instance).  The return will be a list of 30 melons, each different based on passing arguments through the Melon Class init() functions.  You will see below how it's done."""
    cursor = connect()
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE imgurl <> ''
               LIMIT 30;"""  #how I limit the number of melons for which I query

    cursor.execute(query)
    melon_rows = cursor.fetchall() # Retuns a list of tuples, with each tuple representing one row of information for each melon.  Each tuple contains the query items after SELECT.

    # Initialize an empty list called melons, which will hold all of my melon instances created by the for loop below.  This is what I need to return.
    melons = []

    for row in melon_rows:
        # from the for loop, I am creating multiple instances of the Melon Class, named melon.  In order to initialize each instance, the Melon Class __init__ function says I have to pass in a number of arguments.  I passing in these arguments by referencing the tuple index, pointing to the attributes for which I queried.
        melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                      row[6], row[7])
        # I am appending each melon instance to my melon list.
        melons.append(melon)
    
    return melons  # Now, anytime I call the get_melons() function, I get a list of my 30 melon instances 

def get_melon_by_id(id):
    """Query for a specific melon in the database by the primary key"""
    cursor = connect()
    query = """SELECT id, melon_type, common_name,
                      price, imgurl,
                      flesh_color, rind_color, seedless
               FROM melons
               WHERE id = ?;"""

    cursor.execute(query, (id,))

    row = cursor.fetchone() # row is a tuple of the query items
    
    if not row:
        return None

    melon = Melon(row[0], row[1], row[2], row[3], row[4], row[5],
                  row[6], row[7])
    
    return melon

def get_customer_by_email(email):
    cursor = connect()
    query = """ SELECT customers.email, customers.password
                FROM customers
                WHERE email = ?;"""

    cursor.execute(query, (email,))
    row = cursor.fetchone()   # tuple returned with values email and password
    
    if not row:
      return None
    
    customer = Customer(row[0], row[1])
    
    return customer

    
def main():
    connect()
    command = None
    while command != 'quit':

      input_string = raw_input("database>")
      tokens = input_string.split()
      command = tokens[0]
      args = tokens[1:]

      if command == "get_customer":
        get_customer_by_email(*args)
      if command == "melon_id":
        get_melon_by_id(*args)
      if command == "get_melon":
        get_melons(*args)

    CONN.close()

if __name__ == "__main__":
  main()