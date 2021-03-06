from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, g, Markup
import shelve
from Candy import Candy
from CandyCart import CandyCart
from Forms import CreateFeedbackForm, CreateCheckoutForm, NewEmail, SearchCheckoutInformation, UpdateDeliveryForm, StaffLogin, CreateStaff, UpdateStaff, CreateSupplierForm, UpdateSupplierForm, CreateOrderForm, UpdateOrderForm, CreateCandy, UpdateCandy, CustomerLogin, CreateCustomer, UpdateCustomer, CustomerChange, ManagePoints, LoginForm, s_CreateCustomer
from Feedback import Feedback
from datetime import date, timedelta
from CheckoutInformation import CheckoutInformation
from flask_mail import Mail, Message
from User import User, Login
from Customer import Customer
from Staff import Staff
from Supplier import Supplier
from Order import Order
from wtforms import SelectField, validators
from loginUser import loginUser

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

app.config.update(
    # email settings
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='sugaricandyshop@gmail.com',
    MAIL_PASSWORD='Sugari12345',
)
mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')


@app.route('/addtocart/<int:candyID>/', methods=['GET', 'POST'])
def addtocart(candyID):
    cartDict = {}
    candyDict = {}
    subtotal = 0

    db = shelve.open('storage.db', 'c')

    try:
        candyDict = db['Candy']
    except:
        print('Error in retrieving candy object from storage.db')

    try:
        cartDict = db['shoppingCart']
    except:
        print('Error in retrieving cart items from storage.db')

    candy = candyDict.get(candyID)

    quantity = int(request.form['quantity'])

    number = int(request.form['quantity'])
    if number > candy.get_candyStockLevel():
        flash('Quantity exceeds stock level. We only have ' + str(candy.get_candyStockLevel()))
        return redirect(url_for('homepage'))


    candy_cart = CandyCart(candy.get_candyName(), candy.get_candyStockLevel(), candy.get_candyRetailPrice(),
                           candy.get_candyCostPrice(), candy.get_candyCategory(), candy.get_candyImage(),
                           candy.get_candyKeyInformation(), candy.get_candyIngredients(), candy.get_candyCountry(), candy.get_candySupplier())
    candy_cart.set_quantity(quantity)

    subtotal = float(candy.get_candyRetailPrice()) * quantity
    subtotal = "{:.2f}".format(float(subtotal))
    candy_cart.set_subtotal(subtotal)

    cartDict[candy_cart.get_candyName()] = candy_cart

    db['shoppingCart'] = cartDict
    db.close()

    return redirect(url_for('shoppingcart'))


@app.route('/shoppingcart', methods=['GET', 'POST'])
def shoppingcart():
    cartDict = {}
    subtotal = 0
    total = 0

    try:
        db = shelve.open('storage.db', 'r')
        cartDict = db['shoppingCart']
        db.close()

    except:
        print('Error in retrieving cart items from storage.db')
        db = shelve.open('storage.db', 'c')
        db.close()

    cartList = []

    for key in cartDict:
        candy = cartDict.get(key)
        cartList.append(candy)

        subtotal = float(candy.get_subtotal())
        total = float(total)
        total += subtotal
        total = "{:.2f}".format(total)
    '''
    if request.method == "POST":
        # Add quantity
        if request.form["cart_button"] == "+":
            print('+')


        # Deduct quantity
        elif request.form["cart_button"] == "-":
            print('-')

       return redirect(url_for('shoppingcart'))
    '''
    return render_template('shoppingcart.html', cartList=cartList, total=total)


@app.route('/emptycart', methods=['GET', 'POST'])
def emptycart():
    cartDict = {}
    total = 0

    db = shelve.open('storage.db', 'w')

    try:
        cartDict = db['shoppingCart']
    except:
        print('Error in retrieving cart items from storage.db')

    cartDict.clear()

    db['shoppingCart'] = cartDict
    db.close()

    return render_template('shoppingcart.html', total=total)


@app.route('/s_menu', methods=['GET', 'POST'])
def s_menu():
    return render_template('s_menu.html')


@app.route('/s_inventory', methods=['GET', 'POST'])  # retrieve candies
def s_inventory():
    candyDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        candyDict = db['Candy']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()

    candyList = []
    for key in candyDict:
        candyitem = candyDict.get(key)
        candyList.append(candyitem)

    return render_template('s_inventory.html', candyList=candyList, count=len(candyList))


@app.route('/createCandy', methods=['GET', 'POST'])
def createCandy():
    supplierDict = {}
    list = []

    try:
        db2 = shelve.open('storage.db', 'w')
        supplierDict = db2['Suppliers']

    except:
        print('Error in retrieving suppliers from storage.db')
        flash('There are no suppliers. You need a supplier to create a candy.')
        flash(Markup('Click <a href="/s_createsupplier" class="alert-link">here</a> to create a supplier.'))
        return redirect(url_for('s_inventory'))

    for key in supplierDict:  # prob
        s = supplierDict.get(key)
        item = (s.get_companyName(), s.get_companyName())
        list.append(item)

    CreateCandy.supplier = SelectField('', [validators.DataRequired()], choices=list, default='')

    createCandy = CreateCandy(request.form)
    if request.method == 'POST' and createCandy.validate():
        candyDict = {}
        db = shelve.open("storage.db", "c")  # Create, read and write

        try:
            candyDict = db["Candy"]
            Candy.countID = db["CandyCountID"]
        except:
            print("Error in retrieving candies from storage.db")

        # Create an instance of class User
        candy = Candy(createCandy.name.data, 0, createCandy.retailprice.data, createCandy.costprice.data,
                      createCandy.category.data, createCandy.image.data, createCandy.supplier.data, createCandy.keyinformation.data, createCandy.ingredients.data, createCandy.country.data)
        # Save the user instance in usersDict, using userID as the key
        candyDict[candy.get_candyID()] = candy

        # Save dictionary to db
        db["Candy"] = candyDict

        # After create the user, save the countID to shelve/persistance
        db["CandyCountID"] = Candy.countID

        # Module / file Name.ClassName.class_attribute
        selectlist = []

        return redirect(url_for('s_inventory'))
    return render_template('s_createcandy.html', form=createCandy)


