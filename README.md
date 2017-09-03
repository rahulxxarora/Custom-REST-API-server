Custom REST-API Server
======================


Setting up the environment
--------------------------

```bash
sudo pip install -r requirements.txt
```

Running tests
-------------

```bash
python tests.py
```

Running the application
-----------------------

```bash
python app.py
```

API Docs
--------

### Fetching all products

@api {get} /products

@apiOutput 
		   {200} JSON Data

		   {404} Item not found, Invalid endpoint

Example:

```bash
$ curl -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' https://gentle-cliffs-92685.herokuapp.com/products
```

### Fetching a particular product

@api {get} /products/product:ID

@apiOutput 
		   {200} JSON Data

		   {404} Item not found, Invalid endpoint

Example:

```bash
$ curl -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' https://gentle-cliffs-92685.herokuapp.com/products/foo
```

### Creating a new user

@api {post} /user

@apiParam {String, String} user and pwd

@apiOutput 
		   {201} AuthToken

		   {400} Invalid JSON data

		   {404} Invalid endpoint

Example:

```bash
$ curl -d '{"user":"test", "pwd":"test"}' https://gentle-cliffs-92685.herokuapp.com/user
```

### Adding a new product

@api {post} /products

@apiParam {String, String, String} id, seller and price

@apiOutput 
		   {201} Item stored in the database

		   {400} Invalid JSON data

		   {404} Invalid endpoint

Example:

```bash
$ curl -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' -d '{"id":"bar", "seller":"foo", "price":"149"}' https://gentle-cliffs-92685.herokuapp.com/products
```

### Updating a product

@api {put} /products

@apiParam {String, String, String} id, seller and price

@apiOutput 
		   {200} Item updated in the database

		   {400} Invalid JSON data

		   {404} Invalid endpoint

Example:

```bash
$ curl -X PUT -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' -d '{"id":"bar", "seller":"foo", "price":"249"}' https://gentle-cliffs-92685.herokuapp.com/products
```

### Deleting a product

@api {delete} /products/product:ID

@apiOutput 
		   {200} Item deleted successfully

		   {404} Item not found, Invalid endpoint

Example:

```bash
$ curl -X DELETE -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' https://gentle-cliffs-92685.herokuapp.com/products/foo
```