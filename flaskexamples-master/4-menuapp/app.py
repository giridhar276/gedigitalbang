from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, validators


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'giridhar'
app.config['MYSQL_DB'] = 'myflaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

#Articles = Articles()

# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')




# Register Form Class
class RegisterForm(Form):
    empid  = StringField('EmpID ', [validators.Length(min=2, max=50)])    
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    location = StringField('Location', [validators.Length(min=4, max=25)])
    technology = StringField('Technology', [validators.Length(min=4, max=25)])


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        empid    = form.empid.data
        location = form.location.data
        technology = form.technology.data
        

        # Create cursor
        cur = mysql.connection.cursor()

        query = "INSERT INTO employees(name, email, username, empid,location,technology) VALUES('{}','{}','{}',{},'{}','{}')".format(name,email,username,empid,location,technology)
        # Execute query
        cur.execute(query)

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered now', 'success')

        #return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard')
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")
    # Show articles only from the user logged in 
    result = cur.execute("SELECT * FROM employees")

    articles = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles)
    else:
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()




if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
