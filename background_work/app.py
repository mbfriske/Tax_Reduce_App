import os

import pandas as pd
import numpy as np

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


from config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD

app = Flask(__name__)

#################################################
# Database Setup
#################################################


app.config['SQLALCHEMY_DATABASE_URI'] = (f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}')
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
account_apprl_year_2019 = Base.classes.account_apprl_year_2019
account_apprl_year_2018 = Base.classes.account_apprl_year_2018
account_apprl_year_2017 = Base.classes.account_apprl_year_2017
account_apprl_year_2016 = Base.classes.account_apprl_year_2016
account_apprl_year_2015 = Base.classes.account_apprl_year_2015
account_info_2019=Base.classes.account_info_2019
account_info_2018=Base.classes.account_info_2018
account_info_2017=Base.classes.account_info_2017
account_info_2016=Base.classes.account_info_2016
account_info_2015=Base.classes.account_info_2015


# engine
engine = create_engine(f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}')

# render index.html on homepage
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/account_num")
def acct_num():
    """Return a list of states."""

    stmt = "db.session.query(account_apprl_year_2019).statement"
    df = pd.read_sql_query(stmt, db.session.bind)
    acct_num_list = list(df.account_num)

    # Return a list of the column states
    return jsonify(acct_num_list)


@app.route("/account_number/<account_num>")
def account_number(account_num):
    """Return address data"""

    # perform the sql query for account_num
    sel = [
        account_apprl_year_2019.account_num,
        account_apprl_year_2019.city_taxable_val,
        account_apprl_year_2019.city_juris_desc,
    ]

    results = db.session.query(
        *sel).filter(account_apprl_year_2019.account_num == account_num).all()

    # Create a dictionary entry for each row of math data information
    account_num_dict = {}
    for result in results:
        account_num_dict["account_number"] = result[0]
        account_num_dict["city_taxable_value"] = result[1]
        account_num_dict["city_juris_desc"] = result[2]

   # Return Jsonified data ()
    print(account_num_dict)
    return jsonify(account_num_dict)



@app.route("/address/<account_num>")
def address(account_num):
    """Return address data"""

    # perform the sql query for account_num
    sel = [
        account_info_2019.account_num,
        account_info_2019.street_num,
        account_info_2019.full_street_name,
        account_info_2019.unit_id,
        account_info_2019.property_city,
        account_info_2019.property_zipcode,
    ]

    results = db.session.query(
        *sel).filter(account_info_2019.account_num == account_num).all()

    # Create a dictionary entry for each row of math data information
    address_dict = {}
    for result in results:
        address_dict["account_number"] = result[0]
        address_dict["street_number"] = result[1]
        address_dict["street_name"] = result[2]
        address_dict["unit_id"] = result[3]
        address_dict["property_city"] = result[4]
        address_dict["property_zipcode"] = result[5]

   # Return Jsonified data ()
    print(address_dict)
    return jsonify(address_dict)



@app.route("/data/<account_num>")
def data(account_num):

    # query: join tables
    query = (f"select ai.account_num, street_num, street_half_num, full_street_name, unit_id, property_city, left(property_zipcode,5) as Zipcode, aay.tot_val \
            from account_info_2019 as ai \
            INNER JOIN account_apprl_year_2019 as aay on ai.account_num = aay.account_num \
            where ai.account_num = '{account_num}'")

    results = engine.execute(query).fetchall()  

    test_dict = {}
    for result in results:
        test_dict["account_number"] = result[0]
        test_dict["street_number"] = result[1]
        test_dict["street_half_num"] = result[2]
        test_dict["full_street_name"] = result[3]
        test_dict["unit_id"] = result[4]
        test_dict["property_city"] = result[5]
        test_dict["property_zipcode"] = result[6]
        test_dict["total_value"] = int(result[7])

    return jsonify(test_dict)


@app.route("/addresses")
def addresses():

    # query: join tables
    query_1 = "select ai.account_num, concat(street_num, ' ', ai.full_street_name, ' ', ai.unit_id, ' ', ai.property_city, ' ', left(ai.property_zipcode,5))\
    from account_info_2019 as ai where ai.division_cd = 'RES' limit 10"

    results = engine.execute(query_1).fetchall()  


    address_list =[]

    addresses_dict = {} 
    for result in results:
        addresses_dict = {
        'account_number':result[0],
        'address':result[1]
        }

        address_list.append(addresses_dict)


    return jsonify(address_list)


if __name__ == "__main__":
    app.run(debug=True)