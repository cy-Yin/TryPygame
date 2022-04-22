## 1. 游戏设定
- 敌方共有大中小三款飞机，分为高中低三种速度
- 子弹射程并非全屏，大概为屏幕长度的 80%
- 消灭小飞机需要1发子弹，消灭中飞机需要8发子弹，消灭大飞机需要20发子弹
- 每消灭一架小、中、大飞机分别可以获得1000分、6000分和10000分
- 每30秒有一个随机的道具补给，分为两种道具，即全屏炸弹和双倍子弹
- 全屏炸弹最多只能存放3枚，双倍子弹可以维持18秒的效果
- 游戏将根据分数来逐步提高难度，难度的提高表现为飞机数量的增多以及速度的加快

注：

此外，还对游戏进行了一些改进：

为中飞机和大飞机增加了血槽的显示，这样玩家可以直观地知道敌机将在何时被消灭。

我方有3次机会，每次被敌人消灭的时候，新诞生的飞机会有3秒的无敌时间。

游戏结束之后会显示历史最高分数。

## 2. 关于源代码文件

代码模块如下：

- main.py —— 主模块
- myplane.py —— 定义我方飞机
- enemy.py —— 定义敌方飞机
- bullet.py —— 定义子弹
- supply.py —— 定义补给

资源文件如下：

- sound —— 声音、音效资源
- images —— 图片资源
- font —— 字体资源


## 3. 游戏操作
- W : 我方飞机上移
- S : 我方飞机下移
- A : 我方飞机左移
- D : 我方飞机右移
- SPACE : 使用全屏炸弹


--------------------------------- CONTENTS TRANSLATED ARE AS FOLLOWS ---------------------------------

### 1. Game Instruction
- The enemies totally have three types of planes: large, medium and small ones which have a high,medium and low speed respectively.
- The bullets cannot reach everywhere within in the interface, but about 80 percent of it.
- It takes 1 bullet to destroy one small plane, while 8 for a medium one and 20 for a large one. 
- Every small plane is worth 1000 points, with a medium one worth 6000 points and 10000 points for a large one.
- There is a random item supply every half a minute. You may receive a full-screen bomb or a chance to double the bullets to shoot out each second over a period of time.
- You are allowed to have at most 3 full-screen bombs in your inventory. The double-bullet effect lasts about 3 seconds.
- The difficulty of the game will be gradually increased according to the score you get, which means you wil meet an increasing number of the enemy planes which have a higher speed compared to the former ones.
  
Note:

What is more, some improvements have been made about this game:

The Health Point of a medium or large plane will be attached to the screen so that a gameplayer is able to directly know when an enemy plane will be destroyed.

A gameplayer has 3 opportunities to get a new-born plane invincible for 3 seconds during which enemies are not able to hit it after the former plane under our control has been destroyed.

The highest score in history will be displayed after the game ends.

### 2. About The Code

There are several code files as follows:

- main.py —— the main file
- myplane.py —— define planes under the player's control
- enemy.py —— define the enemy planes
- bullet.py —— define the bullets
- supply.py —— define the supply items

File folders containing the sources about game：

- sound
- images
- font

## 3. Game Operation
- W : move upward
- S : move downward
- A : move left
- D : move right
- SPACE : use the full-screen bomb
