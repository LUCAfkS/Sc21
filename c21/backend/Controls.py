from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from time import sleep
from threading import Thread

app = Flask(__name__, template_folder='../templates', static_folder='../styles',)
socketio = SocketIO(app, cors_allowed_origins="*")  # Liberando CORS para testes locais

@app.route('/')
def home():
    return render_template('game-page.html')

@socketio.on('message')
def handle_message(msg):
    print(f"Mensagem recebida: {msg}")
    send("Mensagem recebida no servidor!", broadcast=True)


@socketio.on('times')
def receber_tempo(valor):
    print('Tempo recebido:', valor)
    emit('resposta_tempo', f"Tempo recebido: {valor}")

def timer():
    s= 30
    m= 1
    first = True
    while True:
        s-=1
        if s ==0 and m ==0:
            socketio.emit('timer',str(m)+':0'+str(s)) 
            break
        elif s ==0:
            s+=59
            m-=1
        if s < 10:
            socketio.emit('timer',str(m)+':0'+str(s)) 
        else:
            socketio.emit('timer',str(m)+':'+str(s)) 
        sleep(1)

if __name__ == '__main__':
    Thread(target=timer).start()
    socketio.run(app, debug=True)
