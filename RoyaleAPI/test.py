from client import Client

# save your own key to a key.txt file into the RoyaleAPI directory
with open('RoyaleAPI/key.txt', 'r') as file:
    dev_key = file.read().replace('\n', '')

proxy_url = 'https://proxy.royaleapi.dev/v1'

## get the decks used by the top 3 players in the world
client = Client(token=dev_key, url=proxy_url)
top_decks = client.get_top_decks(limit=3)
print(top_decks)


# stats = client.get_all_card_attrs(attribute='cards_stats')
# attrs = client.get_all_card_attrs(attribute='cards')

# knight_stats = stats['troop'][0]
# knight_atrrs = attrs[0]







