# Sova Store Backend

This is backend for API service "Sova Store"

## Features

- JWT authenticated
- Admin panel /admin/
- Managing orders
- Creating products
- Creating tags (Form and Topic)

## Components

- Store Service :
  - Managing products
  - API:
    - POST:```product/``` - add new product
    - GET:```product/```  - get a list of products
    - GET:```product/<id>/``` - get product's detail info 
    - PUT/PATCH:```product/<id>/``` - update product
    - DELETE:```product/<id>/``` - delete product
    - POST:```tags/``` - add new tag
    - GET:```tags/```  - get a list of tags
    - GET:```tags/<id>/``` - get tag's detail info 
    - PUT/PATCH:```tags/<id>/``` - update tag
    - DELETE:```tags/<id>/``` - delete tag
  
- Users Service:
  - Managing authentication & user registration
  - API:
     - POST:```register/``` - register a new user 
     - POST:```login/``` - get JWT tokens 
     - POST:```token-renew/``` - refresh JWT token 
     - GET:```me/``` - get my profile info 
     - PUT/PATCH:```me/``` - update profile info 

- Order Service:
  - Managing users' orders
  - API:
    - POST:```order/``` - add new order
    - GET:```order/<id>/``` - get specific order
    - PUT/PATCH: ```order/<id>/``` - update a status of specific order

## Installing using GitHub

1. Clone the repository
 ```shell
  git clone https://github.com/SovaHandmade/Sova-Backend.git
  cd Sova-Backend
```

2. Create a virtual environment and activate it
```shell
  python -m venv venv
  source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. Create .env file with all necessities using .env.sample

4. Install requirements
```shell
  pip install -r requirements.txt
```

5. Apply migrations
```shell
  python manage.py migrate
```

6. Create superuser
```shell
  python manage.py createsuperuser
```

7. Run server
```shell
  python manage.py runserver
```

You also can register new non-admin user using ```user/register/```

You also need to obtain token in ```user/login/``` page

# Used technologies
- Python
- Django ORM
- Django REST Framework
- HTML
