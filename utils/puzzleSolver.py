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

def get_all_rotations(cards: list[list[int]]) -> tuple[tuple[int]]:
    '''
    `get_all_rotations`: Given a list of square card encodings, for each card, get the four rotation state representations and append them to a list. The output is a tuple containing tuples for each card containing tuples of the rotated encodings. Rotations are done clockwise by 90 degrees

    Inputs
    ------
    `cards : list[list[int]]`
    - list of all card encodings to calculate rotations for
    
    Returns
    -------
    `cards_all_rot : tuple[tuple[tuple[int]]]`
    - input card rotated n times 90 degrees clockwise
    '''
    
    cards_all_rots = []
    for card in cards:
        rots = [tuple(card)]
        for _ in range(3):
            rots.append(tuple(card[-1:] + card[:-1]))
        
        cards_all_rots.append(tuple(rots))
        
    return tuple(cards_all_rots)
            
def is_valid(potential_neighbor: tuple[int], left_neighbor: tuple[int]=[None], top_neighbor: tuple[int]=tuple[None]) -> bool:
    '''
    `is_valid`: Checks if `potential_neighbor` is a valid neighbor of 'left_neighbor` and `top_neighbor` by checking if connected edges share the same value.
    Returns `True` if so, otherwise it returns `False`

    Inputs
    ------
    `potential_neighbor : tuple[int]`
    - Card we are testing as a potential solution for the tile position $(i,j)$
    
    `left_neighbor : tuple[int]`
    - The card at position $(i,j-1)$ relative to the `potential_neighor`
    
    `top_neighbor : tuple[int]`
    - The card at position $(i-1,j)$ relative to the `potential_neighor`

    Returns
    -------
    `bool`
    - `True` if `potential_neighbor` has matching left and top edges to the right and bottom edges of `left_neighbor` and `top_neighbor`, respectively. If no top or left neighbor is present we consider the condition for that neighbor met.
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
    '''
    `solve_puzzle`: Given a list of `input_cards`, where each entry in the list is a list encoding a 4-side tile with symbols from left, top, right, bottom, and a `grid_size` for the final MxM solution, use DFS with pruning to find a grid where al tiles have matching edges.
    
    Inputs
    ------
    `input_cards : list[list[int]]`
    - List of input tiles, with encoded values representing the symbol on each edge
    
    `grid_size : int`
    - An integer representing the side length of the the MxM grid that we want to solve for.
    
    Returns
    -------
    `ans : list[list[int]]`
    - MxM array representing the solved state of the puzzle. All entries are `None` if no solution was found. 
    '''
    
    ans = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    all_rots = get_all_rotations(input_cards)
    used_tiles = [False] * grid_size**2
    
    pos = 0 

    def dfs_for_grid(pos: int) -> bool:
        '''
        `dfs_for_grid`: Given a position index, find a valid tile in the edge-matching puzzle for teh current position using a Depth First Search implementation with pruning. Recursively search for more solutions when one is found for the current `pos` input. The position in the grid we are trying to fill is colculated by doing the integer division between the grid size of our solution for the row values, and the modulo with the grid size of our solution, with respectto `pos`
        
        Inputs
        ------
        `pos : int`
        - Integer representing the current number tile position we are trying to find a solution for. Used to calculate the row, column values we are at.
        
        Returns
        -------
        `res : bool`
        - Returns `True` if we have found a solution, otherwise returns `False`
        '''
        if pos == grid_size**2:
            return True
        
        i = pos // grid_size
        j = pos % grid_size

        res = False

        for card_idx in range(len(used_tiles)):
            
            if used_tiles[card_idx]:
                continue

            rotations = all_rots[card_idx]

            left_neighbor = ans[i][j-1] if j > 0 else [None]
            top_neighbor = ans[i-1][j] if i > 0 else [None]

            for rot in range(4):
                card = rotations[rot]
                
                if is_valid(potential_neighbor=card, left_neighbor=left_neighbor, top_neighbor=top_neighbor):
                    ans[i][j] = card
                    used_tiles[card_idx] = True
                    res = dfs_for_grid(pos+1)
                    if res:
                        return res 
                    else:
                        ans[i][j] = None
                        used_tiles[card_idx] = False
        return res
    
    res = dfs_for_grid(pos)

    return ans

def plot_solution(arr: list[list[int]], encoding_dict: dict, title: str=None) -> None:
    '''
    `plot_solutions`: given a solution space for the MxM edge matching puzzle, and an encoding dictionary mapping number to symbol, visualize the grid with the edges of each tile.
    
    Inputs
    ------
    `arr : list[list[int]]`
    - Solved grid to the matching-edge puzzle
    
    `encoding_dict : dict`
    - Dictionary mapping the values in teh solution array to symbols to visualize puzzle edges.
    
    Returns
    -------
    `None`
    '''
    
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    
    rows = len(arr)
    cols = len(arr[0])

    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    scale = 0.6

    for i in range(rows):
        for j in range(cols):
            tile_data = arr[i][j]

            offset_x = j * 2
            offset_y = -i * 2

            tile_box = Rectangle((offset_x - 1, offset_y - 1), 2, 2,
                                 linewidth=1.0, edgecolor='black', facecolor='none')
            ax.add_patch(tile_box)

            diamond_vertices = [(scale * x, scale * y) for (x, y) in [(-1, 0), (0, 1), (1, 0), (0, -1)]]

            diamond_path = diamond_vertices + [diamond_vertices[0]]
            diamond_x = [x + offset_x for x, y in diamond_path]
            diamond_y = [y + offset_y for x, y in diamond_path]
            ax.plot(diamond_x, diamond_y, 'k--')

            for k, (dx, dy) in enumerate(diamond_vertices):
                num = tile_data[k]
                label = encoding_dict.get(num, f"?{num}")
                ax.text(offset_x + dx, offset_y + dy, label,
                        ha='center', va='center', fontsize=8,  # Smaller font
                        bbox=dict(boxstyle="round,pad=0.2", edgecolor="black", facecolor="lightgray"))

    ax.set_xlim(-1, cols * 2 + 1)
    ax.set_ylim(-rows * 2 - 1, 1)
    ax.axis('off')
    if title is not None:
        plt.title(title)
    plt.show()


        

        


        

        


        


    
        



