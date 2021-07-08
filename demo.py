from RoyaleAPI import Client

with open('RoyaleAPI/key.txt', 'r') as file:
        dev_key = file.read().replace('\n', '')
proxy_url = 'https://proxy.royaleapi.dev/v1'

client = Client(token=dev_key, url=proxy_url)
graph = client.create_empty_graph()
top100_graph = client.build_graph(graph, depth=100)