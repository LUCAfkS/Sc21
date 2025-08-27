from flask import Flask, render_template
from flask_socketio import SocketIO, emit
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
    
    for i in ['player1','player2','player1','player2']:
        b={'request':i}
        dar(b)
    


@socketio.on('scan_cookiesp')
def scanc(request):
    if request['request']:
        emit('delete_players')


@socketio.on('selecionar_p')
def selecionar_p(Request):
    player = Request['player']
    request = Request['cookie']

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
    print(f"[DEBUG] Cartas no deck antes de dar: {len(mesa.deck_cards.cards_list)}")

    carta = deal_card(mesa.deck_cards)
    print(carta)
    try:
        if request['request']== 'player1':
            mesa.player_one.hand_C.append(carta[0])
        else:
            mesa.player_two.hand_C.append(carta[0])
    except: emit('dei',{'numero_da_carta': None},broadcast=True);return

    emit('dei',{'numero_da_carta': carta[0]},broadcast=True)

@socketio.on('max')
def limitador(Request):
    request = Request
    soma=0
    print('p1',mesa.player_one.hand_C)
    print('p2',mesa.player_two.hand_C)
    if request['request'] == 'player1':
        for cs in mesa.player_one.hand_C: soma+=cs
        print('deck1 ',request['request'])
        emit('limit',{'soma':soma,'mesa':mesa.limit_burst},)
    elif request['request'] == 'player2':
        for cs in mesa.player_two.hand_C: soma+=cs
        print('deck2 ',request['request'])
        emit('limit',{'soma':soma,'mesa':mesa.limit_burst},)

@socketio.on('reset')
def resetar_timer():
    mesa.timer_running = False
    



@socketio.on('delete_tuto')
def delete_tutorial():
    return

@socketio.on('space')
def espaçado():
    emit('trocar',broadcast=True)

@socketio.on('ver_t')
def ver_v():
    emit('vitoria',broadcast=True)

@socketio.on('contar_pontos')
def dar_resultado():
    if sum(mesa.player_two.hand_C) >21 and sum(mesa.player_one.hand_C) >21:
        a = mesa.player_one.hand_C
        k = mesa.player_two.hand_C
        mesa.player_two.hand_C = a
        mesa.player_one.hand_C = k

    if sum(mesa.player_one.hand_C) >21: 
        mesa.player_one.hand_C.append(-21)
    if sum(mesa.player_two.hand_C) >21: 
        mesa.player_two.hand_C.append(-21)


        

    if sum(mesa.player_one.hand_C) == sum(mesa.player_two.hand_C):
        mesa.resetar_r()

        emit('resetar_c',broadcast=True)
        sleep(1)
        for i in ['player1','player2','player1','player2']:
            b={'request':i}
            dar(b)
    elif sum(mesa.player_one.hand_C) < sum(mesa.player_two.hand_C):
        mesa.resetar_r()
        
        mesa.player_one.life -=mesa.value_round
        mesa.player_two.life +=mesa.value_round
        mesa.value_round+=1
        emit('at_dano',{'dano':mesa.value_round},broadcast=True)

        vida2 = mesa.player_one.life
        vida1 = mesa.player_two.life

        emit('resetar_c',broadcast=True)
        sleep(1)
        emit('diminuir_v',{'jogador':'player1','vida2':vida2,'vida1':vida1},broadcast=True)
        if not(mesa.player_one.life <=0) or not(mesa.player_two.life <=0):
            # for i in ['player1','player2','player1','player2']:
            #     b={'request':i}
            #     dar(b)
            pass
        else:
            emit('finalizar_jogo',broadcast=True)
            pass
    else:
        mesa.resetar_r()

        mesa.player_two.life -=mesa.value_round
        mesa.player_one.life +=mesa.value_round
        mesa.value_round+=1
        emit('at_dano',{'dano':mesa.value_round},broadcast=True)

        vida2 = mesa.player_one.life
        vida1 = mesa.player_two.life


        emit('resetar_c',broadcast=True)
        sleep(1)
        emit('diminuir_v',{'jogador':'player2','vida1':vida1,'vida2':vida2},broadcast=True)
        if not(mesa.player_one.life <=0) or not(mesa.player_two.life <=0):
            # for i in ['player1','player2','player1','player2']:
            #     b={'request':i}
            #     dar(b)
            pass
        else:
            emit('finalizar_jogo',broadcast=True)
            pass


if __name__ == '__main__':
    
    socketio.run(app, debug=True,host='0.0.0.0' )#host='0.0.0.0'