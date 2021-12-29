import pymongo


client = pymongo.MongoClient("mongodb+srv://chinppk05:25021996@wmatest.plvbd.mongodb.net/wma_test?retryWrites=true&w=majority")

for database_name in client.list_database_names():  
    print("Database - "+database_name)  
    for collection_name in client.get_database(database_name).list_collection_names():  
        print(collection_name) 
"""
col = db["wma11"]
col.insert_one({"data1":"1","data2":"2","data3":"3"})
"""