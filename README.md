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

Example:

```bash
$ curl -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' https://gentle-cliffs-92685.herokuapp.com/products
```

### Fetching a particular product

@api {get} /products/product:ID

Example:

```bash
$ curl -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' https://gentle-cliffs-92685.herokuapp.com/products/foo
```

### Creating a new user

@api {post} /user

@apiParam {String, String} user and pwd

@apiOutput {String} AuthToken

Example:

```bash
$ curl -d '{"user":"test", "pwd":"test"}' https://gentle-cliffs-92685.herokuapp.com/user
```

### Adding a new product

@api {post} /products

@apiParam {String, String, String} id, seller and price

Example:

```bash
$ curl -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' -d '{"id":"bar", "seller":"foo", "price":"149"}' https://gentle-cliffs-92685.herokuapp.com/products
```

### Updating a product

@api {put} /products

@apiParam {String, String, String} id, seller and price

Example:

```bash
$ curl -X PUT -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' -d '{"id":"bar", "seller":"foo", "price":"249"}' https://gentle-cliffs-92685.herokuapp.com/products
```

### Deleting a product

@api {delete} /products/product:ID

Example:

```bash
$ curl -X DELETE -H 'Authorization: Basic cm9vdDpwd2Q=' -H 'user: root' https://gentle-cliffs-92685.herokuapp.com/products/foo
```