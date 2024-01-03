import requests
import json

# Remplacez 'YOUR_API_KEY' par votre clé API Mistral
mistral_api_key = 'YOUR_API_KEY'

# URL de l'API
url = 'https://api.mistral.ai/v1/chat/completions'

# En-têtes de la requête
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(mistral_api_key)
}

# Corps de la requête - modeles : mistral-tiny, mistral-small, mistral-medium
data = {
    "model": "mistral-tiny",
    "messages": [{"role": "user", "content": "Who is the most renowned French painter?"}]
}

# Convertir le dictionnaire en format JSON
json_data = json.dumps(data)

# Effectuer la requête POST
response = requests.post(url, headers=headers, data=json_data)

# ...

# Vérifier la réponse
if response.status_code == 200:
    # Traitement de la réponse
    result = response.json()

    # Accéder au contenu du champ 'content'
    content = result['choices'][0]['message']['content']

    # Afficher le contenu
    print(content)

else:
    print('Erreur lors de la requête. Code de statut :', response.status_code)
    print(response.text)
