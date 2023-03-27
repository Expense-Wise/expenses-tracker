from expenses import User, db, Expense, app

def allexpense(user_id):
    user = User.query.filter_by(id=user_id).first()
    totalexpense = 0
    for expense in user.expenses:
        totalexpense += expense.amount
        return totalexpense