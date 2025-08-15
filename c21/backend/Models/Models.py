from random import randint

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
        for i in range(number_of_cards):
            random_index = randint(0,len(deck.cards_list)-1)
            return_list.append(deck.cards_list[random_index])
            if not(deck.infinity): deck.cards_list.pop(random_index)

        return return_list

    elif letter_number in deck.cards_list:
        return_list.append(deck.cards_list[letter_number-1])
        if not(deck.infinity): deck.cards_list.pop(letter_number-1)
        return return_list
    
    else: print(ValueError(letter_number))



class Player:
    def __init__(self,deck_C: Deck_C,deck_T: Deck_T = Deck_T()):
        self.hand_C = deal_card(deck_C)
        self.hand_T = deal_card(deck_T)
    
    def use_taramp(self,table: 'Table',recipient: 'Player', taramp: str):
        if taramp in self.hand_T:
            match taramp:

                case 'bet': 
                    print('bettttt')


                case 'betbet':
                    pass


                case 'rebirth':
                    pass


                case 'shield':
                    pass


                case 'due-tramps':
                    pass


                case 'erase-your':
                    pass


                case 'especial-bet':
                    pass


                case 'exchange':
                    pass


                case 'refresh':
                    pass


                case 'for-17':
                    pass


                case 'for-24':
                    pass


                case _:
                    pass


     


        


class Table:
    pass

if __name__ == "__main__":
    DC = Deck_C()
    # print(deal_card(DC,11))
    P1 = Player(DC)
    P2 = Player(DC)
    