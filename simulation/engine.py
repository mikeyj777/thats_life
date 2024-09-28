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
        self.agents = np.full(bounds, None, dtype=object)
        self.running = False
        self.params = params
        if self.params is None:
            self.params = Config.SIMULATION_PARAMS
        self.x = max(0, int(self.agents.shape[0] // 2))
        self.y = max(0, int(self.agents.shape[1] // 2))
        # self.x = 0
        # self.y = 0
        self.lock = threading.Lock()
        self.age_oldest_agent = -1

    def place_pattern(self, grid, pattern, x_offset=0, y_offset=0):
        for (x, y) in pattern:
            if isinstance(grid[x + x_offset, y + y_offset], Agent):
                continue
            grid[x + x_offset, y + y_offset] = Agent()
        
        return grid

    def initialize_agents_predefined_patters(self):
        # Example patterns
        glider = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        block = [(0, 0), (0, 1), (1, 0), (1, 1)]
        blinker = [(0, 1), (1, 1), (2, 1)]

        # Grid setup
        grid_size = 100
        grid = np.full((grid_size, grid_size), None, dtype=object)

        # Place patterns at different locations
        grid = self.place_pattern(grid, glider, x_offset=50, y_offset=50)
        # grid = self.place_pattern(grid, block, x_offset=10, y_offset=10)
        # grid = self.place_pattern(grid, blinker, x_offset=15, y_offset=15)

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
            
                
        apple = 1

    def update(self):
        agent: Agent
        with self.lock:
            living = 0
            agent_count = 0
            for i in range(self.agents.shape[0]):
                for j in range(self.agents.shape[1]):
                    agent = self.agents[i, j]
                    if agent is None:
                        # Check if a new Agent should be born here
                        neighbors = self.count_live_neighbors(i, j)
                        if neighbors == 3:
                            self.agents[i, j] = Agent()
                    else:
                        # Update existing Agent
                        neighbors = self.count_live_neighbors(i, j)
                        if neighbors < 2 or neighbors > 3:
                            agent.state = 'dead'
                            agent.age = 0
                        elif neighbors == 2 or neighbors == 3:
                            agent.state = 'alive'
                            agent.age += 1
                            living += 1
                            if agent.age > self.age_oldest_agent:
                                self.age_oldest_agent = agent.age
                            agent.set_color(self.age_oldest_agent)
                        agent_count += 1

    def count_live_neighbors(self, i, j):
        neighbors = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = (i + di) % self.agents.shape[0], (j + dj) % self.agents.shape[1]
                if isinstance(self.agents[ni, nj], Agent) and self.agents[ni, nj].state == 'alive':
                    neighbors += 1
        return neighbors

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
                    if agent is None:
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
