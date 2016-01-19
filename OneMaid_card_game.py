# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 14:11:44 2016

@author: Prashan
"""

from itertools import product
import random
import collections

class Deck():
    
    suite_names = ['H','D','S','C']
    card_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13] #ace = 1, Jack = 11, Queen = 12, King = 13
        
    def __init__(self):
        self.hands=[]
        self.all_cards=[]
        [self.all_cards.append(Card(suite,num)) for suite,num in product(self.suite_names,self.card_numbers)]    
        
    def get_hands(self):
        return self.hands
        
    def set_hands(self,new_hands):
        self.hands = new_hands
        
    def get_cards(self):
        return self.all_cards
        
    def set_cards(self,all_cards):
        self.all_cards = all_cards
        
        
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    def print_all_hands(self):
        for hand in self.hands:
            print hand.__str__()

    def deal_hands(self,player_names):
        dealt_cards=collections.defaultdict(list)
        for i in range(len(self.all_cards)):
            dealt_cards[i%len(player_names)].append(self.all_cards[i])
        for i,name in enumerate(player_names):
            self.hands.append(Hand(name,dealt_cards[i]))
            
    def __str__(self):
        return ','.join([card.__str__() for card in self.all_cards])
        
        
class Hand():
    def __init__(self,name,cards):
        self.name=name
        self.cards=cards
        
    def get_cards(self):
        return self.cards
        
    def get_name(self):
        return self.name
        
    def __str__(self):
        return self.name+': ['+','.join([card.__str__() for card in self.cards])+']'
        
        
class Card():
    
    def __init__(self,suite,number):
        self.suite = suite
        self.number = number
        
    def __str__(self):
        return self.suite + str(self.number)
        
        
        
class CardGame():
    def __init__(self,players):
        self.players=players
        
class OneMaid(CardGame):
    matching_cards={'H':'D','D':'H','S':'C','C':'S'}
    def __init__(self,players):
        '''Creates a deck. Shuffles it. Deals the cards to players'''
        CardGame.__init__(self,players)
        self.deck=Deck()
        #remove 'S12' based on OneMaid rukes
        all_cards = self.deck.get_cards()
        self.deck.set_cards([card for card in all_cards if str(card)!='S12'])
        #shuffle the deck
        self.deck.shuffle()
        print 'dealing hands'
        self.deck.deal_hands(players)
        
        

    def pair_and_remove(self):
        print 'pairing and removing'
        reduced_hands = [] 
        for hand in self.deck.get_hands():
            red_hand = self.reduce_hand(hand)
            print hand.get_name(),':before reducing',len(hand.get_cards()),'new after reducing',len(red_hand.get_cards())
            reduced_hands.append(red_hand)
        self.deck.set_hands(reduced_hands)    
    
    def reduce_hand(self,hand):
        cards_copy=hand.get_cards()
        items_to_remove=[]
        for i in range(len(hand.get_cards())):
            for j in range(i+1,len(hand.get_cards())):
                if (cards_copy[i].number==cards_copy[j].number and self.matching_cards[cards_copy[i].suite]==cards_copy[j].suite):
                    items_to_remove.append(cards_copy[i])
                    items_to_remove.append(cards_copy[j])
                    
        reduced_list = [item  for item in cards_copy if item not in items_to_remove]
        new_reduced_hand=Hand(hand.name,reduced_list)
        
        return new_reduced_hand
                    
                
    def print_game_deck(self):
        print 'printing game deck'
        self.deck.print_all_hands()
        
    
    def get_total_cards(self,deck):
        total_length=0
        for hand in self.deck.get_hands():
            total_length+=len(hand.get_cards())
       
        return total_length 
    
    
    def game_end(self):
        if self.get_total_cards(self.deck)==1:
            return True
        else:
            return False  
            
            
    def select_card(self,turn):
        
        if turn!=(len(self.players)-1):
            neighbor=turn+1
        else:
            neighbor=0
        selected_card=random.choice(self.deck.get_hands()[neighbor].get_cards())
        print self.deck.get_hands()[turn].get_name(),' selected ',str(selected_card),' from ',self.deck.get_hands()[neighbor].get_name()
            
        self.deck.get_hands()[neighbor].get_cards().remove(selected_card)
        self.deck.get_hands()[turn].get_cards().append(selected_card)
            

if __name__=="__main__":
    players=['Prashan','Annie','Bernie','Clair']  #0,1,2,3
    current_game=OneMaid(players)
    current_game.print_game_deck()
    current_game.pair_and_remove()
    current_game.print_game_deck()
    
    i=0
    
    while (current_game.game_end()==False):
        print '-----------------------------------'
        print 'turn ',i
        current_game.select_card(i%len(players))
        i+=1
        current_game.pair_and_remove()