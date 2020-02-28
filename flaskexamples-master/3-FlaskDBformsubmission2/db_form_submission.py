from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    if request.method == 'GET':
        return render_template('forms/basic_form.html')
    elif request.method == 'POST':
        kwargs = {
            'database': request.form['database'],
            'table': request.form['table'],
	    'filter':request.form['filter'],
            'submit_value': request.form['submit'],
        }
        database = kwargs["database"]
        table    = kwargs["table"]
        condition   = kwargs["filter"]
        
        db  = pymysql.connect(host="localhost", port=3306, user="root", passwd="india@123", db=database )
        cursor = db.cursor()
        
        sql = "select * from " + table
        cursor.execute(sql)
        details = [ ",".join(row) for row in cursor.fetchall()]
        details = list(filter(lambda x : condition in x , details))
        
        return render_template(
            'forms/basic_form_result.html', data = details)


app.run(debug = True)