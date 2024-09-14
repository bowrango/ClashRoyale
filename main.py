import requests
import networkx as nx

with open('RoyaleAPI/key.txt', 'r') as file:
    API_KEY = file.read().replace('\n', '')
BASE_URL = 'https://api.clashroyale.com/v1'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json'
}

def get_all_cards():

    url = f'{BASE_URL}/cards'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()['items']
    else:
        print(f"Error fetching cards: {response.status_code}")
        return None

def main():

    G = nx.Graph()

    cards = get_all_cards()
    for card in cards:
            print(card)
            G.add_node(card['name'], cost=card['elixirCost'])


if __name__ == "__main__":
    main()