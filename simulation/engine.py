# backend/simulation/engine.py

import time
import threading
from models.agent import Agent
import numpy as np
import random
from config import Config

class SimulationEngine:
    def __init__(self, bounds=(800, 800), params=None):
        self.bounds = bounds
        self.agents = np.zeros(bounds, dtype=Agent)
        self.running = False
        self.params = params
        if self.params is None:
            self.params = Config.SIMULATION_PARAMS
        self.x = max(0, int(self.agents.shape[0] // 2))
        self.y = max(0, int(self.agents.shape[1] // 2))
        # self.x = 0
        # self.y = 0
        self.lock = threading.Lock()

    def place_pattern(self, grid, pattern, x_offset=0, y_offset=0):
        for (x, y) in pattern:
            grid[x + x_offset, y + y_offset] = 1
        
        return grid

    def initialize_agents_predefined_patters(self):
        # Example patterns
        glider = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        block = [(0, 0), (0, 1), (1, 0), (1, 1)]
        blinker = [(0, 1), (1, 1), (2, 1)]

        # Grid setup
        grid_size = 20
        grid = np.zeros((grid_size, grid_size), dtype=int)

        # Place patterns at different locations
        grid = self.place_pattern(grid, glider, x_offset=5, y_offset=5)
        grid = self.place_pattern(grid, block, x_offset=10, y_offset=10)
        grid = self.place_pattern(grid, blinker, x_offset=15, y_offset=15)

        self.agents[0:grid.shape[0], 0:grid.shape[1]] = grid

    def initialize_agents(self, num_agents=4):
        i = 0
        x = self.x
        y = self.y
        while i < num_agents:
            i += 1
            increment = 1
            if i % 4 == 1 and i >= 5:
                increment += 1
            if i % 4 == 0:
                x += increment
            if i % 4 == 1:
                y += increment
            if i % 4 == 2:
                x -= increment
            if i % 4 == 3:
                y -= increment

            if x >= self.agents.shape[0]:
                x = 0
            if y >= self.agents.shape[1]:
                y = 0
            if x < 0:
                x = self.agents.shape[0] - 1
            if y < 0:
                y = self.agents.shape[1] - 1
            if isinstance(self.agents[x, y], Agent):
                continue
            self.agents[x, y] = Agent()
            print(x, y)
            
                
        apple = 1

    def update(self):
        agent:Agent
        with self.lock:
            living = 0
            agent_count = 0
            i = self.x
            j = self.y
            first_pass = True
            while i < self.agents.shape[0]:
                while j < self.agents.shape[1]:
                
                    agent = self.agents[i, j]
                    # from https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
                        
                    i_min = i
                    j_min = j
                    if i > 0:
                        i_min = i - 1
                    if j > 0:
                        j_min = j - 1

                    i_max = i
                    j_max = j
                    if i < self.agents.shape[0] - 1:
                        i_max = i + 1
                    if j < self.agents.shape[1] - 1:
                        j_max = j + 1
                    
                    i_tests = [i_min, i, i_max]
                    j_tests = [j_min, j, j_max]

                    neighbors = 0
                    for i_test in i_tests:
                        for j_test in j_tests:
                            if i_test == i and j_test == j:
                                continue
                            if isinstance(self.agents[i_test, j_test], Agent):
                                if self.agents[i_test, j_test].state == 'alive':
                                    neighbors += 1
                    # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                    # Any live cell with more than three live neighbours dies, as if by overpopulation.
                    # Any live cell with two or three live neighbours lives on to the next generation.
                    if neighbors < 2 or neighbors > 3:
                        if isinstance(agent, Agent):
                            self.agents[i, j].state = 'dead'
                        
                    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                    if neighbors == 3:
                        if isinstance(agent, int):
                            self.agents[i, j] = Agent()
                        self.agents[i, j].state = 'alive'
                    
                    
                    if isinstance(agent, Agent):
                        agent_count += 1
                        if agent.state == 'alive':
                            living += 1
                    
                    j += 1
                    
                j = 0
                i += 1
                if i >= self.agents.shape[0] and first_pass:
                    i = 0
                    first_pass = False
            # print(f'living: {living} of {agent_count}')

    def get_state(self):
        agent:Agent
        with self.lock:
            # return {
            #     'agents': self.agents
            # }

            # the statement below returns a list of dictionaries based on the agent properties.  this works well with a web application that can't 
            # jsonify a custom class.
            ans = []
            for i in range(self.agents.shape[0]):
                for j in range(self.agents.shape[1]):
                    agent = self.agents[i, j]
                    if isinstance(agent, int):
                        continue
                    ans.append({
                        'id': agent.id,
                        'position': [i, j],
                        'state': agent.state,
                        'color': agent.color,
                    })
            return ans

    def run(self, update_interval=0.1):
        self.running = True
        while self.running:
            self.update()
            # time.sleep(update_interval)

    def stop(self):
        self.running = False
