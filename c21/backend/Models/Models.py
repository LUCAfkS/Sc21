from random import randint
from datetime import datetime
from time import sleep
date = datetime.now().strftime('%Y/%m/%d  %H:%M:%S')

class Deck_C:
    def __init__(self,cards:list =[1,2,3,4,5,6,7,8,9,10,11],infinity=False):
        self.cards_list = cards
        self.infinity = infinity

        

class Deck_T(Deck_C):
    def __init__(self, infinity=True,cards:list =['bet','betbet','rebirth','shield',
                                                  'due-tramps','erase-your','especial-bet','exchange','refresh',
                                                  'for-17','for-24']):
        super().__init__(cards, infinity)
        
def deal_card(deck: Deck_C,number_of_cards:int = 1,letter_number:int = 0) -> list:
    return_list = []
    if letter_number == 0:
        try:
            for i in range(number_of_cards):
                random_index = randint(0,len(deck.cards_list)-1)
                return_list.append(deck.cards_list[random_index])
                if not(deck.infinity): deck.cards_list.pop(random_index)
        except: print(f'[log][{date}]: solo card:{return_list}--{random_index}')
        return return_list

    elif letter_number in deck.cards_list:
        return_list.append(deck.cards_list[letter_number-1])
        if not(deck.infinity): deck.cards_list.pop(letter_number-1)
        print(f'[log][{date}]: mutiple cards:{return_list}')
        return return_list
    
    else: raise(ValueError(f'[error][{date}]: letter of number {letter_number} invalid'))



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
                    return 1


                case 'betbet':
                    return 2


                case 'shield':
                    return -1


                case 'rebirth':
                    return 0


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
    
    def __init__(self, socketio):
        self.socketio = socketio

        self.deck_cards = Deck_C()
        self.deck_tramps = Deck_T()
        self.player_one = Player(self.deck_cards, self.deck_tramps)
        self.player_two = Player(self.deck_cards, self.deck_tramps)

        self.round = 1
        self.limit_burst = 21
        self.remaining_time = 90
    
    def time_run(self):
        s= 30
        m= 1
        first = True
        while True:
            s-=1
            self.remaining_time-=1 
            if s ==0 and m ==0:
                self.socketio.emit('timer',str(m)+':0'+str(s),namespace='/',)
                self.round +=1
                break
            elif s ==0:
                s+=59
                m-=1
            if s < 10:
                self.socketio.emit('timer',str(m)+':0'+str(s),namespace='/',)

            else:
                self.socketio.emit('timer',str(m)+':'+str(s),namespace='/',)

            self.socketio.sleep(1)
        
    def tramped(self,tramp:str):
        match tramp:

            case 'bet'|'betbet'|'shield'|'rebirth':
                pass
            
            case 'due-tramps'|'erase-your'|'especial-bet'|'exchange'|'refresh':
                pass
            
            case 'for-17'|'for-24':
                pass

#debbuger
if __name__ == "__main__":
    pass