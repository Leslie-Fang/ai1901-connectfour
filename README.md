## Introduction
https://github.com/rmit-s3664000-cameron-sugiada/ai1901-connectfour.git
Based on this repo, we add new stragety with RL(Reinforcement Learning)
强化学习(Reinforcement Learning) 在conect4 棋上的应用

## Setup
The code was written in **Python 3.6**. 
```
pip install pipenv
pipenv install --skip-lock --dev
pipenv install
pipenv shell
```

## Running
The currently available player types are:

* `HumanPlayer` - Player is controlled by user via GUI **[DEFAULT OPTION]**
* `RandomAgent` - Player is controlled by computer and just chooses random valid columns to place token
* `MonteCarloAgent` - Player is controlled by computer and uses [Monte Carlo Tree Search](!https://blog.csdn.net/u014397729/article/details/27366363) to find a good move
著名围棋Ai Alpha Go，核心的地方在于在突破传统的蒙特卡洛搜索树，采用预先训练好的【价值评估网络】和【走子网络】两个神经网络来评估，缩小了每层的搜索量，并且配以Google的TPU，实现超越人类棋手。

* `StudentAgent` - Currently, is a kind of stragety which we implemented
* `RLAgent` - Currently, is a the implementation of our RL algorithm(minmax). Alpha-beta剪枝算法是minmax算法的升级版本，减小运算量

### Human VS Human
```
python -m connectfour.game --player-one HumanPlayer --player-two HumanPlayer
```

### Robot VS Human
```
python -m connectfour.game --player-one RLAgent --player-two HumanPlayer
```

### No GUI
```
python -m connectfour.game --player-one MonteCarloAgent --player-two StudentAgent --no-graphics --fast --auto-close
```
