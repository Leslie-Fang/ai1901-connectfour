## Introduction
conect4 游戏规则：
在6行7列的棋盘上轮流下棋，可以选择任意空的位置下棋，但是如果选择的位置下方是空的，下在该位置上的棋子会下落到底部。
最先在横向，竖向以及对角方向连出4个棋子的一方获胜。

Based on this repo, we add new stragety with RL(Reinforcement Learning)

git clone https://github.com/rmit-s3664000-cameron-sugiada/ai1901-connectfour.git

强化学习(Reinforcement Learning) 在conect4 棋上的应用实现参考了这个[博客](https://roadtolarissa.com/connect-4-ai-how-it-works/) 

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
* `MonteCarloAgent` - Player is controlled by computer and uses [Monte Carlo Tree Search](https://blog.csdn.net/u014397729/article/details/27366363) to find a good move
著名围棋Ai Alpha Go，核心的地方在于在突破传统的蒙特卡洛搜索树，采用预先训练好的【价值评估网络】和【走子网络】两个神经网络来评估，缩小了每层的搜索量，并且配以Google的TPU，实现超越人类棋手。

* `StudentAgent` - Currently, is a kind of stragety which we implemented
* `RLAgent` - Currently, is a the implementation of our RL algorithm(minmax). Alpha-beta剪枝算法是minmax算法的升级版本，减小运算量

### Human VS Human
```
python -m connectfour.game --player-one HumanPlayer --player-two HumanPlayer
```

### Robot VS Human
```
python -m connectfour.game --player-one HumanPlayer --player-two RLAgent
```
大部分情况下，我已经下不过它了

### No GUI
```
python -m connectfour.game --player-one MonteCarloAgent --player-two StudentAgent --no-graphics --fast --auto-close
```

### Calculate Win rate
```
python runtest.py
```
Raw RL method VS MonteCarloAgent: 99% (most times is 100%)

