from RoyaleAPI import Client

# save your own key to a key.txt file into the RoyaleAPI directory
with open('RoyaleAPI/key.txt', 'r') as file:
    dev_key = file.read().replace('\n', '')
proxy_url = 'https://proxy.royaleapi.dev/v1'

## build a networkx graph of cards used by the top 100 players in the world
client = Client(token=dev_key, url=proxy_url)
graph = client.create_empty_graph()
top100_graph = client.build_graph(graph, depth=100)