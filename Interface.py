import time, random
from TicTacToe import GameState, Move

SPIN = ["-", "\\", "|", "/"]
enable = 1

def set_enable_animations(n: int) -> None:
    global enable
    enable = n

def confirm(msg: str) -> bool:
    res = input("\n" + msg + " (Y/n) > ")
    if res == 'Y' or res == 'y' or res == 'yes' or res == 'Yes':
        return True
    return False

def input_number(msg: str) -> int:
    while True:
        res = input("\n" + msg + " > ")
        try:
            n = int(res)
            return n
        except:
            print("Invalid entry! ", end="")
            pass

def get_valid_human_move(game: GameState, dev: bool=False) -> int:
    print(("\n"
        " {0} | {1} | {2} \n" +
        "-----|-----|-----\n" +
        " {3} | {4} | {5} \n" +
        "-----|-----|-----\n" +
        " {6} | {7} | {8} \n" ).format(
            *[["(O)", f" {ndx} ", "[X]"][v + 1] for ndx, 
                v in enumerate(game.board)])
        + (f"\n[{game.to_integer()}]\n" if dev else "")
    )
    print("Your turn! ", end="")
    while True:
        pos = input("{0} Choose a move > ".format(
            "[X]" if game.next_player == 1 else "(O)"
        ))
        try:
            n = int(pos)
            if game.board[n] == 0:
                return Move(n, game.next_player)
            print("Space is already taken! ", end="")
        except:
            print("Invalid entry! ", end="")
            pass

def think(duration: int):
    d = 0
    while d < duration:
        for _ in range(0, 4):
            print(".", end="", flush=True)
            time.sleep(0.05 * enable)
        time.sleep(0.05 * enable)
        print("\b\b\b\b", end="", flush=True)
        time.sleep(0.25 * enable)
        d += 0.5

def dot_dot_dot(count: int):
    d = 0
    while d < count:
        print(".", end="", flush=True)
        time.sleep(0.5 * enable)
        d += 0.5

def spin(duration: int):
    d = 0     
    index = 0                              
    while d < duration:                                     
        d += 0.05       
        print(SPIN[index % 4], end="", flush=True)
        time.sleep(0.05 * enable)
        index += 1
        print("\b", end="")   

def multi_spin(duration: int, size: int):
    d = 0     
    index = 0                              
    while d < duration:                                     
        d += 0.05       
        print(SPIN[index % 4] * size, end="", flush=True)
        time.sleep(0.05 * enable)
        index += 1
        print("\b" * size, end="")     

def cool_type(msg: str, speed: int):
    index = 0
    while index < len(msg):
        print(msg[index], end="", flush=True)
        time.sleep(random.randint(5, 80) / speed * enable)
        index += 1
