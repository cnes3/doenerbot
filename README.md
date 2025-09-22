# doenerbot
telegram bot for rating doener

## Access
save the telegram-bot-token (get it from the BotFather) in the file "bottoken.txt" and start the server.

get credentials.json from your google one cloud access (see https://developers.google.com/workspace/sheets/api/quickstart/python)

## Architecture-ideas
1. interface - chat interaction and prepare dict
2. export function - append google sheet with the dict 

## Data-structure (Dict with key/type)
- Name : str
- Preis : float
- Geschmack : int [1:10]
- Frische (vom Gemüse) : int [1:10]
- Soßen : int [1:10]
- Besonderheiten : str
- Bedienung : int [1:10]
- Größe + Charakter : int [1:10]
- Fleischmenge : int [1:10]
- Geschwindigkeit / Wartezeit : int [1:10]