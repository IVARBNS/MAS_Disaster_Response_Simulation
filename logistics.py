from mesa import Agent
import random
from medical import MedicalAidAgent


class LogisticsAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.supplies = 10

    def step(self):
        self.deliver_supplies()
        self.optimize_route()
        self.track_inventory()

    def deliver_supplies(self):
        neighbors = self.model.grid.get_cell_list_contents([self.pos])
        for agent in neighbors:
            if isinstance(agent, MedicalAidAgent) and self.supplies > 0:
                self.supplies -= 1
                agent.first_aid_kits += 1
                print(f"[LogisticsAgent {self.unique_id}] supplied MedicalAidAgent at {self.pos}, supplies left: {self.supplies}")
                break

    def optimize_route(self):
        new_position = (self.pos[0] + random.choice([-1, 0, 1]), self.pos[1] + random.choice([-1, 0, 1]))
        new_position = (new_position[0] % self.model.grid.width, new_position[1] % self.model.grid.height)
        self.model.grid.move_agent(self, new_position)
        print(f"[LogisticsAgent {self.unique_id}] moved to {self.pos}")

    def track_inventory(self):
        if self.supplies == 0:
            self.supplies = 10
            print(f"[LogisticsAgent {self.unique_id}] restocked supplies at {self.pos}")