@app.route('/deleteCandy/<int:id>/', methods=["POST"])
def deleteCandy(id):
    candyDict = {}

    # retrieve from persistence
    db = shelve.open("storage.db", "w")
    candyDict = db["Candy"]

    # delete the record from the list
    candyDict.pop(id)

    # save the list
    db["Candy"] = candyDict
    db.close()

    return redirect(url_for("s_inventory"))


@app.route('/updateCandy/<int:id>/', methods=['GET', 'POST'])
def updateCandy(id):
    updateCandy = UpdateCandy(request.form)

    if request.method == 'POST' and updateCandy.validate():
        candyDict = {}
        db = shelve.open('storage.db', 'w')
        candyDict = db["Candy"]

        candy = candyDict.get(id)
        candy.set_candyName(updateCandy.name.data)
        candy.set_candyStockLevel(updateCandy.stock.data)
        candy.set_candyRetailPrice(updateCandy.retailprice.data)
        candy.set_candyCostPrice(updateCandy.costprice.data)
        candy.set_candyCategory(updateCandy.category.data)
        candy.set_candyKeyInformation(updateCandy.keyinformation.data)
        candy.set_candyIngredients(updateCandy.ingredients.data)
        candy.set_candyCountry(updateCandy.country.data)
        if updateCandy.image.data != "":
            candy.set_candyImage(updateCandy.image.data)

        db["Candy"] = candyDict
        db.close()
        return redirect(url_for('s_inventory'))

    else:
        candyDict = {}
        db = shelve.open('storage.db', 'r')
        candyDict = db["Candy"]

        # name, stock, price, category
        candy = candyDict.get(id)
        updateCandy.name.data = candy.get_candyName()
        updateCandy.stock.data = candy.get_candyStockLevel()
        updateCandy.retailprice.data = candy.get_candyRetailPrice()
        updateCandy.costprice.data = candy.get_candyCostPrice()
        updateCandy.category.data = candy.get_candyCategory()
        updateCandy.image.field = candy.get_candyImage()
        updateCandy.keyinformation.data = candy.get_candyKeyInformation()
        updateCandy.ingredients.data = candy.get_candyIngredients()
        updateCandy.country.data = candy.get_candyCountry()
        updateCandy.supplier.data = candy.get_candySupplier()

        return render_template('s_updatecandy.html', form=updateCandy)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    createCheckoutForm = CreateCheckoutForm(request.form)

    cartDict = {}
    subtotal = 0
    totalsubtotal = 0
    total = 0

    db = shelve.open('storage.db', 'r')

    try:
        cartDict = db['shoppingCart']
        db.close()
    except:
        print('Error in retrieving cart items from storage.db')

    cartList = []
    for key in cartDict:
        candy = cartDict.get(key)
        print(candy)
        cartList.append(candy)

        subtotal = float(candy.get_subtotal())
        totalsubtotal += subtotal
        total = float(total)
        total += subtotal
        total = "{:.2f}".format(float(total))

    if len(cartList) == 0:
        flash("Shopping cart is empty!")
        return redirect(url_for('shoppingcart'))

    # Click on the Submit button
    if request.method == 'POST' and createCheckoutForm.validate():
        checkoutDict = {}
        candyDict = {}
        db = shelve.open('storage.db', 'c')
        db1 = shelve.open('storage.db', 'w')
        candyDict = db1['Candy']

        total = float(total)

        try:
            checkoutDict = db['Checkouts']
            CheckoutInformation.count = db['CheckoutCountID']

        except:
            print("Error in retrieving Users from storage.db.")

        if createCheckoutForm.shippingMethod.data == 'regular':
            deliveryDate = date.today() + timedelta(days=14)
            shippingFee = 0

        elif createCheckoutForm.shippingMethod.data == 'express':
            deliveryDate = date.today() + timedelta(days=5)
            shippingFee = 3.50
            total += 3.50

        CardType = request.form['CardType']
        CardNumber = request.form['CardNumber']

        checkoutInformation = CheckoutInformation(createCheckoutForm.firstName.data,
                                                  createCheckoutForm.lastName.data, createCheckoutForm.phone.data,
                                                  createCheckoutForm.email.data, createCheckoutForm.address.data,
                                                  createCheckoutForm.postalCode.data,
                                                  createCheckoutForm.shippingMethod.data, CardType, CardNumber,
                                                  createCheckoutForm.expiryDate.data,
                                                  createCheckoutForm.cardVerificationNumber.data, deliveryDate, 'p')

        checkoutInformation.set_total(total)
        checkoutDict[checkoutInformation.get_checkoutID()] = checkoutInformation
        db['Checkouts'] = checkoutDict
        db['CheckoutCountID'] = CheckoutInformation.count

        # remove inventory
        for key in candyDict:
            candy = candyDict.get(key)
            stock = candy.get_candyStockLevel()
            for cart in cartDict:
                cart = cartDict.get(cart)
                if candy.get_candyName() == cart.get_candyName():
                    quantity = cart.get_quantity()
                    stock -= quantity
                    candy.set_candyStockLevel(stock)


        db['shoppingCart'] = cartDict
        db1['Candy'] = candyDict
        db1.close()
        db.close()

        # for receipt
        checkoutList = []
        checkoutList.append(checkoutInformation)

        name = " " + createCheckoutForm.firstName.data + " " + createCheckoutForm.lastName.data
        id = str(checkoutInformation.get_checkoutID())

        try:
            msg = Message("Receipt Number", sender="sugaricandyshop@gmail.com",
                          recipients=[createCheckoutForm.email.data])  # rmb set back createCheckoutForm.email.data
            msg.body = "Dear" + name + ",\n\nThank you for shopping with us!\nYour receipt number is: " + id + "\n\nDo be reminded that you can print a copy of the receipt page and keep it as a reference if necessary.\n\nBest regards,\nSugari Team"
            mail.send(msg)
            print('Email has been sent')

        except:
            print('Email not found')

        return render_template('receipt.html', checkoutList=checkoutList, cartList=cartList, shippingFee=shippingFee,
                               totalsubtotal=totalsubtotal, total=total)
    # Get (first load the page) or when validation fails
    return render_template('checkout.html', form=createCheckoutForm, cartList=cartList, total=total)


