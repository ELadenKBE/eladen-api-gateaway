## Installation

First, you have to create .enc file and define following variables:

SECRET_KEY=<br />
DEBUG=<br />
PRODUCT_SERVICE_URL=<br />
ORDER_SERVICE_URL=<br />
USER_SERVICE_URL=<br />

### Authorisation

{
  "AUTHORIZATION": "sub <token>"
}


## Frequent Queries

### Users

query{
  users{
            id
            username
            email
    		role
    		address
    		firstName
    		lastName
      }
}

query{
  users(search: "tim_user"){
            id
            username
            email
    		role
    		address
    		firstName
    		lastName
      }
}

query{
  users(searchedId: 1){
            id
            username
            email
    		role
    		address
    		firstName
    		lastName
      }
}

### Categories
query{
categories{
      id
    	title
  }
}

{
  categories(searchedId: "1") {
    id
    title
  }
}

{
  categories(search: "updated") {
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

{
  goods(searchedId: 1) {
    id
    title
  }
}

### Goods List

query{
  goodsLists{
    id
    title
    user {
      id
    }
    goods{
      id
    }
  }
}
#### Get all items of a cart

query{
  goodsLists(search:"cart"){
    id
    title
    goods{
      id
      title
    }
  }
}

### Orders 
query{
  orders{
    id
    timeOfOrder
    deliveryAddress
    itemsPrice
    deliveryPrice
    deliveryStatus
    paymentStatus
    userId
    goods{
      id
      title
    }
  }
}

query{
  orders(searchedId:1){
    id
    timeOfOrder
    deliveryAddress
    itemsPrice
    deliveryPrice
    deliveryStatus
    paymentStatus
    userId
  }
}

## Frequent Mutations

### Users

mutation {
  createUser(
    username: "tim_user_test_3"
    email: "testemail@gmail.com"
    role: 1,
    sub:"asdasdad"
  ) {
    id
    username
    email
  }
}

mutation{
  updateUser(userId:1,
  	email:"updated@gmail.com",
  	address:"updated",
  	firstname:"updated",
  	lastname:"updated"){
        id
        username
        email
    		role
    		address
    		firstname
    		lastname
      }
}

mutation{
  deleteUser(userId:1){
    id
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
mutation {
  createGood(
    title: "new good. test. newnwenwe"
    description: "some uninterestin description"
    address: "nowhere 1, 12345"
    categoryId: 1
    price: 123.12
    manufacturer: "asd"
    url: "www.ware.com/test"
  ) {
    id
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

mutation{
  changeCategory(goodId:1, categoryId:1){
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

mutation{
  deleteGood(id:1){
  id
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

mutation{
  cleanGoodsList(listId:1){
    id
    title
    goods{
      id
    }
  }
}

mutation{
  updateGoodsList(listId:1, title:"newwww"){
    title
  }
}

mutation {
  deleteGoodsList(listId:1){
    id
  }
}

mutation{
  cleanGoodsList(listId:2){
    id
    title
  }
}
### Orders

mutation {
  createOrder(
    timeOfOrder: "1999-05-23 11:12"
    deliveryAddress: "test_11"
  ) {
    id
    timeOfOrder
    deliveryAddress
    itemsPrice
    deliveryPrice
    userId
  }
}

mutation {
  updateOrder(orderId:2, deliveryAddress : "updated_18.07") {
    id
    timeOfOrder
    deliveryAddress
    itemsPrice
    deliveryPrice
    userId
  }
}

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