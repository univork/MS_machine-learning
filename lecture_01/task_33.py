"""ააგეთ ე.წ. ნოლიკი-იქსიკი (კონსოლში)."""

class TicTacToe:
    board = ["-" for _ in range(9)]
    positions = {"X": [], "O": []}

    def print_message(self, message: str) -> None:
        print("-" * len(message))
        print(message)
        print("-" * len(message))

    def display_board(self):
        print("\n")
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self.board[0], self.board[1], self.board[2]))
        print('\t_____|_____|_____')
    
        print("\t     |     |")
        print("\t  {}  |  {}  |  {}".format(self.board[3], self.board[4], self.board[5]))
        print('\t_____|_____|_____')
    
        print("\t     |     |")
    
        print("\t  {}  |  {}  |  {}".format(self.board[6], self.board[7], self.board[8]))
        print("\t     |     |")
        print("\n")

    def get_move(self, player: str) -> int:
        try:
            move = int(input(f"Enter number of box for {player}: "))
        except ValueError as ex:
            self.print_message("Input must be a number!")
            raise ex
        
        if move > 9 or move < 0:
            self.print_message("Number must be in [0, 9] range!")
            raise ValueError
        
        if self.board[move - 1] != "-":
            self.print_message("Box already occypied!")
            raise ValueError

        return move
    
    def check_win(self, player: str) -> bool:
        winners = [[0, 1, 2] , [3, 4, 5], [6, 7, 8], [0, 3, 6], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for x in winners:
            if set(x).issubset(set(self.positions[player])):
                return True
        return False
    
    def swap_player(player: str) -> str:
        if player == "X":
            return "O"
        return "X"

    def play(self) -> None:
        self.display_board()

        curr_player = "X"
        game_over = False 
        while not game_over:
            try:
                move = self.get_move(curr_player)
            except ValueError:
                continue

            self.board[move - 1] = curr_player
            self.positions[curr_player].append(move - 1)
                
            self.display_board()

            if self.check_win(curr_player):
                self.print_message("Player " + curr_player + " won!")
                game_over = True
            elif len(self.positions["X"]) + len(self.positions["O"]) == 9:
                self.print_message("Draw!")
                game_over = True
            else: 
                curr_player = self.swap_player(curr_player)
            

if __name__ == "__main__":
    TicTacToe().play()