@app.route('/resendemail/<int:id>/', methods=['GET', 'POST'])
def resendemail(id):
    # cart information
    cartDict = {}
    subtotal = 0
    totalsubtotal = 0
    total = 0

    db = shelve.open('storage.db', 'r')

    try:
        cartDict = db['shoppingCart']
        db.close()
    except:
        print('Error in retrieving cart items from storage.db')

    cartList = []
    for key in cartDict:
        candy = cartDict.get(key)
        print(candy)
        cartList.append(candy)

        subtotal = float(candy.get_subtotal())
        totalsubtotal += subtotal
        total = float(total)
        total += subtotal
        total = "{:.2f}".format(float(total))

    # sending email
    checkoutDict = {}
    db = shelve.open('storage.db', 'w')
    checkoutDict = db['Checkouts']

    checkout = checkoutDict.get(id)
    checkoutList = [checkout]
    name = " " + checkout.get_firstName() + " " + checkout.get_lastName()
    id = str(id)

    total = float(total)
    if checkout.get_shippingMethod() == 'regular':
        deliveryDate = date.today() + timedelta(days=14)
        shippingFee = 0
    elif checkout.get_shippingMethod() == 'express':
        deliveryDate = date.today() + timedelta(days=5)
        shippingFee = 3.50
        total += 3.50

    name = " " + checkout.get_firstName() + " " + checkout.get_lastName()
    id = str(id)

    try:
        msg = Message("Receipt Number", sender="sugaricandyshop@gmail.com",
                      recipients=[checkout.get_email()])  # rmb set back createCheckoutForm.email.data
        msg.body = "Dear" + name + ",\n\nThank you for shopping with us!\nYour receipt number is: " + id + "\n\nDo be reminded that you can print a copy of the receipt page and keep it as a reference if necessary.\n\nBest regards,\nSugari Team"
        mail.send(msg)
        print('Email has been sent')

    except:
        print('Email not found')

    return render_template('receipt.html', checkoutList=checkoutList, cartList=cartList, shippingFee=shippingFee,
                           totalsubtotal=totalsubtotal, total=total)


@app.route('/clear', methods=['GET', 'POST'])
def clear():
    # clear shopping cart after checkout
    cartDict = {}
    db = shelve.open('storage.db', 'w')
    cartDict = db['shoppingCart']

    cartDict = {}
    db['shoppingCart'] = cartDict
    db.close()

    return redirect(url_for('homepage'))

@app.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    return render_template('aboutus.html')


@app.route('/s_deliveryorders', methods=['GET', 'POST'])
def s_deliveryorders():
    checkoutDict = {}
    checkoutList = []

    try:
        db = shelve.open('storage.db', 'r')
        checkoutDict = db['Checkouts']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()


    for key in checkoutDict:
        checkout = checkoutDict.get(key)
        checkoutList.append(checkout)

    return render_template('s_deliveryorders.html', checkoutList=checkoutList)


@app.route('/s_updatedeliveryorders/<int:id>/', methods=['GET', 'POST'])
def s_updatedeliveryorders(id):
    updateDeliveryForm = UpdateDeliveryForm(request.form)
    if request.method == 'POST' and updateDeliveryForm.validate():
        checkoutDict = {}
        db = shelve.open('storage.db', 'w')
        checkoutDict = db['Checkouts']

        order = checkoutDict.get(id)
        order.set_phone(updateDeliveryForm.phone.data)
        order.set_email(updateDeliveryForm.email.data)
        order.set_address(updateDeliveryForm.address.data)
        order.set_postalCode(updateDeliveryForm.postalCode.data)
        order.set_deliveryStatus((updateDeliveryForm.deliveryStatus.data))

        db['Checkouts'] = checkoutDict
        db.close()

        return redirect(url_for('s_deliveryorders'))

    else:
        checkoutDict = {}
        db = shelve.open('storage.db', 'r')
        checkoutDict = db['Checkouts']
        db.close()

        order = checkoutDict.get(id)
        print(order.get_firstName(), order.get_lastName(), order.get_phone())
        # name, stock, price, category

        updateDeliveryForm.firstName.data = order.get_firstName()
        updateDeliveryForm.lastName.data = order.get_lastName()
        updateDeliveryForm.phone.data = order.get_phone()
        updateDeliveryForm.email.data = order.get_email()
        updateDeliveryForm.address.data = order.get_address()
        updateDeliveryForm.postalCode.data = order.get_postalCode()
        updateDeliveryForm.shippingMethod.data = order.get_shippingMethod()
        updateDeliveryForm.deliveryStatus.data = order.get_deliveryStatus()

        return render_template('s_updatedeliveryorders.html', form=updateDeliveryForm)


@app.route('/create_feedback', methods=['GET', 'POST'])
def create_feedback():
    createFeedbackForm = CreateFeedbackForm(request.form)
    if request.method == 'POST' and createFeedbackForm.validate():
        feedbackDict = {}
        db = shelve.open('storage.db', 'c')
        try:
            feedbackDict = db['Feedbacks']
            feedback_id = db["feedback_id"]
            feedback_id += 1
            db["feedback_id"] = feedback_id
        except:
            print("Error in retrieving feedback from Feedback.db.")
            feedback_id = 1
            db["feedback_id"] = 1

        feedback = Feedback(feedback_id, createFeedbackForm.firstName.data, createFeedbackForm.lastName.data,
                            createFeedbackForm.email.data, createFeedbackForm.phone.data,
                            createFeedbackForm.region.data, createFeedbackForm.surveyOne.data,
                            createFeedbackForm.surveyTwo.data, createFeedbackForm.improvements.data)
        feedbackDict[feedback.get_feedbackID()] = feedback
        db['Feedbacks'] = feedbackDict

        db.close()

        return redirect(url_for('feedbacksubmission'))
    return render_template('create_feedback.html', form=createFeedbackForm)


