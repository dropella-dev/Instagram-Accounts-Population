from pymongo import MongoClient

def db_connection():
    mongo_uri = "mongodb://mongo:jSHKXAPwCpYjYnZarCZnJcWkxKxNIZDR@roundhouse.proxy.rlwy.net:46767"
    try:
        client = MongoClient(mongo_uri)
        db = client['test']  
        collection = db['instagram_acounts']
        if collection is not None:
            print(f"Connection initiated with database")
            return collection
        elif collection is None:
            return False
    except Exception as e:
        print(f"Failed to initiate database connection , detail : {e}")
        return False

def insert_record(connection,record):
    try:
        result = connection.insert_one(record)
        if result is not None:
            print(f"Record inserted for {record['user_name']} : {result}")
            return result
        elif result is None:
            return False
    except Exception as e:
        print(f"Failed to insert record for {record['user_name']} , detail : {e}")
        return False

def get_used_proxies(connection):
    try:
        users_info = connection.find({})
        used_proxies = [info['proxy'] for info in users_info]
        if used_proxies:
            return used_proxies
        elif not used_proxies:
            print("Failed to fetch used proxies")
            return False
    except Exception as e:
        print(f"Failed to fetch used proxies, detail : {e}")
        return False
def get_users_data(connection):
    try:
        users_info = connection.find({})
        users_info = [info for info in users_info]
        if users_info:
            return users_info
        elif not users_info:
            print("Failed to fetch users data")
            return False
    except Exception as e:
        print(f"Failed to fetch users data, detail : {e}")
        return False
