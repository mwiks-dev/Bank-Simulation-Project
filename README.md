# Bank Account Service Project

This project simulates a simple Bank Account Service, allowing users to interact with a bank account through a web interface. Users can check their balance, deposit money, and withdraw money within predefined limits. The backend is built with vanilla Python using the `http.server` module, while the frontend is developed with basic HTML and JavaScript. This document details the setup, functionality, and testing approach of the project.

## Backend

The backend server is a lightweight HTTP server written in Python. It provides REST API endpoints for three primary operations: viewing the account balance, depositing money, and withdrawing money. The server does not require authentication.

### Running the Server

1. Ensure Python 3 is installed on your system.
2. Save the server code in a file named `bank.py`.
3. Run the server using the command: `python3 bank.py`.
4. The server will start on `localhost` at port `8000`.

### Endpoints

- **GET /balance**: Fetches the current account balance.
- **POST /deposit**: Deposits a specified amount into the account. The request body should be JSON, e.g., `{"amount": 50000}`.
- **POST /withdraw**: Withdraws a specified amount from the account. Similar to deposit, the request body should contain the amount.

### Transaction Limits

- Maximum deposit per transaction: KES 40,000.
- Maximum deposit per day: KES 150,000.
- Maximum deposit transactions per day: 4.
- Maximum withdrawal per transaction: KES 20,000.
- Maximum withdrawal per day: KES 50,000.
- Maximum withdrawal transactions per day: 3.
- Withdrawals cannot exceed the current balance.

## Frontend

The frontend is a simple HTML page with JavaScript that interacts with the backend via AJAX requests. It provides a user-friendly interface for the account operations.

### Features

- **View Balance**: Users can see their current account balance.
- **Deposit Money**: Users can input an amount to deposit into their account.
- **Withdraw Money**: Users can input an amount to withdraw from their account.

### Running the Frontend

- Open the `bank.html` file in a web browser to access the frontend.
- Ensure the backend server is running as the frontend needs to communicate with it.

## Testing

### Backend Tests

The backend functionality is tested using Python's `unittest` framework. Tests are designed to verify that the API endpoints behave as expected under various conditions.

- **Test Setup**: Each test case starts with setting up a connection to the backend server.
- **Test Cases**: Include testing each endpoint for success responses and handling errors, such as exceeding transaction limits.
- **Running Tests**: Tests can be executed by running `python bank_tests.py` with the backend server running.

### Frontend Tests

Frontend testing is manual, involving interactions with the web interface to ensure that the frontend correctly displays balance information and handles deposit and withdrawal operations.

## Conclusion

This Bank Account Service project demonstrates a basic full-stack application with a Python backend and an HTML/JavaScript frontend. It showcases REST API design, handling HTTP requests in Python, and interacting with a backend server using AJAX in the frontend. The project includes basic transaction validation and unit tests for the backend, providing a foundation for more complex applications.