@app.route('/retrieve_feedback')
def retrieve_feedback():
    feedbackDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        feedbackDict = db['Feedbacks']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()

    feedbackList = []
    for key in feedbackDict:
        feedback = feedbackDict.get(key)
        feedbackList.append(feedback)

    return render_template('retrieve_feedback.html', feedbackList=feedbackList, count=len(feedbackList))


@app.route('/deleteFeedback/<int:id>/', methods=['POST'])
def deleteFeedback(id):
    feedbackDict = {}
    # retrieve from persistance
    db = shelve.open('storage.db', 'w')

    feedbackDict = db['Feedbacks']

    # delete the record from the list
    feedbackDict.pop(id)

    # save the list
    db['Feedbacks'] = feedbackDict

    db.close()

    return redirect(url_for('retrieve_feedback'))


@app.route('/view_feedback/<int:id>', methods=['POST'])
def view_feedback(id):
    feedbackDict = {}
    db = shelve.open('storage.db', 'r')
    feedbackDict = db['Feedbacks']
    db.close()

    feedbackList = []
    feedback = feedbackDict.get(id)
    feedbackList.append(feedback)

    return render_template('view_feedback.html', feedbackList=feedbackList, count=len(feedbackList))


@app.route('/feedbacksubmission', methods=['GET', 'POST'])
def feedbacksubmission():
    return render_template('feedbacksubmission.html')


@app.route('/customerdetails', methods=['GET', 'POST'])
def customerdetails():
    customerChange = CustomerChange(request.form)
    print(request.method)
    if request.method == 'POST':
        db = shelve.open('storage.db', 'w')
        customerDict = db["Customers"]
        logincustomer = ""
        logincustomer=loginUser.user
        print("UPDATINGGG")
        customer = customerDict.get(logincustomer)
        customer.set_firstName(customerChange.firstname.data)
        customer.set_lastName(customerChange.lastname.data)
        customer.set_gender(customerChange.gender.data)
        customer.set_email(customerChange.email.data)


        if customerChange.password.data != "":
            print("CUSTOMER CHANGE")
            print(customerChange.password.data)
            usersDict = {}
            usersDict = db["Users"]
            user=usersDict.get(logincustomer)
            db["Users"] = usersDict

            customer.set_password(customerChange.password.data)
            print(user)
            user.set_password(customerChange.password.data)

        customer.set_contactNo(customerChange.contactNo.data)

        db["Users"] = usersDict
        db["Customers"] = customerDict
        db.close()

        return redirect(url_for('dropsession'))
    else:
        customerDict = {}
        logincustomer = ""
        db2 = shelve.open('storage.db', 'r')
        #id = db2['User']
        customerDict = db2["Customers"]
        logincustomer=loginUser.user
        db2.close()
        print("LOGIN CUSTOMER")
        print(logincustomer)

        customer = customerDict.get(loginUser.user)
        print("LOGIN USER STUFF")
        print(customer)
        print(customerDict)
        customerChange.firstname.data = customer.get_firstName()
        customerChange.lastname.data = customer.get_lastName()
        customerChange.gender.data = customer.get_gender()
        customerChange.email.data = customer.get_email()
        customerChange.password.data = customer.get_password()
        customerChange.contactNo.data = customer.get_contactNo()
        customerChange.membStatus.data = customer.get_membStatus()
        customerChange.membPoints.data = customer.get_membPoints()

        return render_template('customerdetails.html', form=customerChange, id=logincustomer)

@app.route("/create_membership", methods=["GET", "POST"])
def create_membership():
    createMemberForm = CreateCustomer(request.form)

    try:
        db2 = shelve.open('storage.db', 'w')
        staffDict = db2['Staff']

    except:
        print('Error in retrieving staff from storage.db')
        flash('There is no staff. You need a staff to sign up.')
        flash(Markup('Click <a href="/create_staff" class="alert-link">here</a> to create a staff.'))
        return redirect(url_for('login'))

    if request.method == "POST" and createMemberForm.validate():
        customersDict = {}
        usersDict = {}
        db = shelve.open('storage.db', 'c')

        try:
            customersDict = db["Customers"]
            usersDict = db["Users"]
            User.countID = db["UserID"]

        except:
            print("Error in retrieving Members from storage.db.")

        customer = Customer(createMemberForm.firstname.data, createMemberForm.lastname.data,
                            createMemberForm.gender.data, createMemberForm.email.data,
                            createMemberForm.password.data,createMemberForm.contactNo.data, 0)


        customer.set_accumulation()
        customer.set_membStatus()
        customer.set_type("C")

        customerlogin = Login(customer.get_userID(), createMemberForm.password.data, customer.get_type())
        print("created customer login")
        customersDict[customer.get_userID()] = customer

        print("BEFORE")
        print(usersDict)

        usersDict[customer.get_userID()] = customerlogin

        print("AFTER")
        print(usersDict)

        db["Customers"] = customersDict
        db["UserID"] = User.countID
        db["Users"] = usersDict

        db.close()
        return redirect(url_for("homepage"))
    return render_template("signup.html", form=createMemberForm)

