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
Documentation for mongoimport can be found [here] (http://docs.mongodb.org/manual/reference/program/mongoimport/)

The command used in this video:
```
    mongoimport -db dbname -c collectionname --file input-file.json
```
If no hostname and credentials are supplied, mongoimport will try to connect to the default localhost:27017

--------------------------------------
### Operators
Start with $, e.g. $gt, $lt, $lte, $ne
    query = {"population" : {"$gt" : 250000, "$lte" : 500000}"}
    query = {"name" : {"$gt" : "X", "$lte" : "Y"}"}
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

--------------------------------------