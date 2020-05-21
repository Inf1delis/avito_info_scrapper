import pymongo


def connect_to_mongo():
    MONGO_INITDB_ROOT_USERNAME = "user"
    MONGO_INITDB_ROOT_PASSWORD = "user"
    host = "127.0.0.1"
    ports = "27017"
    # uri = "mongodb://{:s}:{:s}@{:s}:{:s}".format(MONGO_INITDB_ROOT_USERNAME, \
    #                                              MONGO_INITDB_ROOT_PASSWORD, host, ports)
    uri = 'mongodb://127.0.0.1:27017/'
    return pymongo.MongoClient(uri)['vimpel38']


def clean_mondo_coll(coll):
    coll.drop()
