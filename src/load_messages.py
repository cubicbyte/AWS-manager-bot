import json

file = open('messages.json', 'r', encoding='utf-8')
messages = json.load(file)
file.close()
