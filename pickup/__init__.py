import os
import json
from flask import Flask, render_template
from pymongo import MongoClient

def load_mongo(db:str()):
    password = input('Password: ')
    client = MongoClient("mongodb+srv://aar0npham:{}@food-izclc.mongodb.net/test?retryWrites=true&w=majority".format(password))
    db = client[db]
    return db

def write_db(db, col, file):
    dump = load_mongo(db)
    cur = dump[col].find({})
    count = dump[col].count_document({})
    with open(file, 'w') as f:
        f.write('[')
        for i, doc in enumerate(cur,1):
            f.write(json.dump(doc))
            if i != count:
                f.write(',')
        f.write(']')
    f.close()

def create_config(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev',DATABASE=os.path.join(app.instance_path,'pickup.json'))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    return app
