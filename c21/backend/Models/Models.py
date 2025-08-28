from random import randint
from datetime import datetime
from time import sleep
date = datetime.now().strftime('%Y/%m/%d  %H:%M:%S')

class Deck_C:
    def __init__(self,cards:list =[1,2,3,4,5,6,7,8,9,10,11],infinity=False):
        self.cards_list = cards
        self.infinity = infinity

    def reset_cc(self):
        self.cards_list = [1,2,3,4,5,6,7,8,9,10,11]

        

class Deck_T(Deck_C):
    def __init__(self, infinity=True,cards:list =['bet','betbet','rebirth','shield',
                                                  'due-tramps','erase-your','especial-bet','exchange','refresh',
                                                  'for-17','for-24']):
        super().__init__(cards, infinity)
        
def deal_card(deck: Deck_C, number_of_cards: int = 1, letter_number: int = 0) -> list:
    return_list = []

    if not deck.cards_list:
        print(f'[log][{date}]: Baralho vazio. Nenhuma carta distribuída.')
        return []

    try:
        if letter_number == 0:
            for _ in range(number_of_cards):
                random_index = randint(0, len(deck.cards_list) - 1)
                return_list.append(deck.cards_list[random_index])
                if not deck.infinity:
                    deck.cards_list.pop(random_index)
        elif 0 < letter_number <= len(deck.cards_list):
            return_list.append(deck.cards_list[letter_number - 1])
            if not deck.infinity:
                deck.cards_list.pop(letter_number - 1)
        else:
            raise ValueError(f'Índice inválido: {letter_number}')
    except Exception as e:
        print(f'[ERRO] ao distribuir carta: {e}')
        return []

    return return_list





class Player:
    def __init__(self,deck_C: list,deck_T: list):
        self.life = 5
        self.attack = 1
        self.hand_C = []
        self.hand_T = []
    
def use_taramp(self,table: 'Table',recipient: 'Player', taramp: str):
    if taramp in self.hand_T:
        match taramp:

            case 'bet': 
                table.value_round+=1
                table.socketio.emit('at_dano',namespace='/')

            case 'betbet':
                table.value_round+=2
                table.socketio.emit('at_dano',namespace='/')


            case 'shield':
                table.value_round-=1
                table.socketio.emit('at_dano',namespace='/')


            case 'due-tramps':
                return 


            case 'erase-your':
                return


            case 'especial-bet':
                return


            case 'exchange':
                return


            case 'refresh':
                return

            case 'for-17':
                return 17


            case 'for-24':
                return 24


            case _:
                pass

class Table:
    
    def __init__(self, socketio = 'socketio'):
        self.socketio = socketio

        self.deck_cards = Deck_C()
        self.deck_tramps = Deck_T()
        self.player_one = Player(self.deck_cards, self.deck_tramps)
        self.player_two = Player(self.deck_cards, self.deck_tramps)

        self.value_round = 1
        self.limit_burst = 21
        self.remaining_time = 90
    
    def time_run(self):
        s = 30
        m = 1
        self.timer_running = True  # Flag de controle

        while self.timer_running:
            s -= 1
            self.remaining_time -= 1

            if s == 0 and m == 0:
                self.socketio.emit('timer', f'{m}:0{s}', namespace='/')
                break

            elif s == 0:
                s = 59
                m -= 1

            if s < 10:
                self.socketio.emit('timer', f'{m}:0{s}', namespace='/')
            else:
                self.socketio.emit('timer', f'{m}:{s}', namespace='/')

            self.socketio.sleep(1)
        if s==0 and m==0:
            self.socketio.emit('trocar', namespace='/')
        self.time_run()


        
    def tramped(self,tramp:str):
        match tramp:

            case 'bet'|'betbet'|'shield'|'rebirth':
                pass
            
            case 'due-tramps'|'erase-your'|'especial-bet'|'exchange'|'refresh':
                pass
            
            case 'for-17'|'for-24':
                pass

    def resetar_r(self):
        self.deck_cards.cards_list = [1,2,3,4,5,6,7,8,9,10,11]
        self.limit_burst = 21
        
        self.player_one.hand_C = []
        self.player_two.hand_C = []
        

#debbuger
if __name__ == "__main__":
    mesa = Table()
    for i in mesa.deck_cards.cards_list:
        deal_card(mesa.deck_cards,letter_number=i)
    mesa.resetar_r()
    print(deal_card(mesa.deck_cards))