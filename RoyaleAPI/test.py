from client import Client

proxy_url = 'https://proxy.royaleapi.dev/v1'

# save your own key to a key.txt file into the RoyaleAPI directory
with open('RoyaleAPI/key.txt', 'r') as file:
    dev_key = file.read().replace('\n', '')

## some demo code to get infomation about the top players and card stats
c = Client(token=dev_key, url=proxy_url)
players = c.get_top_players(limit=10)

stats = c.get_all_card_attrs(attribute='cards_stats')
attrs = c.get_all_card_attrs(attribute='cards')
print(attrs)

# for player in players.raw_data:
#     tag = player.raw_data['tag']
#     player_info = c.get_player(tag)
#     current_deck = player_info.raw_data['currentDeck']
#     current_deck = [dict_idx['name'] for dict_idx in current_deck]
#     print(current_deck)



