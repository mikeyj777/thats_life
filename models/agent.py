# backend/models/agent.py
import numpy as np
import uuid
from config import Config

class Agent:
    def __init__(self, state='dead'):
        self.state = state
        self.id = str(uuid.uuid4())
        self.age = 0
        self.color = {'alive': (1.0, 1.0, 1.0), 'dead': (0.0, 0.0, 0.0)}
        self.height = 0.0
        self.set_color_and_height()

    def set_color_and_height(self, oldest_agent = 1):
        colors = Config.SIMULATION_PARAMS['colors']
        oldest_agent = max(1, oldest_agent)
        
        agent_color_phase = (len(colors) - 1) * self.age / oldest_agent
        color = colors[int(agent_color_phase)]
        color = np.array(color, dtype=float)
        color /= 255
        self.color = {
            'alive': color,
            'dead': (0, 0, 0)
        }
        self.height = self.age / oldest_agent  # Normalize height based on age