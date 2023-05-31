## Installation

First, you have to create .enc file and define following variables:

SECRET_KEY=

Optional variables:
<br>DEBUG=

### Authorisation

mutation { tokenAuth(username:"tim",password:"12345"){ token } }

{
  "AUTHORIZATION": "JWT <token>"
}

query{
  me{
    id
    username
  }
}


## Frequent Queries

### Users
query{
users{
      id
    	username
  		email
    }
  }

### Categories
query{
categories{
      id
    	title
  }
}

### Goods

query{
goods{
      id
    	title
  description
  address
  url
  price
  category{
    id
    title
  }
  seller{
    id
    username
    email
  }
  }
}

## Frequent Mutations

### Users
mutation{
  createUser(username: "tim", email: "testemail@gmail.com", password: "12345"){
    user{
      id
    	username
  		email
    }
  }
}

### Categories
mutation{
  createCategory(title:"new category. test"){
		title
  }
}

mutation{
  updateCategory(id:1, title:"updated"){
    id
    title
  }
}

### Goods
mutation{
  createGood(
    title:"new category. test",
    description:"some uninterestin description",
    address:"nowhere 1, 12345",
    categoryId:1,
    price: 123.12
    
  ){
		title
  }
}

mutation {
  updateGood(
    goodId: 1
    title: "updated"
    description: "updated"
    address: "updated"
    price: 0
  ) {
    id
    title
    description
    address
    price
		seller{
      id
    }
    category{
      id
    }
  }
}

### Goods List

mutation{
  createGoodsList(
    title:"new goods list. test",
  ){
    id
		title
  }
}

### Orders
master




## Introspections
### Show all mutations

query IntrospectionQuery {
  __type(name: "Mutation") {
    name
    kind
    fields {
      name
      args {
        name
        type {
          name
          kind
        }
      }
      type {
        name
        kind
      }
    }
  }
}

## Test commands
### Execute a particular test
python manage.py test tests.api_tests.category_test
### Execute all tests
python manage.py test tests --pattern="*_test.py" 

### Generate test report
run with coverage:<br>
coverage run manage.py test tests.api_tests.category_test<br>
generate report: coverage report<br>
generate html: coverage html