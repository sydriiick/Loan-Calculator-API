from flask import Flask, request, jsonify, Response
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv
from io import StringIO

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///loans.db', echo=True)
Base = declarative_base()

class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    borrower_name = Column(String)
    desired_loan_amount = Column(Float)
    loan_term = Column(Integer)
    principal_loan_amount = Column(Float)
    monthly_payment_amount = Column(Float)
    total_interest_amount = Column(Float)
    total_sum_of_payments = Column(Float)

Base.metadata.create_all(engine)

# Helper function to convert query results to dictionary
def loan_to_dict(loan):
    print(loan)
    return {
        "borrower_name": loan.borrower_name,
        "desired_loan_amount": loan.desired_loan_amount,
        "loan_term": loan.loan_term,
        "principal_loan_amount": loan.principal_loan_amount,
        "monthly_payment_amount": loan.monthly_payment_amount,
        "total_interest_amount": loan.total_interest_amount,
        "total_sum_of_payments": loan.total_sum_of_payments
    }

# Endpoint for loan calculation
@app.route('/loans', methods=["POST"])
def calculate_loan():
    data = request.get_json()
    borrower_name = data.get('borrower_name')
    desired_loan_amount = data.get('desired_loan_amount')
    loan_term = data.get('loan_term')

    # Loan calculations
    principal_loan_amount = desired_loan_amount
    monthly_payment_amount = (desired_loan_amount * 0.02) / (1 - (1 + 0.02) ** -loan_term)
    total_interest_amount = (monthly_payment_amount * loan_term) - desired_loan_amount
    total_sum_of_payments = principal_loan_amount + total_interest_amount

    # Save data to database
    Session = sessionmaker(bind=engine)
    session = Session()
    loan = Loan(borrower_name=borrower_name, desired_loan_amount=round(desired_loan_amount, 2),
                loan_term=loan_term, principal_loan_amount=round(principal_loan_amount, 2),
                monthly_payment_amount=round(monthly_payment_amount, 2),
                total_interest_amount=round(total_interest_amount, 2),
                total_sum_of_payments=round(total_sum_of_payments, 2))
    session.add(loan)
    session.commit()

    # Prepare response
    response = loan_to_dict(loan)
    
    session.close()
    return jsonify(response)

# Endpoint for listing and filtering loans
@app.route('/loans', methods=['GET'])
def list_and_filter_loans():
    borrower_last_name = request.args.get('name')
    desired_loan_amount = request.args.get('amount')
    loan_term = request.args.get('term')
    sort_by = request.args.get('sort_by', 'name')
    order_by = request.args.get('order_by', 'asc')

    Session = sessionmaker(bind=engine)
    session = Session()

    # Filtering loans based on provided parameters
    query = session.query(Loan)
    if borrower_last_name:
        query = query.filter(Loan.borrower_name.ilike(f'%{borrower_last_name}%'))
    if desired_loan_amount:
        query = query.filter(Loan.desired_loan_amount == float(desired_loan_amount))
    if loan_term:
        query = query.filter(Loan.loan_term == int(loan_term))

    # Sorting loans
    if sort_by == 'amount':
        sort_field = Loan.desired_loan_amount
    elif sort_by == 'term':
        sort_field = Loan.loan_term
    else:
        sort_field = Loan.borrower_name

    if order_by == 'desc':
        query = query.order_by(sort_field.desc())
    else:
        query = query.order_by(sort_field.asc())

    loans = query.all()
    session.close()

    # Execute query and convert results to dictionary
    loans = [loan_to_dict(loan) for loan in query.all()]
    session.close()

    return jsonify(loans)

# Endpoint for exporting loans as CSV
@app.route('/loans/export', methods=['GET'])
def export_loans():
    Session = sessionmaker(bind=engine)
    session = Session()

    loans = session.query(Loan).all()
    session.close()

    # Prepare CSV data
    csv_data = StringIO()
    csv_writer = csv.DictWriter(csv_data, fieldnames=["Borrower Name", "Desired Loan Amount", "Loan Term",
                                                      "Principal Loan Amount", "Monthly Payment Amount",
                                                      "Total Interest Amount", "Total Sum of Payments"])
    csv_writer.writeheader()
    for loan in loans:
        csv_writer.writerow({
            "Borrower Name": loan.borrower_name,
            "Desired Loan Amount": loan.desired_loan_amount,
            "Loan Term": loan.loan_term,
            "Principal Loan Amount": loan.principal_loan_amount,
            "Monthly Payment Amount": loan.monthly_payment_amount,
            "Total Interest Amount": loan.total_interest_amount,
            "Total Sum of Payments": loan.total_sum_of_payments
        })

    # Return CSV file as response
    return Response(csv_data.getvalue(), mimetype='text/csv', headers={
        "Content-disposition": "attachment; filename=loans.csv"
    })


if __name__ == '__main__':
    app.run(debug=True)