API Geo – TP2


1) ouvrir le dossier `api-geo`.
2) Définir la clé OpenRouteService (ORS):

j'ai creer un compte chez openrouteservice
voici le lien de la cle :
https://account.heigit.org/manage/key


Démarrer le serveur
Par défaut: `http://127.0.0.1:5000`

Exemples rapides
- `http://127.0.0.1:5000`
- `http://127.0.0.1:5000/coords/Paris`
- `http://127.0.0.1:5000/coords/Londres`
- `http://127.0.0.1:5000/distance?from=Paris&to=Londres`


Pourquoi debug=True est utile en développement:

Auto-reload: le serveur se relance automatiquement dès que vous modifiez un fichier (reloader), évitant les redémarrages manuels.
Debugger interactif: en cas d’erreur, Flask/Werkzeug affiche une page avec la trace détaillée et une console interactive pour inspecter l’état.
Messages d’erreur détaillés: stack traces complètes et contexte facilitant le diagnostic rapide.
Logs verbeux: sorties de log supplémentaires utiles pour comprendre le flux pendant le dev.


Pourquoi préciser format=json avec Nominatim:

Sortie machine‑lisible: force une réponse JSON (au lieu de HTML/XML), facile à parser dans le code.
Champs attendus: garantit la présence de clés comme lat et lon au bon endroit.
Type MIME cohérent: renvoie Content-Type: application/json, évitant des parsings hasardeux.
Réduction d’ambiguïtés: évite la page HTML par défaut (pensée pour humains) et les variations d’affichage.
Taille et performance: réponse généralement plus compacte que HTML/XML.


http://127.0.0.1:5000
Bienvenue sur l'API Geo !
http://127.0.0.1:5000/coords/Paris
{
  "city": "Paris",
  "lat": 48.8534951,
  "lon": 2.3483915
}
http://127.0.0.1:5000/coords/Londres
{
  "city": "Londres",
  "lat": 51.4893335,
  "lon": -0.1440551
}
http://127.0.0.1:5000/distance?from=Paris&to=Londres
{
  "distance_km": 459.334,
  "from": "Paris",
  "profile": "driving-car",
  "to": "Londres"
}


Pourquoi limiter le nombre d’appels API:

Quotas et rate limiting: éviter le dépassement (erreurs 429), suspension de la clé.
Coûts: certaines APIs facturent à l’appel; limiter réduit la facture.
Performance: moins d’appels = latence réduite, application plus réactive.
Fiabilité: risque moindre de timeouts/pannes lors de pics; meilleure tolérance aux erreurs.
Équité et conformité: respect des ToS et des politiques d’usage “fair use”.
Ressources client: économie de batterie/données réseau (mobiles)


Expliquer la persistance de l’historique:

Mémoire vs. disque: actuellement l’historique est en mémoire (RAM). Quand le serveur redémarre, la RAM est vidée, donc l’historique disparaît. Pour le conserver, il faut l’écrire sur un support persistant (fichier ou base de données) puis le recharger au démarrage.
Fichier JSON (le plus simple)
À chaque ajout dans history, on sauvegarde tout le tableau dans un fichier history.json.
Au démarrage du serveur, on lit history.json (s’il existe) et on remplit history.
Avantages: facile à mettre en place. Limites: moins robuste en cas d’écritures concurrentes et moins performant si le fichier grossit.
SQLite (recommandé si l’app grandit)
On stocke chaque entrée sous forme de ligne dans une table.
Avantages: fiable, requêtage facile, meilleure gestion des écritures multiples. Limites: un peu plus de configuration.


En conclusion:

Réponses aux questions
Pourquoi `debug=True` est utile en développement:
- Auto-reload du serveur.
- Debugger interactif avec stack traces détaillées.
- Logs plus verbeux.

Pourquoi préciser `format=json` avec Nominatim:
- Sortie machine‑lisible (JSON) au lieu de HTML/XML.
- Clés attendues (`lat`, `lon`) au bon format.
- Type MIME cohérent (`application/json`).
- Réponses plus compactes.

Pourquoi limiter le nombre d’appels API:
- Quotas/rate limiting (éviter 429 et suspensions).
- Coûts potentiels à l’appel.
- Performance et latence.
- Fiabilité en cas de pics.
- Conformité (fair use) et ressources côté client.

Persistance de l’historique (explication):
- En mémoire, l’historique disparaît au redémarrage.
- Solutions:
  - Fichier JSON: sauvegarder après chaque ajout et recharger au démarrage.
  - SQLite: plus robuste et requêtage facile si l’app grandit.