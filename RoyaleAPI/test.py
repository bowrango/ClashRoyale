from client import Client

# key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkwMDJiMWE3LTRhMTItNDdhMy04MDU2LTU5YmFiZTZmZmVjZiIsImlhdCI6MTYwOTE5Njc3Mywic3ViIjoiZGV2ZWxvcGVyL2MyMGJhNThjLTlkNGUtMDFkZC01YzUwLTI5ZDMzZDZlMDNjNiIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIxMjguMTI4LjEyOC4xMjgiXSwidHlwZSI6ImNsaWVudCJ9XX0.1RKFtdown15NHs9gv32_25jsS2iS7uhrrM0Q2RjRTWNwVAYVwe9Q3FvscLn20DZU9ZhvJ_1vziLATz98JrzShg'
proxy_url = 'https://proxy.royaleapi.dev/v1'

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



