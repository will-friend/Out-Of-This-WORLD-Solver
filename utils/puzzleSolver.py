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
    used_tiles = [False] * grid_size**2
    
    pos = 0 

    def dfs_for_grid(pos):
        
        if pos == grid_size**2:
            return True
        
        i = pos // grid_size
        j = pos % grid_size

        res = False

        for card_idx in range(len(used_tiles)):
            
            if used_tiles[cardr_idx]:
                continue

            card = input_card[card_idx]
            rot = 0

            left_neighbor = ans[i][j-1] if j > 0 else [None]
            top_neighbor = ans[i-1][j] if i > 0 else [None] 

            while rot < 4:
                
                if is_valid(potential_neighbor=card, left_neighbor=left_neighbor, top_neighbor=top_neighbor):
                    ans[i][j] = card
                    used_tiles[card_idx] = True
                    res = dfs_for_grid(pos+1)
                    if res:
                        return res 
                    else:
                        ans[i][j] = None
                        used_tiles[card_idx] = False
                else:
                    card = rotate_card(card, 1)
                    rot += 1
        return res
    
    res = dfs_for_grid(pos)

    return ans

def plot_solution(arr: list[list[int]], encoding_dict: dict, title: str=None) -> None:

    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    
    rows = len(arr)
    cols = len(arr[0])

    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # --- Scale factor for diamond size ---
    scale = 0.6  # Smaller than 1 to reduce overlap

    # Plot each tile
    for i in range(rows):
        for j in range(cols):
            tile_data = arr[i][j]

            # Offset for tile center
            offset_x = j * 2
            offset_y = -i * 2

            # Draw tile boundary (optional)
            tile_box = Rectangle((offset_x - 1, offset_y - 1), 2, 2,
                                 linewidth=1.0, edgecolor='black', facecolor='none')
            ax.add_patch(tile_box)

            # Diamond vertex positions (scaled)
            diamond_vertices = [(scale * x, scale * y) for (x, y) in [(-1, 0), (0, 1), (1, 0), (0, -1)]]

            # Diamond outline
            diamond_path = diamond_vertices + [diamond_vertices[0]]
            diamond_x = [x + offset_x for x, y in diamond_path]
            diamond_y = [y + offset_y for x, y in diamond_path]
            ax.plot(diamond_x, diamond_y, 'k--')

            # Labels at vertices
            for k, (dx, dy) in enumerate(diamond_vertices):
                num = tile_data[k]
                label = encoding_dict.get(num, f"?{num}")
                ax.text(offset_x + dx, offset_y + dy, label,
                        ha='center', va='center', fontsize=8,  # Smaller font
                        bbox=dict(boxstyle="round,pad=0.2", edgecolor="black", facecolor="lightgray"))

            # Optional: dashed box around the diamond
            padding = scale * 1.2
            # box = Rectangle((offset_x - padding, offset_y - padding),
            #                 2 * padding, 2 * padding,
            #                 linewidth=1.0, edgecolor='blue', facecolor='none', linestyle='--')
            # ax.add_patch(box)

    # Adjust plot limits
    ax.set_xlim(-1, cols * 2 + 1)
    ax.set_ylim(-rows * 2 - 1, 1)
    ax.axis('off')
    if title is not None:
        plt.title(title)
    plt.show()


        

        


        

        


        


    
        



