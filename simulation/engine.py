# simulation/engine.py

import time
import threading
import logging
from models.agent import Agent
import numpy as np
from config import Config

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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
        self.age_oldest_agent = 1

    def place_pattern(self, grid, pattern, x_offset=0, y_offset=0):
        for (x, y) in pattern:
            x = (x + x_offset) % self.bounds[0]
            y = (y + y_offset) % self.bounds[1]
            if grid[x, y] is None:
                grid[x, y] = Agent()
        # logging.debug(f"Placed pattern at offset ({x_offset}, {y_offset})")
        return grid

    def initialize_agents_predefined_patterns(self):
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
        with self.lock:
            new_agents = np.full(self.bounds, None, dtype=object)
            for i in range(self.bounds[0]):
                for j in range(self.bounds[1]):
                    neighbors = self.count_live_neighbors(i, j)
                    current_agent = self.agents[i, j]
                    
                    if current_agent is None:
                        if neighbors == 3:
                            new_agents[i, j] = Agent()
                    else:
                        new_agent = Agent()
                        new_agent.id = current_agent.id
                        new_agent.age = current_agent.age
                        
                        if 2 <= neighbors <= 3:
                            new_agent.state = 'alive'
                            new_agent.age += 1
                            if new_agent.age > self.age_oldest_agent:
                                self.age_oldest_agent = new_agent.age
                        else:
                            new_agent.state = 'dead'
                            new_agent.age = 0
                        
                        new_agent.set_color_and_height(self.age_oldest_agent)
                        new_agents[i, j] = new_agent

            self.agents = new_agents
        
        # logging.debug(f"Updated simulation. Oldest agent age: {self.age_oldest_agent}")

    def count_live_neighbors(self, i, j):
        neighbors = 0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = (i + di) % self.bounds[0], (j + dj) % self.bounds[1]
                if isinstance(self.agents[ni, nj], Agent) and self.agents[ni, nj].state == 'alive':
                    neighbors += 1
        return neighbors

    def get_state(self):
        with self.lock:
            state = [
                {
                    'id': agent.id,
                    'position': [i, j],
                    'state': agent.state,
                    'color': agent.color,
                    'height': agent.height
                }
                for i in range(self.bounds[0])
                for j in range(self.bounds[1])
                if (agent := self.agents[i, j]) is not None
            ]
            # logging.debug(f"Got state. Total agents: {len(state)}")
            return state

    def run(self, update_interval=0.1):
        self.running = True
        while self.running:
            self.update()
            # time.sleep(update_interval)

    def stop(self):
        self.running = False
        logging.info("Simulation stopped")