@app.route("/s_create_membership", methods=["GET", "POST"])
def s_create_membership():
    createMemberForm = s_CreateCustomer(request.form)
    if request.method == "POST" and createMemberForm.validate():
        customersDict = {}
        usersDict = {}
        db = shelve.open('storage.db', 'w')

        try:
            customersDict = db["Customers"]
            User.countID = db["UserID"]
            print('C1:')
            print(User.countID)

        except:
            print("Error in retrieving Members from storage.db.")

        try:
            usersDict = db["Users"]

        except:
            print("DOES NOT EXIST")

        customer = Customer(createMemberForm.firstname.data, createMemberForm.lastname.data,
                                     createMemberForm.gender.data, createMemberForm.email.data,
                                     createMemberForm.password.data, createMemberForm.contactNo.data,createMemberForm.membPoints.data)
        customer.set_accumulation()
        customer.set_membStatus()
        customer.set_type("C")

        customerlogin = Login(customer.get_userID(), createMemberForm.password.data, customer.get_type())

        customersDict[customer.get_userID()] = customer
        usersDict[customer.get_userID()] = customerlogin
        print(usersDict)
        db["Customers"] = customersDict
        db["UserID"] = User.countID
        db["Users"] = usersDict

        db.close()
        return redirect(url_for("s_membershiplist"))
    return render_template("s_createcustomer.html", form=createMemberForm)


@app.route("/s_membershiplist")
def s_membershiplist():
    customersDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        customersDict = db["Customers"]
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()

    customersList = []
    for key in customersDict:
        customer = customersDict.get(key)
        customersList.append(customer)
    return render_template("s_membershiplist.html", customersList=customersList, count=len(customersList))

@app.route('/managePoints/<int:id>', methods=['GET', 'POST'])
def managePoints(id):
    managePoints = ManagePoints(request.form)
    if request.method == "POST" and managePoints.validate():
        customerDict = {}
        db = shelve.open('storage.db', 'w')
        customerDict = db["Customers"]
        customer = customerDict.get(id)

        if managePoints.type.data == "A": #ADD
            customer.add_points(managePoints.value.data)
        elif managePoints.type.data == "D": #DEDUCT
            if customer.get_membPoints() >= managePoints.value.data:
                customer.deduct_points(managePoints.value.data)
            elif customer.get_membPoints() < managePoints.value.data:
                flash('Not enough points to deduct.')
                return redirect(url_for("s_membershiplist"))
        customer.set_membStatus()
        db["Customers"] = customerDict
        db.close()
        return redirect(url_for("s_membershiplist"))
    return render_template("s_managepoints.html", form=managePoints)

@app.route('/updateMember/<int:id>', methods=['GET', 'POST'])
def updateMember(id):
    updateCustomer = UpdateCustomer(request.form)
    if request.method == 'POST' and updateCustomer.validate():
        customerDict = {}
        db = shelve.open('storage.db', 'w')
        customerDict = db["Customers"]

        customer = customerDict.get(id)
        customer.set_firstName(updateCustomer.firstname.data)
        customer.set_lastName(updateCustomer.lastname.data)
        customer.set_gender(updateCustomer.gender.data)
        customer.set_email(updateCustomer.email.data)

        if updateCustomer.password.data != "":
            print(updateCustomer.password.data)
            usersDict = {}
            usersDict = db["Users"]
            user=usersDict.get(id)
            user.set_password(updateCustomer.password.data)
            db["Users"] = usersDict

            customer.set_password(updateCustomer.password.data)

        customer.set_contactNo(updateCustomer.contactNo.data)
        customer.set_membPoints(updateCustomer.membPoints.data)

        db["Customers"] = customerDict
        db.close()

        return redirect(url_for('s_membershiplist'))
    else:
        customerDict = {}
        db = shelve.open('storage.db', 'r')
        customerDict = db["Customers"]
        db.close()

        customer = customerDict.get(id)
        updateCustomer.firstname.data = customer.get_firstName()
        updateCustomer.lastname.data = customer.get_lastName()
        updateCustomer.gender.data = customer.get_gender()
        updateCustomer.email.data = customer.get_email()
        updateCustomer.password.data = customer.get_password()
        updateCustomer.contactNo.data = customer.get_contactNo()
        updateCustomer.membStatus.data = customer.get_membStatus()
        updateCustomer.membPoints.data = customer.get_membPoints()
        return render_template('s_updatecustomer.html', form=updateCustomer, id=id)


@app.route('/deleteMember/<int:id>', methods=['POST'])
def deleteMember(id):
    customersDict = {}
    usersDict = {}
    db = shelve.open('storage.db', 'w')

    usersDict = db["Users"]
    customersDict = db["Customers"]

    customersDict.pop(id)
    usersDict.pop(id)

    db["Customers"] = customersDict
    db["Users"] = usersDict

    db.close()

    return redirect(url_for('s_membershiplist'))



@app.route('/create_staff', methods=['GET', 'POST'])
def create_staff():
    createstaff = CreateStaff(request.form)

    if request.method == 'POST' and createstaff.validate():
        staffDict = {}
        usersDict = {}
        db = shelve.open("storage.db", "c")  # Create, read and write

        try:
            staffDict = db["Staff"]
            usersDict = db["Users"]
            User.countID = db["UserID"]
            print('S1:')
            print(User.countID)
        except:
            print("Error in retrieving staff from storage.db")

        # Create an instance of class User
        staff = Staff(createstaff.firstname.data, createstaff.lastname.data, createstaff.gender.data,
                            createstaff.email.data, createstaff.password.data)
        staff.set_type("S")

        stafflogin = Login(staff.get_userID(), createstaff.password.data, staff.get_type())

        print("BEFORE STAFF")
        print(usersDict)

        # Save the user instance in usersDict, using userID as the key
        staffDict[staff.get_userID()] = staff
        usersDict[staff.get_userID()] = stafflogin

        print("AFTER STAFF")
        print(usersDict)

        # Save dictionary to db
        db["Staff"] = staffDict
        db["Users"] = usersDict
        print("DATABASE")
        print(db["Users"])

        # After create the user, save the countID to shelve/persistance
        db["UserID"] = User.countID
        print('S2:')
        print(User.countID)

        # Module / file Name.ClassName.class_attribute
        db.close()
        return redirect(url_for('s_stafflist'))
    return render_template('s_createstaff.html', form=createstaff)


@app.route('/s_stafflist', methods=['GET', 'POST'])  # retrieve candies
def s_stafflist():
    staffDict = {}
    db = shelve.open('storage.db', 'r')
    staffDict = db['Staff']
    db.close()
    staffList = []
    for key in staffDict:
        staff = staffDict.get(key)
        staffList.append(staff)
        hidden = "*" * len(staff.get_password())
    return render_template('s_stafflist.html', staffList=staffList, count=len(staffList))


