from mesa import Agent
import random


class EngineerAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        self.move()
        self.clear_debris()
        self.repair_infrastructure()
        self.build_shelter()

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def clear_debris(self):
        if self.pos in self.model.debris_locations:
            self.model.debris_locations.remove(self.pos)
            print(f"[EngineerAgent {self.unique_id}] cleared debris at {self.pos}")

    def repair_infrastructure(self):
        if random.random() < 0.05:
            print(f"[EngineerAgent {self.unique_id}] repaired infrastructure at {self.pos}")

    def build_shelter(self):
        if random.random() < 0.03:
            print(f"[EngineerAgent {self.unique_id}] built temporary shelter at {self.pos}")
