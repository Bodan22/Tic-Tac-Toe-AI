import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        # Initialize the main window
        self.master = master
        self.master.title("Tic-Tac-Toe")
        
        # Initialize the game board as a list of 9 empty spaces
        self.board = [' ' for _ in range(9)]
        
        # Create a list to store the button objects
        self.buttons = []

        # Create the 3x3 grid of buttons
        for i in range(3):
            for j in range(3):
                # Create a button and bind it to the player_move function
                button = tk.Button(master, text=' ', font=('Arial', 20), width=5, height=2,
                                   command=lambda row=i, col=j: self.player_move(row, col))
                button.grid(row=i, column=j)
                self.buttons.append(button)

    def player_move(self, row, col):
        # Convert 2D coordinates to 1D index
        index = 3 * row + col
        
        # Check if the selected cell is empty
        if self.board[index] == ' ':
            # Update the board and button text
            self.board[index] = 'X'
            self.buttons[index].config(text='X', state='disabled')
            
            # Check for win or tie
            if self.check_win('X'):
                self.end_game("You win!")
            elif self.is_full():
                self.end_game("It's a tie!")
            else:
                # If game hasn't ended, AI makes a move
                self.ai_move()

    def ai_move(self):
        # Get the best move for AI using minimax
        best_move = self.get_best_move()
        
        # Update the board and button text
        self.board[best_move] = 'O'
        self.buttons[best_move].config(text='O', state='disabled')
        
        # Check for win or tie
        if self.check_win('O'):
            self.end_game("AI wins!")
        elif self.is_full():
            self.end_game("It's a tie!")

    def check_win(self, player):
        # Define all possible winning combinations
        win_states = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        # Check if any winning combination is satisfied
        return any(all(self.board[i] == player for i in state) for state in win_states)

    def is_full(self):
        # Check if there are no empty spaces left on the board
        return ' ' not in self.board

    def get_available_moves(self):
        # Return a list of indices of empty cells
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def minimax(self, depth, is_maximizing):
        # Base cases: check for terminal states
        if self.check_win('O'):
            return 1  # AI wins
        if self.check_win('X'):
            return -1  # Player wins
        if self.is_full():
            return 0  # Tie game
        
        if is_maximizing:
            # Maximizing player (AI)
            best_score = float('-inf')
            for move in self.get_available_moves():
                self.board[move] = 'O'
                score = self.minimax(depth + 1, False)
                self.board[move] = ' '  # Undo the move
                best_score = max(score, best_score)
            return best_score
        else:
            # Minimizing player (Human)
            best_score = float('inf')
            for move in self.get_available_moves():
                self.board[move] = 'X'
                score = self.minimax(depth + 1, True)
                self.board[move] = ' '  # Undo the move
                best_score = min(score, best_score)
            return best_score

    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        # Try all possible moves and choose the one with the highest score
        for move in self.get_available_moves():
            self.board[move] = 'O'
            score = self.minimax(0, False)
            self.board[move] = ' '  # Undo the move
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def end_game(self, message):
        # Disable all buttons and show game over message
        for button in self.buttons:
            button.config(state='disabled')
        messagebox.showinfo("Game Over", message)

def main():
    # Create the main window and start the game
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()