@app.route('/updateStaff/<int:id>/', methods=['GET', 'POST'])
def updateStaff(id):
    updateStaff = UpdateStaff(request.form)

    db = shelve.open("storage.db", "r")
    User.countID = db["UserID"]
    db.close()

    if request.method == 'POST' and updateStaff.validate():
        staffDict = {}
        usersDict = {}

        db = shelve.open('storage.db', 'w')
        staffDict = db["Staff"]
        usersDict = db["Users"]

        staff = staffDict.get(id)
        user = usersDict.get(id)

        staff.set_firstName(updateStaff.firstname.data)
        staff.set_lastName(updateStaff.lastname.data)
        staff.set_gender(updateStaff.gender.data)
        staff.set_email(updateStaff.email.data)

        if updateStaff.password.data != "":
            print("NEW PASSWORD")
            print(updateStaff.password.data)
            staff.set_password(updateStaff.password.data)
            user.set_password(updateStaff.password.data)

            print(staff)
            print(user)

        db["Users"] = usersDict
        db["Staff"] = staffDict
        db.close()
        return redirect(url_for('s_stafflist'))

    else:
        staffDict = {}
        db = shelve.open('storage.db', 'r')
        staffDict = db["Staff"]
        db.close()

        staff = staffDict.get(id)

        # name, stock, price, category
        updateStaff.firstname.data = staff.get_firstName()
        updateStaff.lastname.data = staff.get_lastName()
        updateStaff.gender.data = staff.get_gender()
        updateStaff.email.data = staff.get_email()
        updateStaff.password.data = staff.get_password()

        return render_template('s_updateStaff.html', form=updateStaff, staffID=id)


@app.route('/deleteStaff/<int:id>/', methods=["POST"])
def deleteStaff(id):
    staffDict = {}
    usersDict = {}
    staffcount = 0
    # retrieve from persistence
    db = shelve.open("storage.db", "w")
    staffDict = db["Staff"]
    for key in staffDict:
        staffcount += 1
    if staffcount == 1:
        flash('There is only 1 staff. You need to have at least 2 staffs to delete a staff.')
        return redirect(url_for("s_stafflist"))

    usersDict = db["Users"]

    # delete the record from the list
    staffDict.pop(id)
    usersDict.pop(id)

    # save the list
    db["Staff"] = staffDict
    db["Users"] = usersDict
    db.close()

    return redirect(url_for("s_stafflist"))


@app.route('/chocolate', methods=['GET', 'POST'])
def chocolate():
    candyDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        candyDict = db['Candy']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()


    candyList = []
    candyInnerList = []
    counter = 0

    for key in candyDict:
        candy = candyDict.get(key)
        if candy.get_candyCategory() == 'C':
            candyInnerList.append(candy)
            counter += 1
            if counter % 3 == 0:
                candyList.append(candyInnerList)
                candyInnerList = []
    if len(candyInnerList) != 0:
        candyList.append(candyInnerList)
        candyInnerList = []

    db.close()

    return render_template('chocolate.html', candyList=candyList)


@app.route('/gummy', methods=['GET', 'POST'])
def gummy():
    candyDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        candyDict = db['Candy']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()

    candyList = []
    candyInnerList = []
    counter = 0

    for key in candyDict:
        candy = candyDict.get(key)
        if candy.get_candyCategory() == 'G':
            candyInnerList.append(candy)
            counter += 1
            if counter % 3 == 0:
                candyList.append(candyInnerList)
                candyInnerList = []
    if len(candyInnerList) != 0:
        candyList.append(candyInnerList)
        candyInnerList = []

    db.close()

    return render_template('gummy.html', candyList=candyList)


@app.route('/fizzy', methods=['GET', 'POST'])
def fizzy():
    candyDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        candyDict = db['Candy']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()

    candyList = []
    candyInnerList = []
    counter = 0

    for key in candyDict:
        candy = candyDict.get(key)
        if candy.get_candyCategory() == 'F':
            candyInnerList.append(candy)
            counter += 1
            if counter % 3 == 0:
                candyList.append(candyInnerList)
                candyInnerList = []
    if len(candyInnerList) != 0:
        candyList.append(candyInnerList)
        candyInnerList = []
    db.close()

    return render_template('fizzy.html', candyList=candyList)


@app.route('/specials', methods=['GET', 'POST'])
def specials():
    candyDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        candyDict = db['Candy']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()

    candyList = []
    candyInnerList = []
    counter = 0

    for key in candyDict:
        candy = candyDict.get(key)
        if candy.get_candyCategory() == 'S':
            candyInnerList.append(candy)
            counter += 1
            if counter % 3 == 0:
                candyList.append(candyInnerList)
                candyInnerList = []
    if len(candyInnerList) != 0:
        candyList.append(candyInnerList)
        candyInnerList = []

    db.close()

    return render_template('specials.html', candyList=candyList)


@app.route('/candy_description/<int:id>', methods=['POST'])
def candy_description(id):
    candyDict = {}
    db = shelve.open('storage.db', 'r')
    candyDict = db['Candy']
    db.close()

    candyList = []
    candy = candyDict.get(id)
    candyList.append(candy)

    return render_template('candy_description.html', candyList=candyList, count=len(candyList))


