from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    
    #assigning the variable cart_items to the 'cart' value, which as indicated is a dictionary itself, with ids as keys and qty as values.
    cart_items = session['cart']  

    #we initialize an empty list b/c in our for loop, we are creating a list of dictionaries, with keys name, price, qty and values name, price, qty based on ids.
    melon_details = []

    #this for loop interates over each id:qty in cart_items
    for id, quantity in cart_items.iteritems():
        #call the get_melon_by_id() function so we can obtain all info for each melon.  we will use this info below to create yet another dictionary
        melon = model.get_melon_by_id(id)
        #referencing attributes of melon and assigning as values to the melon_dict.
        melon_dict = {
            "name": melon.common_name,
            "price": melon.price,
            "quantity": quantity
        }
        #appending to the melon_details list initiated above the for loop
        melon_details.append(melon_dict)

    #the list melon_details is then passed to the html document, which iterates over this list to create the items in the cart.
    return render_template("cart.html", melons = melon_details)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
    # changing the integer id into a string b/c dictionaries prefer keys as strings
    id = str(id)

    # checking to see if the customer has an existing cart (ie is anything added)
    if 'cart' in session:
        #if cart exists, then checking to see if the item added already exists
        if id in session['cart']:
            #if the item already exists, then we are increasing the value (in this case the qty) by 1.
            session['cart'][id] += 1
        else:
            #if the item does not yet exist, then we are adding it to the dictionary with a value of 1.
            session['cart'][id] = 1
        #if cart does not exist, then we are assigning the cart key a value, which is another dictionary.  This has a key of 'id' and initial value of 1
    else:
        session['cart'] = {id:1}

    #after adding the item to the cart, we are redirecting to the /cart page, which then calls the function shopping_cart().
    return redirect("/cart")

@app.route("/sessionclear", methods=["GET"])
def sessionclear():
    session.clear()
    return "BOOM!"


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    
    email = request.form.get('email')
    customer = model.get_customer_by_email(email)

    if customer:
        if 'users' in session:
            if customer.email not in session['users']:
               session['users'] = {customer.email: customer.password}
               print session['users']
    
    # flash("Login Successful")
    return redirect("/melons")

@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
