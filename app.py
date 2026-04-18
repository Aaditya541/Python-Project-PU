from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env
load_dotenv()

# Get API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

# ---------------- DATABASE ----------------
def save_chat(user, bot):
    conn = sqlite3.connect("chat.db")
    conn.execute("CREATE TABLE IF NOT EXISTS chat (user TEXT, bot TEXT)")
    conn.execute("INSERT INTO chat (user, bot) VALUES (?, ?)", (user, bot))
    conn.commit()
    conn.close()

# ---------------- AI RESPONSE ----------------
def chatbot_response(msg):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": msg}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Error avyo: " + str(e)

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def reply():
    user_msg = request.form['msg']
    bot_reply = chatbot_response(user_msg)

    save_chat(user_msg, bot_reply)

    return jsonify(bot_reply)

if __name__ == "__main__":
    app.run(debug=True)