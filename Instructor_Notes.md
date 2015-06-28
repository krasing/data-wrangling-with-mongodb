MongoDB http://www.mongodb.com/ is a NoSQL database http://en.wikipedia.org/wiki/NoSQL.

See this official site for JSON data format http://www.json.org/.

Python dictionaries documentation http://www.json.org/.

PHP Arrays documentation http://php.net/manual/en/language.types.array.php.

Ruby Hashes documentation http://www.tutorialspoint.com/ruby/ruby_hashes.htm.

----------------------------------
You can download MongoDB for your platform from the official MongoDB page http://www.mongodb.org/downloads. You can also read specific MongoDB installation instructions http://docs.mongodb.org/manual/installation/.

You do not need to install MongoDB on your machine for most of the exercises in this course, however for best learning outcome we recommend that you do it. It's fast and easy!

MongoDB has a lot of drivers and client libraries http://docs.mongodb.org/manual/applications/drivers/. The one we will be using in this course is PyMongo http://api.mongodb.org/python/current/installation.html. See the official documentation for PyMongo installation instructions.

-----------------------------------
You need to install pymongo to run this code locally:

pip install pymongo
See how to do MongoDB Installation in our wiki https://www.udacity.com/wiki/ud032#installing-mongodb.

Install mongodb
http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

---------------------------------------
See this site for PyMongo installation information.

The preferred way of installing pymongo on platforms other than Windows is using pip:

pip install pymongo
To be able to use PyMongo, you need a running MongDB instance to connect to. For information on how to install MongoDB on your local machine, please see Course Materials.

---------------------------------------


### Importing documents

#### Directly from the system

Documentation for mongoimport can be found [here] (http://docs.mongodb.org/manual/reference/program/mongoimport/)

```
    $mongoimport -db dbname -c collectionname --file input-file.json
```
If no hostname and credentials are supplied, mongoimport will try to connect to the default localhost:27017

#### Using PyMongo

Getting dictionary from json:

    db = client.examples
    with open('arachnid.json') as f:
        data = json.loads(f.read())

Getting dictionary from csv: see [autos.py](./autos.py)

data - list of dictionaries

arachnid - collection
        
    for a in data:
        db.arachnid.insert(a)

--------------------------------------
### Operators
Start with $, e.g. $gt, $lt, $lte, $ne

    query = {"population" : {"$gt" : 250000, "$lte" : 500000}}
    query = {"name" : {"$gt" : "X", "$lte" : "Y"}}
    query = {"foundingDate" : {"gt" : datetime(1837, 1, 1)}}
    cities = db.cities.find(query)
    
[MongoDB Query Operators Reference](http://docs.mongodb.org/manual/reference/operator/query)

--------------------------------------
### Using shell commands
To start mongo shell locally: Type following command in your terminal:

    mongo
    
    > use examples
    > db.cities.find()
    > db.cities.find( {"governmentType" : {"$exists" : 1}} ).count()
    > db.cities.find( {"governmentType" : {"$exists" : 1}} ).pretty()
    > db.collection_names()


--------------------------------------

### Regular expressions - Perl compatible (PCRE)
    query = {"moto" : {"$regex" : "[Ff]riendship|[Hh]appiness"}}
    
### Structured data
    db.autos.find({"modelYear" : {"$in" : [1965, 1966, 1967]}}).count()
    db.autos.find({"modelYear" : {"$all" : [1965, 1966, 1967]}}).count()
    db.autos.find({"dimensions.weight" : {"$gt" : 50000}})
    
---------------------------------------

### Example code

    def get_db():
        from pymongo import MongoClient
        client = MongoClient('localhost:27017')
        db = client.examples
        return db
        
    def in_query():
        query = {"manufacturer" : "Ford Motor Company", "assembly" : {"$in" : ["Germany", "United Kingdom", "Japan"]}}
        return query


    if __name__ == "__main__":

        db = get_db()
        query = in_query()
        autos = db.autos.find(query, {"name":1, "manufacturer":1, "assembly": 1, "_id":0})

        print "Found autos:", autos.count()
        import pprint
        for a in autos:
            pprint.pprint(a)

### Add projection (specification how to display the results)

    query = {"entities.hashtags" : {"$ne" : []}}
    projection =  {"entities.hashtags.text" : 1, "_id" : 0}
    result = db.tweets.find(query, projection)
    
param1: query document
param2: projection documents

### Updating (modifing existing documents) collectionname

Using save command (in pymongo - method on collection object)

Replace the document with the same _id. If no such document is available or the new document does not have _id field, a new record is added.

    city = db.cities.find_one({"name" : "Munchen", "country" : "Germany"})
    city["isoCountryCode"] = "DEU"
    db.cities.save(city)
    
Using `update` command with $set operator

    city = db.cities.update({"name" : "Munchen", "country" : "Germany"},
                             {"$set" : {"isoCountryCode" : "DEU"} })

To update multiple documents:

    city = db.cities.update({"name" : "Munchen", "country" : "Germany"},
                             {"$set" : {"isoCountryCode" : "DEU"} }, 
                             multi = True)
                             
param1: query document; param2: update documents

to remove field: `{"$unset" : {"isoCountryCode" : ""}`

If "$set" operator is not used the whole document will be replaced, not just the field:

    city = db.cities.update({"name" : "Munchen", "country" : "Germany"},
                             {"isoCountryCode" : "DEU" })
                             
Will lead to single field document.

### Remove documents
Remove documents satisfying some criteria:

    db.cities.remove(querydocument)
    
Remove an entire collection:

    db.cities.drop()

### MongDB console vs Python script:

Python script: `db.cities.find_one()`

MongDB console: `db.cities.findOne()`