@app.route('/s_createsupplier', methods=['GET', 'POST'])
def s_createsupplier():
    createSupplierForm = CreateSupplierForm(request.form)

    if request.method == 'POST' and createSupplierForm.validate():
        supplierDict = {}
        db = shelve.open('storage.db', 'c')

        try:
            supplierDict = db['Suppliers']

            supplierList = []
            for key in supplierDict:
                supplier = supplierDict.get(key)
                supplierList.append(supplier)

            for supplier in supplierList:
                companyName = supplier.get_companyName()
                companyEmail = supplier.get_companyEmail()
                companyPhone = supplier.get_companyPhone()

                error1 = 'Company name, "' + createSupplierForm.companyName.data + '" already exist!'
                error2 = 'Email already exist'
                error3 = 'Company phone already exist'

                if createSupplierForm.companyName.data == companyName:
                    return render_template('s_createsupplier.html', form=createSupplierForm, error1=error1)
                elif createSupplierForm.companyEmail.data == companyEmail:
                    return render_template('s_createsupplier.html', form=createSupplierForm, error2=error2)
                elif createSupplierForm.companyPhone.data == companyPhone:
                    return render_template('s_createsupplier.html', form=createSupplierForm, error3=error3)

        except:
            print("Error in retrieving Supplier from storage.db.")

        supplier = Supplier(createSupplierForm.companyName.data, createSupplierForm.companyPhone.data,
                            createSupplierForm.companyEmail.data, createSupplierForm.address.data,
                            createSupplierForm.postalCode.data)

        supplierDict[createSupplierForm.companyName.data] = supplier
        db['Suppliers'] = supplierDict

        db.close()

        return redirect(url_for('s_retrievesupplier'))

    return render_template('s_createsupplier.html', form=createSupplierForm)


@app.route('/s_retrievesupplier')
def s_retrievesupplier():
    # Retrieve the data from persistance
    supplierDict = {}
    orderDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        supplierDict = db['Suppliers']
        orderDict = db['Orders']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()

    supplierList = []
    for key in supplierDict:

        supplier = supplierDict.get(key)
        supplierList.append(supplier)

        try:
            for key in orderDict:
                order = orderDict.get(key)
                if order.get_companyName() == supplier.get_companyName():
                    if order.get_deliveryStatus() == 'p':
                        num = supplier.get_numOrders() + 1
                        supplier.set_numOrders(num)
                    else:
                        supplier.set_numOrders(0)

        except:
            print('No orders')

    return render_template('s_retrievesupplier.html', supplierList=supplierList, count=len(supplierList))


@app.route('/s_updatesupplier/<id>/', methods=['GET', 'POST'])
def s_updatesupplier(id):
    updateSupplierForm = UpdateSupplierForm(request.form)

    if request.method == 'POST' and updateSupplierForm.validate():
        supplierDict = {}
        db = shelve.open('storage.db', 'w')
        supplierDict = db['Suppliers']

        supplier = supplierDict.get(id)
        supplier.set_companyName(updateSupplierForm.companyName.data)
        supplier.set_companyPhone(updateSupplierForm.companyPhone.data)
        supplier.set_companyEmail(updateSupplierForm.companyEmail.data)
        supplier.set_address(updateSupplierForm.address.data)
        supplier.set_postalCode(updateSupplierForm.postalCode.data)

        db['Suppliers'] = supplierDict
        db.close()

        return redirect(url_for('s_retrievesupplier'))

    else:
        supplierDict = {}
        db = shelve.open('storage.db', 'r')
        supplierDict = db['Suppliers']
        db.close()

        supplier = supplierDict.get(id)
        updateSupplierForm.companyName.data = supplier.get_companyName()
        updateSupplierForm.companyPhone.data = supplier.get_companyPhone()
        updateSupplierForm.companyEmail.data = supplier.get_companyEmail()
        updateSupplierForm.address.data = supplier.get_address()
        updateSupplierForm.postalCode.data = supplier.get_postalCode()

        return render_template('s_updatesupplier.html', form=updateSupplierForm)


@app.route('/s_createorder/<id>/', methods=['GET', 'POST'])
def s_createorder(id):
    supplierDict = {}
    orderDict = {}
    candyDict = {}

    db1 = shelve.open('storage.db', 'c')
    db2 = shelve.open('storage.db', 'r')
    supplierDict = db2['Suppliers']


    db2.close()

    try:
        orderDict = db1['Orders']
        order_id = db1['OrderCountID']
        order_id += 1

    except:
        print('Error in retrieving orders from storage.db')
        order_id = 1
        db1['OrderCountID'] = 1

    try:
        db3 = shelve.open('storage.db', 'w')
        candyDict = db3['Candy']
        db3.close()

    except:
        db3 = shelve.open('storage.db', 'c')
        db3.close()

    supplier = supplierDict.get(id)
    list = []
    for key in candyDict:
        c = candyDict.get(key)

        if supplier.get_companyName() == c.get_candySupplier():
            item = (c.get_candyName(), c.get_candyName())
            list.append(item)

    if len(list) == 0:
        flash(supplier.get_companyName() + " is not supplying any candy.")
        flash(Markup('Click <a href="/createCandy" class="alert-link">here</a> to create a candy for ' + supplier.get_companyName() + ' to supply.'))
        return redirect(url_for('s_retrievesupplier'))

    CreateOrderForm.product = SelectField('', [validators.DataRequired()], choices=list, default='')
    createOrderForm = CreateOrderForm(request.form)
    createOrderForm.companyName.data = supplier.get_companyName()

    if request.method == 'POST' and createOrderForm.validate():
        for key in candyDict:
            c = candyDict.get(key)

            if createOrderForm.product.data == c.get_candyName():
                productPrice = c.get_candyCostPrice()

        totalPrice = float(productPrice) * int(createOrderForm.productQuantity.data)
        totalPrice = "{:.2f}".format(float(totalPrice))

        order = Order(order_id, createOrderForm.companyName.data, createOrderForm.product.data,
                      createOrderForm.productQuantity.data, productPrice,
                      createOrderForm.deliveryDate.data, createOrderForm.deliveryStatus.data)
        order.set_totalPrice(totalPrice)

        orderDict[order.get_orderID()] = order
        db1['Orders'] = orderDict
        db1['OrderCountID'] = order_id

        db1.close()

        return redirect(url_for('s_retrieveorder'))
    return render_template('s_createorder.html', form=createOrderForm)


