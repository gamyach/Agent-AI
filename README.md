# Agent-AI


Overview

AI Query Agent is a Python-based system that efficiently retrieves client financial data from a dataset using an LRU (Least Recently Used) Cache for optimized performance. The agent allows querying of account balances, transactions, category-based reports, and average transaction values.

Features

LRU Caching: Improves efficiency by caching recently accessed data.

Client Account Balance Query: Retrieve a client's balance for a specific year.

Transaction Query: Fetch transactions for a specific client and year.

Category-Based Reports: Extract transactions related to a specific category.

Average Transaction Calculation: Compute the average transaction value by type.


Installation

1. Clone the repository:

git clone <repository_url>


2. Navigate to the project directory:

cd ai-query-agent


3. Ensure you have Python installed (Python 3 recommended).


4. Install required dependencies (if any):

pip install -r requirements.txt



Usage

Initializing the Agent

from ai_query_agent import AIQueryAgent

agent = AIQueryAgent('DataSet.txt', cache_size=4)

Query Examples

Retrieve Client Account Balance

Prompt: Get the balance of client '12345' for the year 2023.

result = agent.query_client_balance(client_id='12345', year=2023)
print(result)

Retrieve Transactions

Prompt: Fetch all transactions for client '12345' in 2023.

transactions = agent.query_transactions(client_id='12345', year=2023)
print(transactions)

Query Transactions by Category

Prompt: Get all grocery-related transactions.

category_data = agent.query_category_reports(category='Groceries')
print(category_data)

Calculate Average Transaction Values

Prompt: Calculate the average amount of each transaction type.

average_transactions = agent.query_average_transaction()
print(average_transactions)

Code Structure

LRUCache

A class implementing an OrderedDict-based LRU Cache:

get(key): Retrieves an item and moves it to the most recently used position.

put(key, value): Inserts an item; removes the least recently used item if the cache exceeds capacity.


AIQueryAgent

A class that loads data from a dataset and allows queries:

query_client_balance(client_id, year): Fetches account balance for a given client and year.

query_transactions(client_id, year): Retrieves transactions for a specific client and year.

query_category_reports(category): Returns transactions matching a given category.

query_average_transaction(): Computes the average transaction amount by type.


Dataset Format

The dataset should be a JSON file structured as follows:

{
  "clients": [
    {
      "client_id": "12345",
      "client_name": "John Doe",
      "2023": {
        "account_balance": 5000,
        "transactions": [
          {"description": "Groceries", "amount": 150},
          {"description": "Rent", "amount": 1200}
        ]
      }
    }
  ]
}

License

This project is licensed under the MIT License.

Contributing

Feel free to submit issues and pull requests for improvements.

Author

GAMYA CHANDA 

