def rotate_card(card: list[int], n: int=1) -> list[int]:
    '''
    `rotate_card`: Given input card, where a card is defined a square with a symbol on each edge, encoded with a list with `int`
    values corresponding to each kind of symbol in left-top-right-bottom edge order, return the card rotated 90 degrees
    clockwise.

    Inputs
    ------
    `card : list[int]`
    - list of values mappable to defined symbols in order of left-top-right-bottom of square card
    
    `n : int`
    - number of times to rotate card clockwise. we take modulo with respect to n to ensure we don't
    repeat rotations
    Returns
    -------
    `card : list[int]`
    - input card rotated n times 90 degrees clockwise
    '''
    if n%4 == 0:
        return card
    for _ in range(n%4):
        card = card[-1:] + card[:-1]
    
    return card

def is_valid(potential_neighbor: list[int], left_neighbor: list[int]=[None], top_neighbor: list[int]=[None]) -> bool:
    '''
    `is_valid`: Checks if `card2_edge` is a valid neighbor of `card1_edge` by checking if connected edge share the same value.
    Returns `True` if so, otherwise it returns `False`

    Inputs
    ------
    `card1_edge : list[int]`
    - Card edge, already determined to be valid, we wish to compare `card2_edge` against
    
    `card2_edge : list[int]`
    - Card edge from card we are testing as possible neighbor to `card1_edge`

    Returns
    -------
    `bool`
    - `True` if `card2_edge` is a valid neighbor to `card1_edge`, otherwise returns `False`
    '''
    if left_neighbor[0] is None and top_neighbor[0] is None:
        return True
    elif left_neighbor[0] is None:
        return potential_neighbor[1] == top_neighbor[3]
    elif top_neighbor[0] is None:
        return potential_neighbor[0] == left_neighbor[2]
    else:
        return (potential_neighbor[0] == left_neighbor[2]) and (potential_neighbor[1] == top_neighbor[3])


def solve_puzzle(input_cards: list[list[int]], grid_size: int) -> list[list[int]]:
    
    ans = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    unused_tiles = {i: input_cards[i] for i in range(len(input_cards))}
    used_tiles = set()
    
    pos = 0 

    def dfs_for_grid(pos):
        
        if len(used_tiles) == grid_size**2:
            return True
        
        i = pos // grid_size
        j = pos % grid_size

        rot = 0
        card_idx = 0

        res = False

        for card_idx in list(unused_tiles.keys()):

            card = unused_tiles[card_idx]
            rot = 0

            left_neighbor = ans[i][j-1] if j > 0 else [None]
            top_neighbor = ans[i-1][j] if i > 0 else [None] 

            while rot < 4:
                
                if is_valid(potential_neighbor=card, left_neighbor=left_neighbor, top_neighbor=top_neighbor):
                    ans[i][j] = card
                    used_tiles.add(card_idx)
                    unused_tiles.pop(card_idx)
                    res = dfs_for_grid(pos+1)
                    if res:
                        return res 
                    else:
                        ans[i][j] = None
                        unused_tiles[card_idx] = rotate_card(card, 4-rot)
                        used_tiles.remove(card_idx)
                else:
                    card = rotate_card(card, 1)
                    rot += 1
        return res
    
    res = dfs_for_grid(pos)

    return ans

    


        

        


        

        


        


    
        