@app.route('/s_retrieveorder')
def s_retrieveorder():
    # Retrieve the data from persistance
    orderDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        orderDict = db['Orders']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()

    orderList = []
    for key in orderDict:
        order = orderDict.get(key)
        orderList.append(order)

    name = 'ALL'
    return render_template('s_retrieveorder.html', orderList=orderList, count=len(orderList), name=name)


@app.route('/retrieveSupplierOrders/<id>/', methods=['GET', 'POST'])
def retrieveSupplierOrders(id):
    # Retrieve the data from persistance
    supplierDict = {}
    orderDict = {}

    try:
        db = shelve.open('storage.db', 'r')
        supplierDict = db['Suppliers']
        orderDict = db['Orders']
        db.close()

    except:
        db = shelve.open('storage.db', 'c')
        db.close()

    supplier = supplierDict.get(id)
    companyName = supplier.get_companyName()

    orderList = []
    for key in orderDict:
        order = orderDict.get(key)
        if order.get_companyName() == companyName:
            if order.get_deliveryStatus() == 'p':
                orderList.append(order)

    name = companyName
    return render_template('s_retrieveorder.html', orderList=orderList, count=len(orderList), name=name)


@app.route('/s_updateorder/<int:id>/', methods=['GET', 'POST'])
def s_updateorder(id):
    updateOrderForm = UpdateOrderForm(request.form)

    if request.method == 'POST' and updateOrderForm.validate():
        orderDict = {}
        candyDict = {}
        db = shelve.open('storage.db', 'w')
        orderDict = db['Orders']
        candyDict = db['Candy']

        order = orderDict.get(id)
        order.set_companyName(updateOrderForm.companyName.data)
        order.set_product(updateOrderForm.product.data)
        order.set_productQuantity(updateOrderForm.productQuantity.data)
        order.set_productPrice(updateOrderForm.productPrice.data)
        order.set_deliveryStatus(updateOrderForm.deliveryStatus.data)

        # add here for the add products to inventory
        for key in candyDict:
            candy = candyDict.get(key)
            stock = candy.get_candyStockLevel()

            if order.get_deliveryStatus() == 'd':
                if candy.get_candyName() == updateOrderForm.product.data:
                    stock += int(updateOrderForm.productQuantity.data)
                    candy.set_candyStockLevel(stock)

                # set to todays date for delivery date if reach ealier or later than predicted time
                if updateOrderForm.deliveryDate.data != date.today():
                    order.set_deliveryDate(date.today())
                else:
                    order.set_deliveryDate(updateOrderForm.deliveryDate.data)

        db['Orders'] = orderDict
        db['Candy'] = candyDict
        db.close()

        return redirect(url_for('s_retrieveorder'))

    else:
        orderDict = {}
        db = shelve.open('storage.db', 'r')
        orderDict = db['Orders']
        db.close()

        order = orderDict.get(id)
        updateOrderForm.companyName.data = order.get_companyName()
        updateOrderForm.product.data = order.get_product()
        updateOrderForm.productQuantity.data = order.get_productQuantity()
        updateOrderForm.productPrice.data = order.get_productPrice()
        updateOrderForm.deliveryDate.data = order.get_deliveryDate()
        updateOrderForm.deliveryStatus.data = order.get_deliveryStatus()

        return render_template('s_updateorder.html', form=updateOrderForm)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login = LoginForm(request.form)
    customerDict = {}

    if request.method == 'POST' and login.validate():
        usersDict={}
        idList=[]
        try:
            db = shelve.open('storage.db', 'r')
            usersDict = db["Users"]
            db.close()
        except:
            usersDict={}

        if usersDict=={}:
            print('Error in retrieving suppliers from storage.db')
            flash('There are no users.')
            return redirect(url_for('login'))

        session.pop('staff', None)
        session.pop('customer', None)
        print("....")
        try:
            db = shelve.open('storage.db', 'r')
            usersDict = db["Users"]
            db.close()
        except:
            print("ERRORRRR")

        print(usersDict)
        for key in usersDict:
            user = usersDict.get(key)
            print(user.get_userID())
            idList.append(user.get_userID())
            if str(login.id.data) == str(user.get_userID()):
                print("ENTERED LOGIN")
                print(user.get_password())
                if login.password.data == user.get_password():
                    print(user.get_type())
                    if user.get_type()=="S":
                        session['staff'] = user.get_userID()
                        print(str(user.get_userID()) + ' logged in')
                        return redirect(url_for('s_menu'))
                    elif user.get_type()=="C":
                        session["customer"] = user.get_userID()
                        loginUser.user=login.id.data
                        print(str(user.get_userID()) + ' logged in')
                        return redirect(url_for('customerdetails'))
                else:
                    flash('Incorrect ID or Password.')
                    return redirect(url_for('login'))

        for number in idList:
            print("IN NUMBER")
            if str(login.id.data) != number:
                flash('Incorrect ID or Password.')
                return redirect(url_for('login'))





    return render_template('s_login.html', form=login)


@app.before_request
def before_request():
    g.staff = None
    if 'staff' in session:
        g.staff = session['staff']
    if "customer" in session:
        g.customer = session["customer"]


@app.route('/dropsession')
def dropsession():
    session.pop('staff', None)
    session.pop("customer", None)
    print('Logged out')
    return redirect(url_for('login'))


@app.route('/customerlogin', methods=['GET', 'POST'])
def customerlogin():
    customerlogin = CustomerLogin(request.form)
    if request.method == 'POST' and customerlogin.validate():
        customerDict = {}
        db = shelve.open('storage.db', 'w')
        customerDict = db["Customers"]
        # loginUser.loginUser.user = db['User']
        for key in customerDict:
            customer = customerDict.get(key)
            if customerlogin.username.data == customer.get_userID():
                if customerlogin.password.data == customer.get_password():
                    loginUser.user = customerlogin.username.data
                    # db['User'] = loginUser.loginUser.user
                    db.close()
                    return redirect(url_for('customerdetails'))
        else:
            db.close()
            return redirect(url_for('homepage'))
    return render_template('customerlogin.html', form=customerlogin)

if __name__ == '__main__':
    app.run(port=5005)
