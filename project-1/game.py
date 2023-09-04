import numpy as np
from enum import Enum
import matplotlib.pyplot as plt

class Side(Enum):
    GIVE_1 = 1
    GIVE_2 = 2
    GET_1 = 3
    GET_2 = 4
    GET_ALL = 5
    ALL_GIVE = 6


class Player:
    def __init__(self, name, money, previous, next):
        self.name: str = name
        self.money: float = money
        self.history = []

        self.lost: float = 0.0
        self.gained: float = 0.0

        # Linked list
        self.previous: Player = previous
        self.next: Player = next
        
    
    # Update and returns the amount of money that was actually updated
    # If the player does not have enough money, it will update the money to 0
    def update(self, side, money) -> float:
        if self.money + money < 0:
            money = -self.money

        if money < 0:
            self.lost += money
        else:
            self.gained += money
        
        self.money += money

        self.history.append((side, money))

        return money

class SpinnerGame:
    def __init__(self, players = 4, initial_momeny = 10.0):
        self.total_players: int = players
        self.initial_momeny: float = initial_momeny

        self.spins: int = 0
        self.pool_money: float = 0.0

        self.active_players: int = players

        self.__init_players()

    
    def __init_players(self):
        self.head_player: Player = None
        self.current_player: Player = None
        self.all_players: list[Player] = []

        previous: Player = None
        for i in range(self.total_players):
            new_player = Player(name=i + 1, money=self.initial_momeny, previous=previous, next=None)
            self.all_players.append(new_player)
            
            if self.head_player is None:
                self.head_player = new_player

            if previous is not None:
                previous.next = new_player
            
            previous = new_player

        # Making it a circular linked list
        previous.next = self.head_player
        self.head_player.previous = previous
        self.current_player = self.head_player

        self.first_broken: Player = None
        self.winner: Player = None
    
    def spin(self) -> Side:
        if self.winner is not None:
            return None
        
        if self.current_player is None:
            return None
        
        self.spins += 1
            
        side = Side(np.random.randint(1, 7))

        if side == Side.GIVE_1:
            self.pool_money += -self.current_player.update(side, -1.0)
        elif side == Side.GIVE_2:
            self.pool_money += -self.current_player.update(side, -2.0)
        elif side == Side.GET_1 and self.pool_money >= 1.0:
            self.pool_money += -self.current_player.update(side, 1.0)
        elif side == Side.GET_2 and self.pool_money >= 2.0:
            self.pool_money += -self.current_player.update(side, 2.0)
        elif side == Side.GET_ALL:
            self.pool_money += -self.current_player.update(side, self.pool_money)
        elif side == Side.ALL_GIVE:
            tmp_player = self.current_player.next

            while tmp_player is not self.current_player:    
                self.pool_money += -tmp_player.update(side, -1.0)

                tmp_player = tmp_player.next

        if self.current_player.money == 0:
            if self.first_broken is None:
                self.first_broken = self.current_player
            
            self.remove_current_player()

        if self.active_players == 1:
            self.winner = self.current_player
            self.head_player = self.current_player
            return side

        self.current_player = self.current_player.next
        
        return side


    def remove_current_player(self):
        if self.current_player is None:
            return

        self.active_players -= 1

        if self.current_player.next == self.current_player:
            self.current_player = None
            return

        self.current_player.previous.next = self.current_player.next
        self.current_player.next.previous = self.current_player.previous

        self.current_player = self.current_player.next

    def summary(self):
        result = f"Pool money: ${self.pool_money}\n"

        tmp_player = self.head_player
        for i in range(self.active_players):
            result += f"Player #{tmp_player.name} has ${tmp_player.money}\n"

            tmp_player = tmp_player.next

        return result + "\n"
    