# Loan Calculator API

This is a Flask application that provides a RESTful API for loan calculation, listing, filtering, and exporting loan data.

## Setup

1. **Clone the Repository:**
    ```bash
    git clone 'https://github.com/sydriiick/Loan-Calculator-API.git'
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application:**
    ```bash
    python app.py
    ```

4. **Access the API:**
    The API will be accessible at `http://localhost:5000`.

## Usage

### 1. Calculate Loan

- **Endpoint:** `POST /loans`
- **Payload:** JSON containing borrower name, desired loan amount, and loan term.
    ```json
    {
        "borrower_name": "Syd Frisco",
        "desired_loan_amount": 10000,
        "loan_term": 12
    }
    ```
- **Response:** JSON containing loan details.
    ```json
    [
      {
        "borrower_name": "Syd Frisco",
        "desired_loan_amount": 10000.0,
        "loan_term": 12,
        "monthly_payment_amount": 945.6,
        "principal_loan_amount": 10000.0,
        "total_interest_amount": 1347.15,
        "total_sum_of_payments": 11347.15
      }
    ]
    ```

### 2. List, Filter, and Sort Loans

- **Endpoint:** `GET /loans`
- **Query Parameters:**
  - `borrower_last_name`: Filter loans by name.
  - `desired_loan_amount`: Filter loans by amount.
  - `loan_term`: Filter loans by term.
  - `sort_by`: Sort loans by `name`, `amount`, or `term` (default: `name`).
  - `order_by`: Sorting order (`asc` for ascending, `desc` for descending) (default: `asc`).

- **Example Request:**
    ```
    GET /loans?name=Frisco&amount=10000&sort_by=term&order_by=desc
    ```

- **Response:** JSON containing a list of filtered and sorted loans.

### 3. Export Loans

- **Endpoint:** `GET /loans/export`
- **Response:** CSV file containing all loan data.

## Example

1. **Calculate Loan:**
    ```
    POST http://localhost:5000/loans
    ```
    Payload:
    ```json
    {
        "borrower_name": "Syd Frisco",
        "desired_loan_amount": 5000,
        "loan_term": 12
    }
    ```

2. **List, Filter, and Sort Loans:**
    ```
    GET http://localhost:5000/loans?name=Frisco&amount=1000&sort_by=term&order_by=desc
    ```

3. **Export Loans:**
    ```
    GET http://localhost:5000/loans/export
    ```

## Tips

- Ensure the API server is running (`python app.py`) before making requests.
- Use tools like cURL, Postman, or web browsers to interact with the API.
- Adjust sorting and filtering parameters as needed to retrieve specific loan data
