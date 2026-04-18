from flask import Flask, render_template, request, jsonify
import sqlite3
import openai

app = Flask(__name__)

# 👉 Tamari API key mukvi
openai.api_key = "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"

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": msg}]
        )
        return response.choices[0].message["content"]
    except:
        return "Error avyo "

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