# Puzzle Room

## Description

As you delve deeper into the tomb in search of answers, you stumble upon a puzzle room, its floor entirely covered in pressure plates. The warnings of the great necromancer, who hid his treasure here, suggest that one wrong step could lead to your doom.

You enter from the center of the eastern wall. Although you suspect you’re missing a crucial clue to guide your steps, you’re confident that everything you need to safely navigate the traps is already within reach.

At the center of the room lies the key to venturing further into the tomb, along with the promise of powerful treasures to aid you on your quest. Can you find the path, avoid the traps, and claim the treasure (flag) on the central platform?

Author: Christopher Roberts (caffix)

## Files

* [puzzle_room.py](puzzle_room.py)

## Solution

* [solve.py](solve.py)

The goal is to discover the correct path to the central shrine, ensuring that none of the puzzle's constraints are violated. While there are many valid paths through the room, only one specific route is correct. The key detail is that the words encountered along this correct path form a decryption key needed to decrypt the flag.

Since we can't determine the correct path in advance, we need to explore all possible routes. Fortunately, the challenge code is structured in a way that makes implementing a search algorithm straightforward, with only minimal adjustments. It almost seems like the challenge was designed for this approach 🤔.

Flag: `pctf{Did_you_guess_it_or_apply_graph_algorithms?}`
