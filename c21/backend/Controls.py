from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from time import sleep
from threading import Thread

from Models.Models import deal_card, use_taramp
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

        elif player == 'jogador2':
            mesa.p2 = player
            emit('delete_player2',broadcast=True)
            emit('delete_players')

        if mesa.p1 and mesa.p2:
            start_game()
    
    else: emit('delete_players')


@socketio.on('deal')
def dar(request):

    carta = deal_card(mesa.deck_cards)
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
    if request['request'] == 'player1':
        for cs in mesa.player_one.hand_C: soma+=cs
        emit('limit',{'soma':soma,'mesa':mesa.limit_burst},)
    elif request['request'] == 'player2':
        for cs in mesa.player_two.hand_C: soma+=cs
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

def emitir_reset():
    sleep(4)
    emit('resetar_c', broadcast=True)


@socketio.on('contar_pontos')
def dar_resultado():

    vida1 = mesa.player_two.life
    vida2 = mesa.player_one.life
    limite = mesa.limit_burst
    soma1 = sum(mesa.player_one.hand_C)
    soma2 = sum(mesa.player_two.hand_C)

    estourou1 = soma1 > limite
    estourou2 = soma2 > limite

    if estourou1:
        mesa.player_one.hand_C.append(-limite)
        soma1 = -(sum(mesa.player_one.hand_C))
    if estourou2:
        mesa.player_two.hand_C.append(-limite)
        soma2 = -(sum(mesa.player_two.hand_C))

    # Empate absoluto
    if (not estourou1 and not estourou2) and (soma1 == soma2):
        mesa.resetar_r()
        emitir_reset()

        return

    # Aplica resultado
    mesa.resetar_r()
    dano = mesa.value_round
    mesa.value_round += 1

    if soma1 > soma2:
        mesa.player_one.life += dano
        mesa.player_two.life -= dano
        vida1 = mesa.player_two.life
        vida2 = mesa.player_one.life
        emitir_reset()
        sleep(1)
        start_game()
        emit('at_dano', {'dano': dano}, broadcast=True)
        emit('diminuir_v', {'jogador': 'player2', 'vida1': vida2, 'vida2': vida1}, broadcast=True)
    elif soma2 > soma1:
        mesa.player_two.life += dano
        mesa.player_one.life -= dano
        vida1 = mesa.player_two.life
        vida2 = mesa.player_one.life
        emitir_reset()
        sleep(1)
        start_game()
        emit('at_dano', {'dano': dano}, broadcast=True)
        emit('diminuir_v', {'jogador': 'player1', 'vida1': vida2, 'vida2': vida1}, broadcast=True)

    # Verifica fim de jogo
    if mesa.player_two.life <= 0 or mesa.player_one.life <= 0:
        print('entroooou')
        ganhador = 'p1' if mesa.player_one.life <=0 else ''
        ganhador = 'p2' if mesa.player_two.life <=0 else ''
        emit('finalizar_jogo',{'ganhador':ganhador} ,broadcast=True)


@socketio.on('u_taramp')
def us_taramp(data):
    if data.jogador_at == 'player1':
        use_taramp()
    



if __name__ == '__main__':
    
    socketio.run(app, debug=True,host='0.0.0.0' )#host='0.0.0.0'