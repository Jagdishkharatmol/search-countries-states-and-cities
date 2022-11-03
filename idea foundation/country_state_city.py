from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
import json
import ast
 
 
app = Flask(__name__)
app.secret_key = 'ideafoundation'
 
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'username'
app.config['MYSQL_DATABASE_PASSWORD'] = 'passwoord'
app.config['MYSQL_DATABASE_DB'] = 'idea'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



try:
    conn = mysql.connect()
    cursor =conn.cursor()
except Exception as e:
    print("Error:",e)




@app.route('/',methods=["GET"])
def show_data():
    fetch_countries_data=f"""SELECT id, name, iso3, iso2, numeric_code, phone_code, capital,
                               currency, currency_name, currency_symbol, tld, native,
                               region, subregion, timezones, translations, latitude,
                               longitude, emoji, emojiU FROM country_info"""
    cursor.execute(fetch_countries_data)
    global countries
    countries = cursor.fetchall()
    #cursor.close()
    return render_template('index.html',countries=countries)


@app.route('/state/<string:id>/',methods=["GET",'POST'])
def fill_data_state(id):
    fetch_state_data=f"select states from country_info where id={id}";
    cursor.execute(fetch_state_data)
    global states
    states = cursor.fetchall()
    states=states[0][0]
    states=ast.literal_eval(states)
    return render_template('index.html',states=states,countries=countries)

@app.route('/city/<string:id>/',methods=["GET",'POST'])
def fill_data_city(id):
    global cities
    cities=states[int(id)]['cities']
    return render_template('index.html',states=states,countries=countries,cities=cities)
    


if __name__=='__main__':
    app.run(debug=False)

