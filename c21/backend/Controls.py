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

def start_game():
    if mesa.remaining_time == 90:
        socketio.start_background_task(target=mesa.time_run,)
    dar()


@socketio.on('scan_cookiesp')
def scanc(request):
    if request['request']:
        emit('delete_players')


@socketio.on('selecionar_p')
def selecionar_p(player):
    player = player['player']
    request = player['cookie']

    if not(request):

        if player == 'jogador1':
            mesa.p1 = player
            emit('delete_player1',broadcast=True)
            emit('delete_players')
            print(mesa.p1)

        elif player == 'jogador2':
            mesa.p2 = player
            emit('delete_player2',broadcast=True)
            emit('delete_players')
            print(mesa.p2)

        if mesa.p1 and mesa.p2:
            print('começou')
            start_game()
    
    else: emit('delete_players')


@socketio.on('deal')
def dar(request):
    request['request']
    carta = deal_card(mesa.deck_cards)
    if request['request']== 'player1':
        mesa.player_one.hand_C.append(carta[0])
    else:
        mesa.player_two.hand_C.append(carta[0])
    emit('dei',{'numero_da_carta': carta[0]},broadcast=True)

@socketio.on('max')
def limitador(request):
    soma=0
    if request['request'] == 'player1':
        for cs in mesa.player_one.hand_C: soma+=cs
        print(request['request'])
        emit('limit',{'soma':soma,'mesa':mesa.limit_burst},)
    else:
        # request['request'] == 'player2':
        for cs in mesa.player_two.hand_C: soma+=cs
        print(request['request'])
        emit('limit',{'soma':soma,'mesa':mesa.limit_burst},)




@socketio.on('delete_tuto')
def delete_tutorial():
    return





if __name__ == '__main__':
    
    socketio.run(app, debug=True, )#host='0.0.0.0'
