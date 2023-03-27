from sqlalchemy import insert
from expenses import app, db, Expense, User

with app.app_context():
    # Define the data to be inserted into the Expense table
    expenses = [
        {
            "userId": 1,
            "amount": 50.0,
            "description": "Concert ticket",
            "category": "Entertainment",
            "repaid": "Paid"
        },
        {
            "userId": 1,
            "amount": 20.0,
            "description": "Dinner",
            "category": "Food",
            "repaid": "Paid"
        },
        {
            "userId": 1,
            "amount": 200.0,
            "description": "Hotel",
            "category": "Travel",
            "repaid": "Unpaid"
        },
        {
            "userId": 2,
            "amount": 10.5,
            "description": "Coffee",
            "category": "Food",
            "repaid": "Paid"
        },
        {
            "userId": 2,
            "amount": 25.0,
            "description": "Movie ticket",
            "category": "Entertainment",
            "repaid": "Unpaid"
        },
        {
            "userId": 2,
            "amount": 100.0,
            "description": "Gas",
            "category": "Travel",
            "repaid": "Unpaid"
        }
    ]
    # Define the data to be inserted into the User table
    users = [
        {"email": "user1@example.com"},
        {"email": "user2@example.com"},
    ]
# Construct the SQL statements for inserting the data into the Expense and User tables
    expense_stmt = insert(Expense.__table__).values(expenses)
    user_stmt = insert(User.__table__).values(users)
# Execute the SQL statements using the session object
    db.session.execute(expense_stmt)
    db.session.execute(user_stmt)
# Commit the changes to the database
    db.session.commit()
