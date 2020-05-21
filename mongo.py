import pymongo


def connect_to_mongo():
    uri = 'mongodb://127.0.0.1:27017/'
    return pymongo.MongoClient(uri)['vimpel38']


def clean_mondo_coll(coll):
    coll.drop()
