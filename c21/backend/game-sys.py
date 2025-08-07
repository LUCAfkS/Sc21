from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__, template_folder='../templates', static_folder='../styles')
socketio = SocketIO(app, cors_allowed_origins="*")  # Liberando CORS para testes locais

@app.route('/')
def home():
    return render_template('game-page.html')

@socketio.on('message')
def handle_message(msg):
    print(f"Mensagem recebida: {msg}")
    send("Mensagem recebida no servidor!", broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
