from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient

# termonology
# collection is the equivalent of a table in a normal database or similar to a folder
# docs are similar to rows in a table. 


load_dotenv()

password = os.getenv("MONGODB_PWD")

#creating connection to MongoDB
connection_string = f"mongodb+srv://alitv1998you:{password}@database.lejcqby.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

dbs =client.list_database_names()
test_db = client.test
collections = test_db.list_collection_names()


#__________Inserting document___________#
def insert_test_doc():
    collection = test_db.test

    test_document = {
        "name": "Tim",
        "type": "Test"
    }
    inserted_id = collection.insert_one(test_document).inserted_id

    print(inserted_id)

#if db does not exist mongodb will create that database only if u also insert a document
production = client.production
person_collection = production.person_collection

def create_documents():
    names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
    last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Garcia']
    ages = [25, 32, 41, 19, 28, 37]

    docs = []
    for names, last_names, ages in zip(names, last_names, ages):
        doc = {"names": names, "last_names": last_names, "ages": ages}
        docs.append(doc)
    person_collection.insert_many(docs)
    print(docs)

# create_documents()

printer = pprint.PrettyPrinter()

#__________Reading documents___________#
def find_all_people():
    people = person_collection.find()
    for person in people:
        printer.pprint(person)

# find_all_people()

def find_tim():
    tim = person_collection.find_one({"names":"David"})
    printer.pprint(tim)

def count_all_people():
    count = person_collection.count_documents(filter={})
    print(f"number of people inside the collection {count}")

def get_person_by_id(person_id):
    from bson.objectid import ObjectId

    #to search person by id you need to convert the id to a object
    _id = ObjectId(person_id)
    print(_id)
    person = person_collection.find_one({"_id": _id})
    printer.pprint(person)

# get_person_by_id("645b934d43a4310aa9295254")

def get_age_range(min_age, max_age):
    #advanced query between to numbers
    query = {"$and": [
            {"ages": {"$gte": min_age}},
            {"ages": {"$lte": max_age}}
        ]}

    people = person_collection.find(query)

    for person in people:
        printer.pprint(person)

# get_age_range(10, 30)

def project_columns():
    #select what columns you want to read
    # 0 no read, 1 yes read
    columns = {"_id": 0, "names": 1, "ages": 1}
    people = person_collection.find({}, columns)

    for person in people:
        printer.pprint(person)
# project_columns()


#__________Update___________#
def update_person_by_id(person_id):
    from bson.objectid import ObjectId

    #to search person by id you need to convert the id to a object
    _id = ObjectId(person_id)
    
    all_updates = {
        "$set": {"new_field": True}, #creates a new column
        "$inc": {"age": 1}, #icrements age by one
        "$rename": {"names": "first", "last_names": "last"} #changes name on column/field
    }
    # person_collection.update_one({"_id": _id}, all_updates)

    #removing field/column
    person_collection.update_one({"_id": _id}, {"$unset": {"new_field": ""}})

# update_person_by_id("645b934d43a4310aa9295254")

def replace_one(person_id):
    #replacing information within the same id 
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)
    
    all_updates = {
        "first name": "fehmmi",
        "last name": "aliti",
        "age": 25
    }

    person_collection.replace_one({"_id":_id}, all_updates)

# replace_one("645b934d43a4310aa9295250")

#__________Delete___________#
def delete_one(person_id):
    #deleting a doc in the collection

    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    person_collection.delete_one({"_id":_id})

# delete_one("645b934d43a4310aa9295250")

#__________Relationships___________#

addresses = {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "CA",
    "zip": "12345"
}

def add_address_embed(person_id, address):
    #adding address to a person within the same doc
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    person_collection.update_one({"_id":_id}, {"$addToSet": {"address": address}})
    
# add_address_embed("645b934d43a4310aa9295251", addresses)

def add_address_relationships(person_id, address):
    from bson.objectid import ObjectId
    _id = ObjectId(person_id)

    address = address.copy()

    address['owner_id'] = person_id


    address_collection = production.address
    address_collection.insert_one(address)

add_address_relationships("645b934d43a4310aa9295253", addresses)