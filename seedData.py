from sqlalchemy import insert
from expenses import app, db, Expense, User

with app.app_context():
    expenses = [
        {
            "userId": 1,
            "amount": 50.0,
            "description": "Concert ticket",
            "category": "Entertainment"
        },
        {
            "userId": 1,
            "amount": 20.0,
            "description": "Dinner",
            "category": "Food"
        },
        {
            "userId": 1,
            "amount": 200.0,
            "description": "Hotel",
            "category": "Travel"
        },
        {
            "userId": 2,
            "amount": 10.5,
            "description": "Coffee",
            "category": "Food"
        },
        {
            "userId": 2,
            "amount": 25.0,
            "description": "Movie ticket",
            "category": "Entertainment"
        },
        {
            "userId": 2,
            "amount": 100.0,
            "description": "Gas",
            "category": "Travel"
        }
    ]
    users = [
        {"email": "user1@example.com"},
        {"email": "user2@example.com"},
    ]

    expense_stmt = insert(Expense.__table__).values(expenses)
    user_stmt = insert(User.__table__).values(users)

    db.session.execute(expense_stmt)
    db.session.execute(user_stmt)

    db.session.commit()
