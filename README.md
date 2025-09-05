# Out-Of-This-WORLD-Solver

On what would've been any other regular day, I was introduced to *Professor McBrainy's Zany out of this WORLD* puzzle:

![Alt text](./images/IMG_0059.jpg)

This puzzle is an edge matching puzzle: given a set of n tiles, where $\sqrt{n}\in\mathbb{N}$, find an MxM grid ($M=\sqrt{n}$) such that for any tile in the grid, its edge matches the edge of its neighboring tiles. For McBrainy's puzzle, the tiles are square, but each edge has a symbol on it that we are to match to other tiles in the grid. There are eight different symbols, all planets or moons. We are given 16 tiles, and asked to find a 4x4 grid that meets the edge matching criteria.

Initially it seemed like a simple enough task, but after a little bit of trial and error it quickly became apparent that this was no simple task. When we sat down and worked out the combinatorics for the problem, we got that there were $16!*4^{15}$ possible 4x4 unique grids we could make, where the $16!$ factorial is just how many ways can you lay 16 tiles down on a 4x4 grid uniquely, and the $4^{15}$ comes from each tile being able to have four unique states since they can be rotated 90 degrees to provide a new state/configuration of edges. In reality the calculation should give $4^16$ but if we assume one solution configuration, much like the tiles, the 4x4 grid could be rotated such that it is a "new" solution, depending on how we index the grid, so we divide by four to account for that.

This quickly deflated the trial and error method. Luckily for me, though, I just started my masters studies of computer science. After reviewing some DSA, I noticed that *Depth First Search* (DFS) with pruning (or Backtesting with pruning depending on what you reference) are excellent for combinatorial problems, since we could map each state of the the problem in a seach space tree. Now, searching the $16!*4^{15}$ possible states (and really building them first and then seeing if the solution works) still seems like a lofty task. However, since we hav constraints to our problem, we can prume subtrees from our search space if the conditions are not met, and the earlier we find the ocndition not met, the more time we save (finding them early is not guaranteed but is just a fact of the method)!

The puzzle seemed like the perfect test of implementing a DFS+Pruning algorithm (and satisfy my need to get a solution). In the repository you will find a jupyter notebook `PuzzleNotebook.ipynb`, where I go in depth on the thought process for coming up with the proper implementation for a program to solve the problem, a walkthrough of the actual code, and a demonstration with a 2x2 sample to show it works as well as the grande finale of solving the great Professor McBrainy's edge matching puzzle. 

Under the `utils` folder is the python file that contains the actual functions talked about in the jupyter notebook. Under `images` are some stock images (like the one above) used to show the puzzle and the final solution mapped from what the solver produced. 

As I continue my studies of computer science, I will attempt to update this repo with either: a) more optimized solvers if possible, and b) implement in languages I am learning (next up will be Java!) to practice the implementation.

If you notice anything that could be improved or optimized, please let me know as I am always happy to learn how to become a better computer scientist!