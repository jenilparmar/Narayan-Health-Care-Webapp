import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mydatabase"]
mycol = mydb["Patients"]
x = mycol.find()

# # Iterate over the cursor to access the documents
# for document in x:
#     print(document)
x=mycol.delete_many({})