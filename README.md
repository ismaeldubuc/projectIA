# ProjectIA

## Description
Ce projet est une IA de type chatbot utilisant ollama qui lui recupérera un RAG sur aws S3 afin de l'apprendre et de l'utiliser pour répondre à des questions.

## Installation
- Cloner le projet
- Créer un fichier .env et y ajouter les clés d'accès aws (si besoin m'écrire afin de les obtenir)
- Lancer le script upload.py pour uploader le fichier pdf dans un bucket S3 avec la commande suivante : python3.11 upload.py
- Lancer le script localrag.py pour lancer le chat avec Ollama avec la commande suivante : python3.11 localrag.py --model llama3.2 

## A Noter
- Lorsque le script localrag.py est lancé, il faut patienter quelques minutes avant que le chat soit opérationnel, cela est du au fait que Ollama charge les embeddings dans la mémoire vive et cela peut prendre quelques minutes

## Contact

En cas de problème, vous pouvez me contacter via :
- Mail : ismael.dubuc@gmail.com
- Discord : ismael_d