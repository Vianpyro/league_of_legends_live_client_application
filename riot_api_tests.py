import requests
import webbrowser

# Api key
if input('Need new API key? ')[0].lower() == 'y':
    webbrowser.open('https://developer.riotgames.com/', new=1)

# Display player stats by name (API Key = RGAPI-b29f8386-fa35-4afe-b8a9-09417f5e1989)
# Vianpyro Decimus PUUID: rrM25_zwnrDW7V5w9ZzUMZrRa9o0nuDbPcLHwB7Bc6bjJHrGi9TAubA1OE6ntHM9Ht1cI7olY0xwvg
api_key = input('API Key: ')
player_name = input('Player name: ')
player_tag = input('Player region: ')

request = requests.get(f'https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{player_name}/{player_tag}?api_key={api_key}').json()
print(request)
