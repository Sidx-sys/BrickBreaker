# DASS Asignment-2, Brick Breaker Game

## Starting Up The Game
- enter `python3 main.py` in the terminal to run the game
  
## Game Description
Its a fairly simple game where you have a paddle, a ball and bricks that can be broken by these balls. 
There are 4 different types of bricks in the game:
- Level 1 brick (*Green*) -> can be broken in 1 hit
- Level 2 brick (*Blue*) -> can be broken in 2 hits
- Level 3 brick (*Red*) -> can be broken in 3 hits
- Level 4 brick (*Pink*) -> are unbreakable and can be only broken by a **`thru-ball`**
- *Rainbow Brick* which changes is hardness until you hit it

On breaking a brick, there is a *50%* probability that you might get a powerup, which are abilities that can give you advantage/disadvantage in the game. There are 6 types of powerups in the game:

1. Expand Paddle -> The length of paddle increases from **7 => 11**
2. Shrink Paddle -> The length of paddle decreases from **7 => 4**
3. Grab Ball -> The ball **sticks to the paddle** upon contact
4. Multi Ball -> Every ball **divides into 2 more balls**
5. Fast Ball -> Ball speed **increases on average** upon contact with paddles
6. Thru Ball -> Ball can **go through any brick (including Unbreakable)** as if nothing was there
7. Laser Paddle -> Paddle equips **blasters which shoots lasers from its ends** to deal damage equivalent of a ball

Additionally, you have:
- There are 3 levels in the game currently
-  `3` Health points to complete the game, where on losing a health you start with no powers
-  Time taken to complete the game on the top-left part of screen
-  Score in the top-middle of the game frame
-  Upon losing 3 lives the game is over and you exit the game
-  **The game is in TIME_ATTACK mode**, i.e the bricks slowly fall down. If the bricks touch the paddle, the game ends
-  Boss Level (level-3), Defeat the Boss with **12 health**

### Some Features
- Inheritance is implemented by having parent classes for Blocks and Powerups
- Polymorphism is implemented in the Powerups module by having an `start_effect` function with different functionality in each subclass
- Encapsulation is done by using classes for implementation of various things
- Abstraction is handled as all the details are abstracted in different files and oly interface is being used in the `main.py` file


## Game Guide
A / Left-arrow key -> move the paddle left
D / Right-arow key -> move the paddle right
Space -> launch the ball

The game accomodates for all sorts of collisions and edge cases are handled to the best of my abilities.
