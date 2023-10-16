# Django Rest Framework and ReactJS (NextJS) Frame

## Prerequisites
### Install
```
Python 3.11.4
NodeJS 18.15.0
```

## For Backend (http://localhost:8000/)
### Create Python Env
```
cd backend
python3 -m venv env
source env/bin/activate
```

### Install necessary lib or dep
```
pip install -r requirements.txt
```

### DB Migrate
Note: Current DB is SQLite (if want to change, follow this https://docs.djangoproject.com/en/4.2/ref/settings/#databases)
```
python manage.py migrate
```

### Run Test
```
python manage.py test
```

### Run API
```
python manage.py runserver
```

### API Detail To Buy Food Item
```
Create a new order for a specific food item from the ice cream truck.

URL:
    http://localhost:8000/api/order/

Args:
    food_item: Food Item ID
    quantity: quantity 
    truck: Truck ID

Returns:
    "ENJOY!": if buy in stock amount of food
    "SORRY!": if buy out of stock amount of food
```

### API Detail To Get Truck Details
```
Get details of a specific ice cream truck, including its food items and total earnings.

URL:
    http://localhost:8000/api/truck/<pk>

Args:
    pk (int): The primary key of the truck to retrieve details.
    
Returns:
    A JSON response with the truck's details.
```

## For Frontend (http://localhost:3000/)
### NPM Install
```
cd frontend
npm install
```

### Run App
```
npm run dev
```