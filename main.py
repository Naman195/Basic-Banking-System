
# THE SPARK FOUNDATION
# GRIPNOV20
# Name  = NAMAN ARORA


from flask import * 

import sqlite3

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/')
def login():

    return render_template("login.html")

@app.route('/home')
def home():
    
    return render_template("index.html")


@app.route('/customerlist')
def customers_list():

     conn = sqlite3.connect('bank_management.db')

     temp = conn.execute("select * from customers_list")

     return render_template("customers_list.html" , data = temp)



@app.route('/viewcustomer/<int:Account_no>')


def viewcustomer(Account_no):

    conn = sqlite3.connect("bank_management.db")

    temp1 = conn.execute('select * from customers_list')

    temp2 = conn.execute('select * from customers_list')


    temp = conn.execute('select * from customers_list where Account_no=?',(Account_no,))

    # test = temp.fetchone()

    # name = test[2]

    test = conn.execute('select * from customers_list where Account_no=?',(Account_no,))
    
    for i in test:
        Account_no = i[1]
        name = i[2]



    # # print(name)


    return render_template("viewcustomer.html" , data = temp, data1 = temp1, data2 = test, name = name, no = Account_no, data3 = temp2)


@app.route("/transfer/<int:Sender>", methods = ['POST','GET'])

def transfer(Sender):

    if request.method == 'POST':

        name=request.form['name']
        no=request.form['no']
        amount=request.form['credit']

        amount = int(amount)

        conn = sqlite3.connect("bank_management.db")


        temp = conn.execute('select Account_balance from customers_list where Account_no=?',(Sender,))



        for i in temp:

            test = i[0]

        temp1 = conn.execute('select Account_balance from customers_list where Account_no=?',(no,))

        for i in temp1:
            
            test1 = i[0]

        if (test>0):

            if(amount<=test):                
                debit  = test - amount

                credit = test1 + amount

                change = 'update customers_list set Account_balance=? where Account_no=?'

                data = (debit,Sender)

                conn.execute(change,(data))

                conn.commit()
                
                change = 'update customers_list set Account_balance=? where Account_no=?'

                data = (credit,no)

                conn.execute(change,(data))

                conn.commit()

                flash("Your Amount Has been Transferred Successfully!", "success")


                return redirect('/customerlist')


            else:
                flash("Insufficient Balance! Please enter a valid amount.", "danger")
                return redirect('/customerlist')

                 

        else:
            flash("Your Account Balance is Null", "danger")
            return redirect('/customerlist')
            

        
@app.route("/about")

def about():

    return render_template("about.html")




if __name__=="__main__":
    app.run(debug=True)