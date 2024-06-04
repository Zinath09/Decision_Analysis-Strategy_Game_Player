import numpy as np
import random
from player import Player

class Buchnajzer(Player):
    
# Nadpisujemy metodę __init__() Player
    def __init__(self, name):
        # Wywołujemy metodę __init__() klasy Player, która inicjalizuje
        # atrybuty wspólne dla obu klas.
        super().__init__( name)
        self.cards = []
        self.pile = []
        self.opponent = set()
        self.deck = set()

    def getCheckFeedback(self, checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True):
        super().getCheckFeedback( checked, iChecked, iDrewCards, revealedCard, noTakenCards, log=True)
        if checked: 
            if iChecked and iDrewCards: #sprawdziłam i dobrałam, czyli się myliłam mówił prawdę
                self.addToCards(self.pile[-noTakenCards:]) #wzięłam karty
            
            if iChecked and not iDrewCards: #sprawdziłam i on dobrał, czyli kłamał
                self.opponent |= set(self.pile[-noTakenCards:]) #wziął karty
            
            if not iChecked and iDrewCards: #kiedy on sprawdził i ja dobrałam
                self.addToCards(self.pile[-noTakenCards:]) #wzięłam karty
            
            if not iChecked and iDrewCards: #kiedy on sprawdził i on dobrał
                self.opponent |= set(self.pile[-noTakenCards:]) #wziął karty

            self.pile = self.pile[:noTakenCards] #usunęły się karty

    
    def is_impossible_card(self, declared_card):
        if declared_card in self.cards:
            return True #impossible declared card
        if declared_card in self.pile:
            return True  #impossible declared card
        return False
        
    ### player's random strategy
    def putCard(self, declared_card):

    # kiedy masz ostatnią kartą
        if len(self.cards) == 1 and declared_card is not None and self.cards[0][0] >= declared_card[0]:
            return self.cards[0], self.cards[0]  #random sample zwraca listę więc ją rozpakowuję i podaję fakową jej wartość taka jak początkowy gracz
        
    
    # 5% of randomness
        if random.random()>0.95: 
            ### if (s)he decides to cheat, (s)he randomly declares the card.
            declaration = random.choice(self.cards)             
            ### Yet, declared card should be no worse than a card on the top of the pile . 
            if declared_card is not None and declaration[0] < declared_card[0]:
                declaration = (min(declared_card[0]+1,14), declaration[1])
        
    ### player tries to put the minimal card on the table
        if self.pile==0 or declared_card == None:
            card = min(self.cards)
            declaration = card
        else:
            self.cards.sort()
            card = None
            for i in self.cards:
                if i[0]>=declared_card[0]:
                    card= i                
            declaration = i 

        ### return the decision (true card) and declaration (player's declaration)
        return card, declaration
    
    
    ###  decides whether to check or not
    def checkCard(self, opponent_declaration):
        if opponent_declaration[0]>max(self.cards)[0]:
            return True #we want to check if we cannot put any card
        if len(self.cards)==1:
            return False
        if self.is_impossible_card(opponent_declaration):
            return True #we want to check, if we know, that the card is in our deck or in pile

        if len(self.opponent)==1: #jeśli przeciwnikowi została ostatnia karta ( czy przedostatnia) Gra się kończy jak będzie ktoś miał wszystkie karty na stole
            return True
        
        return False
    
    def addToCards(self, cards):
        for i in cards:
            self.cards.append(i)