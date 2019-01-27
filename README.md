# ML_Snake
ML Snake Game

<h2>Description</h2>
<p>Rudimentary Reinforcement-learning Snake game. The snake's decision making is determined through a feedforward deep
neural network. At any given point, based on the position of all its body cells and position of food, 
the snake chooses between turning up, down, left, or right. Through a reward and punishment to its score,
the snake is incentivised to find food, avoid death, and to do so quickly. In any given learning iteration, 
when it eats food and length increases, the model's score increases. 
Score decreases incrementally with time and substantially with death. 
Searches are pruned when scores are too low. At the end of an iteration, if the iteration's score exceeds 
the previous best score, neural network parameters are slightly shifted randomly. </p>
