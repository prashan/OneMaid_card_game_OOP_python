# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:11:44 2016

@author: Prashan
"""

## This is the text editor interface. 
## Anything you type or change here will be seen by the other person in real time.


from itertools import product
import random
import collections

class Card():
    
    def __init__(self,suite,number):
        self.suite = suite
        self.number = number
        
    def __str__(self):
        return self.suite + str(self.number)

class Deck():
    
    suite_names = ['H','D','S','C']
    card_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13] #ace = 1, Jack = 11, Queen = 12, King = 13
        
    def __init__(self):
        self.all_cards=[]
        [self.all_cards.append(Card(suite,num)) for suite,num in product(self.suite_names,self.card_numbers)]    
        
    def get_cards(self):
        return self.all_cards
        
    def set_cards(self,all_cards):
        self.all_cards = all_cards
        
    def remove_card(self,card):
        if card in self.all_cards:
            self.all_cards.remove(card)
        else:
            raise 'card not in deck'
    
    def deck_size(self):
        return len(self.all_cards)
        
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    def deal_hands(self,player_names,num_cards):
        print 'dealing hands'
        hands=[]
        dealt_cards=collections.defaultdict(list)
        for i in range(num_cards):
            if len(self.all_cards)!=0:
                dealt_cards[i%len(player_names)].append(self.all_cards.pop())
        for i,name in enumerate(player_names):
            hands.append(Hand(name,dealt_cards[i]))
        return hands
            
    def __str__(self):
        return ','.join([card.__str__() for card in self.all_cards])
        
        
class Hand():
    
    matching_cards={'H':'D','D':'H','S':'C','C':'S'}
    
    def __init__(self,name,cards):
        self.name=name
        self.cards=cards
        
    def get_cards(self):
        return self.cards
        
    def get_name(self):
        return self.name
        
    def get_size(self):
        return len(self.cards)
        
    def __str__(self):
        return self.name+': ['+','.join([card.__str__() for card in self.cards])+']'
        
        
    def remove(self,card):
        index_to_remove=[i for c in self.cards if str(c)==str(card)]
        del self.cards[index_to_remove]
        
        
    
    def pair_and_remove(self):
        cards_copy=list(self.get_cards())
        for i in range(len(cards_copy)):
            for j in range(i+1,len(cards_copy)):
                if (cards_copy[i].number==cards_copy[j].number and self.matching_cards[cards_copy[i].suite]==cards_copy[j].suite):
                    self.cards.remove(cards_copy[i])
                    self.cards.remove(cards_copy[j])
                    
        print self.get_name(),':before reducing',len(self.get_cards()),'after reducing',len(self.get_cards())
        
        if self.get_size()==0:
            print self.get_name()+' finished cards'
        return self.get_size()
                
        
class CardGame():
    def __init__(self,players):
        self.hands=[]
        self.players=players
        self.deck=Deck()
        self.deck.shuffle()
        
    def get_hands(self):
        return self.hands
        
    def set_hands(self,new_hands):
        self.hands = new_hands
        
    def print_all_hands(self):
        for hand in self.hands:
            print hand.__str__()
        
class OneMaid(CardGame):
   
    def __init__(self,players):
        '''Creates a deck. Shuffles it. Deals the cards to players'''
        CardGame.__init__(self,players)
        self.remove_S_queen()
        dealt_hands = self.deck.deal_hands(players,999)
        self.set_hands(dealt_hands)
        
    
    def remove_S_queen(self):
        '''Remove spades queen'''
        all_cards = self.deck.get_cards()
        self.deck.set_cards([card for card in all_cards if str(card)!='S12'])
        
       
    def play(self):
        hand_copy=list(self.get_hands())
        for hand in hand_copy:
            if hand.pair_and_remove()==0:
                self.get_hands().remove(hand)
                self.players.remove(hand.get_name())
   
    def get_players(self):
        return self.players
    
    def get_total_cards(self,deck):
        total_length=0
        for hand in self.get_hands():
            total_length+=len(hand.get_cards())
       
        return total_length 
    
    
    def game_end(self):
        if self.get_total_cards(self.deck)==1:
            print 'The loser is '+self.get_hands()[0].get_name()
            print 'The last hand is '+','.join([str(card) for hand in self.get_hands() for card in hand.get_cards() ])
            return True
        else:
            return False  
            
            
    def select_card(self,turn):
        
        if turn!=(len(self.players)-1):
            neighbor=turn+1
        else:
            neighbor=0
            
        if len(self.get_hands()[neighbor].get_cards())==0:
            raise "Card length exception"
            
        random.shuffle(self.get_hands()[neighbor].get_cards())
        selected_card=random.choice(self.get_hands()[neighbor].get_cards())
        
        print self.get_hands()[turn].get_name(),' selected ',str(selected_card),' from ',self.get_hands()[neighbor].get_name()
        self.get_hands()[neighbor].get_cards().remove(selected_card)
        self.get_hands()[turn].get_cards().append(selected_card)
            

if __name__=="__main__":
    players=['Prashan','Annie','Bernie','Clair']  #0,1,2,3
    current_game=OneMaid(players)
    current_game.print_all_hands()
    current_game.play()
    current_game.print_all_hands()
    
    i=0
    
    while (current_game.game_end()==False):
        print '-----------------------------------'
        print 'turn ',i
        current_game.select_card(i%len(current_game.get_players()))
        i+=1
        current_game.play()
    
    
    
    