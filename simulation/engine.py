# simulation/engine.py

import numpy as np
from config import Config
from models.agent import Agent
import threading

class SimulationEngine:
    def __init__(self):
        self.width, self.height = Config.SIMULATION_PARAMS['resolution']
        self.agents = np.empty((self.width, self.height), dtype=object)
        self.x = 0
        self.y = 0
        self.lock = threading.Lock()
        self.max_age = -1
        self.initialize_agents()

    def initialize_agents(self):
        for i in range(self.width):
            for j in range(self.height):
                if np.random.random() < 0.2:  # 20% chance of being alive initially
                    self.agents[i, j] = Agent(state='alive')
                else:
                    self.agents[i, j] = None

    def update(self):
        with self.lock:
            living = 0
            agent_count = 0
            i = 0
            j = 0
            while i < self.agents.shape[0]:
                while j < self.agents.shape[1]:
                    agent = self.agents[i, j]
                    
                    i_min = max(i - 1, 0)
                    j_min = max(j - 1, 0)
                    i_max = min(i + 1, self.agents.shape[0] - 1)
                    j_max = min(j + 1, self.agents.shape[1] - 1)
                    
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
                    
                    if neighbors < 2 or neighbors > 3:
                        if isinstance(agent, Agent):
                            agent.state = 'dead'
                            agent.age = 0
                    elif neighbors == 3 or (isinstance(agent, Agent) and agent.state == 'alive'):
                        if not isinstance(agent, Agent):
                            self.agents[i, j] = Agent()
                        self.agents[i, j].state = 'alive'
                        if isinstance(agent, Agent) and agent.state == 'alive':
                            agent.age += 1
                            if agent.age > self.max_age:
                                self.max_age = agent.age
                                print(f'max age: {self.max_age} | agent count: {agent_count} | living: {living}')
                                agent.set_color_and_height(self.max_age)
                    
                    if isinstance(agent, Agent):
                        agent_count += 1
                        if agent.state == 'alive':
                            living += 1
                    
                    j += 1
                    
                j = 0
                i += 1
                if i >= self.agents.shape[0]:
                    i = 0
            

    def update_agent_colors(self):
        max_age = max((agent.age for agent in self.agents.flat if isinstance(agent, Agent) and agent.state == 'alive'), default=1)
        for agent in self.agents.flat:
            if isinstance(agent, Agent) and agent.state == 'alive':
                agent.set_color_and_height(max_age)

    def get_agent(self, i, j):
        return self.agents[i, j]

    def is_alive(self, i, j):
        return isinstance(self.agents[i, j], Agent) and self.agents[i, j].state == 'alive'