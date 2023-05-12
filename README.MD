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