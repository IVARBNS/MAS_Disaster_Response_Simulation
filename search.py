from mesa import Agent
import random


class SearchRescueAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.found_victim = False

    def step(self):
        self.patrol()
        self.search_for_victims()
        self.communicate_victims()
        print(f"\n\n[SearchRescueAgent {self.unique_id}] patrolling at {self.pos}, found victim: {self.found_victim}")

    def patrol(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def search_for_victims(self):
        if random.random() < 0.1:
            self.found_victim = True
            if self.pos not in self.model.reported_victims:
                self.model.reported_victims.append(self.pos)

    def communicate_victims(self):
        if self.found_victim:
            self.model.broadcast_victim_location(self.pos)
