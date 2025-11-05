# 🦋 Wise Chatbot - Interface Flask

Ce projet propose une **interface web fluide et responsive** pour un chatbot construit avec **Flask**, **HTML**, **CSS** et **JavaScript**.  
Pour l’instant, la partie IA (Rasa) n’est pas encore intégrée : cette version permet de tester uniquement **le design, la navigation et l’interactivité** du chatbot.

---

## 🚀 Fonctionnalités actuelles

- Page d’accueil élégante et responsive.
- Redirection fluide vers la page du chatbot.
- Interface de discussion avec bulles de messages.
- Simulation de réponse automatique pour tester sans Rasa.

---

## 🧱 Structure du projet

wise_chatbot/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│ ├── landing.html
│ └── chatbot.html
│
└── static/
├── css/
│ ├── landing.css
│ └── chatbot.css
└── js/
├── landing.js
└── chatbot.js


---

## ⚙️ Installation et exécution

 ### 1️⃣ Crée un environnement virtuel
```bash
python -m venv env

2️⃣ Active-le
Sous Windows :
env\Scripts\activate

Sous macOS / Linux :
source env/bin/activate

3️⃣ Installe les dépendances
pip install -r requirements.txt

4️⃣ Lance l’application Flask
python app.py


Tu devrais voir :

 * Running on http://127.0.0.1:5000

5️⃣ Ouvre ton navigateur

➡️ Va sur http://localhost:5000

Tu verras la page d’accueil du chatbot 🦋.
Clique sur le bouton 💬 Commencer la discussion pour tester la page du chatbot.

🧠 Mode test (sans Rasa)

 Le code Flask contient une réponse factice :

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get("message")
    fake_reply = f"Tu as dit : {user_message} 😄 (Rasa non connecté)"
    return jsonify({"response": fake_reply})


➡️ Cela te permet de tester l’affichage des bulles sans installer ni exécuter Rasa.

🧰 Technologies utilisées

Flask – serveur web Python

HTML5 / CSS3 – structure et design

JavaScript (Fetch API) – échanges entre l’utilisateur et Flask


💙 Auteur

Créé par Carole Tousse
Assistant intelligent et bienveillant pour asssurer une bonne préinscription — version interface.