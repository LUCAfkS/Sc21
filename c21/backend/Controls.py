from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit, send
from time import sleep
from threading import Thread

from Models.Models import deal_card
import Models.Models as mm


app = Flask(__name__, template_folder='../templates', static_folder='../styles', )
socketio = SocketIO(app, cors_allowed_origins="*",)  # Liberando CORS para testes locais

mesa = mm.Table(socketio)
mesa.p1 = None
mesa.p2 = None

@app.route('/')
def home():
    return render_template('game-page.html')

@socketio.on('selecionar_p')
def selecionar_p(player: dict):
    player = player['player']
    if player == 'jogador1':
        mesa.p1 = player
        print(mesa.p1)
    elif player == 'jogador2':
        mesa.p2 = player
        print(mesa.p2)
    if mesa.p1 != None and mesa.p2 !=None:
        start_game()

@socketio.on('del_tela')
def del_tela():
    socketio.emit('forever',)


@socketio.on('deal')
def dar():
    carta = deal_card(mesa.deck_cards)
    emit('dei',{'numero_da_carta': carta[0]},broadcast=True)


@socketio.on('delete_tuto')
def delete_tutorial():
    return


def start_game():
    if mesa.remaining_time == 90:
        socketio.start_background_task(target=mesa.time_run,)



if __name__ == '__main__':
    
    socketio.run(app, debug=True, )#host='0.0.0.0'
