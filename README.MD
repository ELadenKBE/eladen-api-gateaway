## Installation

First, you have to create .enc file and define following variables:

SECRET_KEY=

Optional variables:
<br>DEBUG=


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