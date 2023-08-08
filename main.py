import os
import hmac
import hashlib
import sys


class GameInterface:
    def __init__(self, moves):
        self.moves = moves

    def display_hmac(self, hmac):
        print(f"Computer's move HMAC: {hmac}")

    def display_menu(self):
        for idx, move in enumerate(self.moves, 1):
            print(f"{idx}. {move}")
        print("0. Exit")
        choice = int(input("Enter your choice: "))
        return self.moves[choice - 1]

    def display_results(self, user_move, computer_move, result):
        print(f"Your move: {user_move}")
        print(f"Computer's move: {computer_move}")
        if result == "user":
            print("You win!")
        elif result == "computer":
            print("Computer wins!")
        else:
            print("It's a draw!")




class CryptoManager:

    @staticmethod
    def generate_key():
        return os.urandom(32)

    @staticmethod
    def generate_hmac(key, message):
        return hmac.new(key, message.encode(), 'sha256').hexdigest()



class MoveValidator:
    
    @staticmethod
    def validate_moves(moves):
        # Validation logic here
        if len(moves) < 3 or len(moves) % 2 == 0:
            return False, "You need to provide an odd number of non-repeating strings greater than 3."
        elif len(set(moves)) != len(moves):
            return False, "All strings should be unique."
        return True, ""


class RuleEngine:
    def __init__(self, moves):
        self.moves = moves

    def get_winner(self, user_move, computer_move):
        # Determine the winner logic
        if user_move == computer_move:
            return "Draw"
        half = len(self.moves) // 2
        user_move_index = self.moves.index(user_move)

        if computer_move in self.moves[user_move_index + 1:user_move_index + 1 + half]:
            return "user"
        else:
            return "computer"



class GameDriver:
    def __init__(self, moves):
        valid, message = MoveValidator.validate_moves(moves)
        if not valid:
            sys.exit(message)
        
        self.rule_engine = RuleEngine(moves)
        self.interface = GameInterface(moves)

    def start_game(self):
        key = CryptoManager.generate_key()
        computer_move = self.interface.moves[0]
        hmac_value = CryptoManager.generate_hmac(key, computer_move)

        self.interface.display_hmac(hmac_value)

        user_move = self.interface.display_menu()

        result = self.rule_engine.get_winner(computer_move, user_move)
        self.interface.display_results(user_move, computer_move, result)

        # Display the key after showing the result
        print(f"HMAC key: {key.hex()}")

if __name__ == "__main__":
    moves = sys.argv[1:]
    game = GameDriver(moves)
    game.start_game()
