from flask import Flask, render_template, send_from_directory, request, jsonify
import requests
import os

app = Flask(__name__, template_folder="pages")

# === ROUTES FRONTEND ===

@app.route('/')
def home():
    return render_template('landing/landing.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot/chatbot.html')


# === SERVIR LES FICHIERS CSS/JS SPÉCIFIQUES ===
@app.route('/pages/<path:filename>')
def serve_page_files(filename):
    return send_from_directory('pages', filename)

"""
# === API POUR COMMUNIQUER AVEC RASA ===
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get("message")
    rasa_url = "http://localhost:5005/webhooks/rest/webhook"  # URL du serveur Rasa

    try:
        response = requests.post(rasa_url, json={"message": user_message})
        data = response.json()

        if data and "text" in data[0]:
            return jsonify({"response": data[0]["text"]})
        else:
            return jsonify({"response": "Désolé, je n’ai pas compris 😅"})
    except Exception as e:
        return jsonify({"response": f"Erreur de connexion au serveur Rasa : {e}"})

"""
@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get("message")
    # Réponse factice pour tester l'interface
    fake_reply = f"Tu as dit : {user_message} 😄 (Rasa non connecté)"
    return jsonify({"response": fake_reply})


if __name__ == '__main__':
    app.run(debug=True)
