const apiUrl = 'http://localhost:8000'; 

// Fetch balance immediately the page loads
document.addEventListener('DOMContentLoaded', function() {
    getBalance(); 
});

//fetch balance on the specified endpoint
function getBalance() {
    fetch(`${apiUrl}/balance`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('balance').textContent = data.balance;
        })
        .catch(error => console.error('Error fetching balance:', error));
}

// deposit funds on the specified endpoint
function deposit() {
    const amount = document.getElementById('depositAmount').value;
    if (amount) {
        fetch(`${apiUrl}/deposit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount: parseFloat(amount) }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                alert(data.message || 'Deposit successful');
                getBalance(); // Refreshes balance
            }
        })
        .catch(error => console.error('Error making deposit:', error));
    } else {
        alert("Please enter an amount to deposit.");
    }
}

// allow withdrawals on the specified endpoint
function withdraw() {
    const amount = document.getElementById('withdrawAmount').value;
    if (amount) {
        fetch(`${apiUrl}/withdraw`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount: parseFloat(amount) }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                alert(data.message || 'Withdrawal successful');
                getBalance(); // Refreshes the balance
            }
        })
        .catch(error => console.error('Error making withdrawal:', error));
    } else {
        alert("Please enter an amount to withdraw.");
    }
}
