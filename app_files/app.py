import os

import pandas as pd
import numpy as np
import json

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

import psycopg2
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine



app = Flask(__name__)

#################################################
# Database Setup for Heroku
#################################################
from boto.s3.connection import S3Connection

PGHOST =  os.environ.get('PGHOST', None)
PGDATABASE =  os.environ.get('PGDATABASE', None)
PGUSER =  os.environ.get('PGUSER', None)
PGPASSWORD =  os.environ.get('PGPASSWORD', None)
PGPORT =  os.environ.get('PGPORT', None)

conn = psycopg2.connect(
            dbname=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD,
            host=PGHOST,
            port=PGPORT
            )

cur = conn.cursor()

#################################################
# Database Setup for Local
#################################################

# from config import PGHOST, PGDATABASE, PGUSER, PGPASSWORD
# from config import u, p


# app.config['SQLALCHEMY_DATABASE_URI'] = (f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}')
# db = SQLAlchemy(app)


#################################################
# Save references to each table

# Base = automap_base()

# Base.prepare(db.engine, reflect=True)

# account_apprl_year_2019 = Base.classes.account_apprl_year_2019
# account_apprl_year_2018 = Base.classes.account_apprl_year_2018
# account_apprl_year_2017 = Base.classes.account_apprl_year_2017
# account_apprl_year_2016 = Base.classes.account_apprl_year_2016
# account_apprl_year_2015 = Base.classes.account_apprl_year_2015
# account_info_2019=Base.classes.account_info_2019
# account_info_2018=Base.classes.account_info_2018
# account_info_2017=Base.classes.account_info_2017
# account_info_2016=Base.classes.account_info_2016
# account_info_2015=Base.classes.account_info_2015
# predictions=Base.classes.predictions

# engine
# engine = create_engine(f'postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}')

# render index.html on homepage
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/addresses")
def addresses():

    # query: join tables
    # query_1 = "select ai.account_num, concat(street_num, ' ', ai.full_street_name, ' ', ai.unit_id, ' ', ai.property_city, ' ', left(ai.property_zipcode,5))\
    # from account_info_2019 as ai where ai.division_cd = 'RES' limit 1000000"

    # # results = engine.execute(query_1).fetchall()  
    # cur.execute(query_1)
    # results = cur.fetchall()


    # address_list =[]

    # addresses_dict = {} 
    # for result in results:
    #     addresses_dict = {
    #     'account_number':result[0],
    #     'address':result[1]
    #     }

    #     address_list.append(addresses_dict)

    with app.open_resource('static/addresses.json') as f:
        address_list = json.load(f)

    return jsonify(address_list)



@app.route("/attributes/<account_num>")
def attributes(account_num):
    """Return attribute data"""

    # query: join tables
    query_2 = (f"SELECT rd.account_num, rd.act_age, rd.tot_living_area_sf, rd.num_kitchens,\
                rd.num_full_baths, rd.num_half_baths, rd.num_bedrooms, aay.tot_val\
                FROM res_detail_2019 as rd\
                INNER JOIN account_apprl_year_2019 as aay on rd.account_num = aay.account_num\
                where rd.account_num = '{account_num}'")

    # results = engine.execute(query_2).fetchall() 
    cur.execute(query_2)
    results = cur.fetchall()     

    attribute_list =[]

    attribute_dict = {} 
    for result in results:
        attribute_dict = {
        'account_number':result[0],
        'property_age':+result[1],
        'total_living_square_feet': +result[2],
        'number_kitchens': +result[3],
        'number_full_baths': +result[4],
        'number_half_baths': +result[5],
        'number_bedrooms':+result[6],
        'total_value':int(result[7]),
        }

        attribute_list.append(attribute_dict)

    return jsonify(attribute_list)


@app.route("/prediction/<account_num>")
def prediction(account_num):
    """Return prediction data"""

    # query: join tables
    query_3 = (f"SELECT ai.account_num, p.appraisal_yr, p.prediction, p.confidence, uncertainty, aay2019.tot_val, tot_val_pred \
                FROM account_info_2019 as ai \
                INNER JOIN account_apprl_year_2019 as aay2019 on ai.account_num = aay2019.account_num \
                LEFT OUTER JOIN predictions as p on ai.account_num = p.account_num where ai.account_num = '{account_num}'")

    # results = engine.execute(query_3).fetchall() 
    cur.execute(query_3)
    results = cur.fetchall()     

    prediction_dict = {}

    for result in results:
        prediction_dict["account_number"] = result[0]
  #     prediction_dict["appraisal_year"] = +result[1]
        if result[2] is None:
            prediction_dict["prediction"] = ''
        else:
            prediction_dict["prediction"] = result[2]
  #      prediction_dict["confidence"] = +result[3]
  #      prediction_dict["uncertainty"] = +result[4]
        if result[5] is None:
            prediction_dict["tot_val"] = 'unknown'
        else:
            prediction_dict["tot_val"] = str(('${:0,.0f}'.format(result[5])))
        if result[6] is None:
            prediction_dict["tot_val_pred"] = 'unknown'
        else:
            prediction_dict["tot_val_pred"] = str(('${:0,.0f}'.format(result[6])))     
            print(str(('${:,f}'.format(result[6]))))       

    # Return Jsonified data ()
    return jsonify(prediction_dict)

if __name__ == "__main__":
    app.run()