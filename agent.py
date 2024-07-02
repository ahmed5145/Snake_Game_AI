import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point
from model import Linear_QNet, QTrainer
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from IPython import display

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.head
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        state = [
            # Danger straight
            (game.direction == Direction.RIGHT and game.is_collision(point_r)) or
            (game.direction == Direction.LEFT and game.is_collision(point_l)) or
            (game.direction == Direction.UP and game.is_collision(point_u)) or
            (game.direction == Direction.DOWN and game.is_collision(point_d)),

            # Danger right
            (game.direction == Direction.UP and game.is_collision(point_r)) or
            (game.direction == Direction.DOWN and game.is_collision(point_l)) or
            (game.direction == Direction.LEFT and game.is_collision(point_u)) or
            (game.direction == Direction.RIGHT and game.is_collision(point_d)),

            # Danger left
            (game.direction == Direction.DOWN and game.is_collision(point_r)) or
            (game.direction == Direction.UP and game.is_collision(point_l)) or
            (game.direction == Direction.RIGHT and game.is_collision(point_u)) or
            (game.direction == Direction.LEFT and game.is_collision(point_d)),

            # Move direction
            game.direction == Direction.LEFT.value,
            game.direction == Direction.RIGHT.value,
            game.direction == Direction.UP.value,
            game.direction == Direction.DOWN.value,

            # Food location
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train(self):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        record = 0
        game = SnakeGameAI()

        plt.ion()  # Turn on interactive mode

        while True:
            state_old = self.get_state(game)
            final_move = self.get_action(state_old)

            reward, done, score = game.play_step(final_move)
            state_new = self.get_state(game)

            self.train_short_memory(state_old, final_move, reward, state_new, done)
            self.remember(state_old, final_move, reward, state_new, done)

            if done:
                game.reset()
                self.n_games += 1
                self.train_long_memory()

                if score > record:
                    record = score
                    self.model.save()

                print('Game:', self.n_games, 'Score:', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / self.n_games
                plot_mean_scores.append(mean_score)

                # Update plot in real-time
                self.plot_progress(plot_scores, plot_mean_scores)

                # Exit training if necessary (for testing purposes)
                #if self.n_games >= 100:  # Adjust as needed
                    #break

    def plot_progress(self, plot_scores, plot_mean_scores):
        plt.clf()
        plt.title('Snake Game AI Training Progress', fontsize=16, fontweight='bold')
        plt.xlabel('Number of Games', fontsize=14)
        plt.ylabel('Score', fontsize=14)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)

        plt.plot(plot_scores, label='Score', color='blue', linestyle='-', marker='o', markersize=4)
        plt.plot(plot_mean_scores, label='Mean Score', color='green', linestyle='-', marker='x', markersize=4)

        plt.legend(loc='upper left', fontsize=12)
        plt.ylim(ymin=0)

        plt.text(len(plot_scores)-1, plot_scores[-1], str(plot_scores[-1]))
        plt.text(len(plot_mean_scores)-1, plot_mean_scores[-1], str(plot_mean_scores[-1]))

        display.clear_output(wait=True)
        display.display(plt.gcf())

        plt.pause(0.1)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

if __name__ == '__main__':
    agent = Agent()
    agent.train()
