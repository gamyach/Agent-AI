import json
import re
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            removed = self.cache.popitem(last=False)  # Remove least recently used
            print(f"[Cache Evicted] {removed[0]}")  # Log evicted key
        self.cache[key] = value

class AIQueryAgent:
    def __init__(self, dataset_path, cache_size=5):
        self.data = self.load_data(dataset_path)
        self.cache = LRUCache(cache_size)
    
    def load_data(self, path):
        with open(path, 'r') as file:
            return json.load(file)
    
    def query_client_balance(self, client_id, year):
        cache_key = f"balance_{client_id}_{year}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return f"[Cache Hit] {cached_result}"
        
        for client in self.data['clients']:
            if client['client_id'] == client_id:
                if str(year) in client:
                    balance = client[str(year)]['account_balance']
                    self.cache.put(cache_key, balance)
                    return f"Account Balance for {client['client_name']} in {year}: ${balance}"
        return "Client or year not found."
    
    def query_transactions(self, client_id, year):
        cache_key = f"transactions_{client_id}_{year}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return f"[Cache Hit] {cached_result}"
        
        for client in self.data['clients']:
            if client['client_id'] == client_id:
                if str(year) in client:
                    transactions = client[str(year)]['transactions']
                    self.cache.put(cache_key, transactions)
                    return transactions
        return "Client or year not found."
    
    def query_category_reports(self, category):
        cache_key = f"category_{category}"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return f"[Cache Hit] {cached_result}"
        
        category_data = []
        for client in self.data['clients']:
            for year, details in client.items():
                if isinstance(details, dict) and 'transactions' in details:
                    filtered_transactions = [t for t in details['transactions'] if category.lower() in t['description'].lower()]
                    if filtered_transactions:
                        category_data.extend(filtered_transactions)
        
        self.cache.put(cache_key, category_data)
        return category_data if category_data else f"No transactions found for {category}."
    
    def query_average_transaction(self):
        cache_key = "average_transaction"
        cached_result = self.cache.get(cache_key)
        if cached_result:
            return f"[Cache Hit] {cached_result}"
        
        transaction_types = {}
        for client in self.data['clients']:
            for year, details in client.items():
                if isinstance(details, dict) and 'transactions' in details:
                    for t in details['transactions']:
                        transaction_types.setdefault(t['description'], []).append(t['amount'])
        
        avg_transactions = {t: sum(v) / len(v) for t, v in transaction_types.items()}
        self.cache.put(cache_key, avg_transactions)
        return avg_transactions

    def handle_prompt(self, prompt):
        prompt = prompt.lower()
        
        balance_match = re.search(r"balance.*client\s*(\w+).*year\s*(\d{4})", prompt)
        if balance_match:
            client_id, year = balance_match.groups()
            return self.query_client_balance(client_id, year)
        
        transaction_match = re.search(r"transactions.*client\s*(\w+).*year\s*(\d{4})", prompt)
        if transaction_match:
            client_id, year = transaction_match.groups()
            return self.query_transactions(client_id, year)
        
        category_match = re.search(r"(?:client reports for|show all transactions related to)\s*(.+)", prompt)
        if category_match:
            category = category_match.group(1)
            return self.query_category_reports(category)
        
        avg_match = re.search(r"(average transaction|mean transaction amount|typical transaction value)", prompt)
        if avg_match:
            return self.query_average_transaction()
        
        return "Sorry, I didn't understand the query. Please rephrase."
    
agent = AIQueryAgent('DataSet.txt', cache_size=3)
while True:
    user_prompt = input("Ask me a question: ")
    if user_prompt.lower() == "exit":
        break
    response = agent.handle_prompt(user_prompt)
    print(response)
