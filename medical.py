from mesa import Agent
import random


class MedicalAidAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.first_aid_kits = 3

    def step(self):
        self.coordinate_with_rescue()
        self.deliver_first_aid()
        self.setup_field_hospital()

    def coordinate_with_rescue(self):
        print(f"[MedicalAidAgent {self.unique_id}] coordinating at {self.pos}")

    def deliver_first_aid(self):
        if self.model.reported_victims:
            target = random.choice(self.model.reported_victims)
            new_pos = self.model.get_closer_position(self.pos, target)
            self.model.grid.move_agent(self, new_pos)
            print(f"[MedicalAidAgent {self.unique_id}] heading to {target}, now at {self.pos}")
            if self.pos == target:
                if self.first_aid_kits > 0:
                    self.first_aid_kits -= 1
                    self.model.reported_victims.remove(target)
                    print(f"[MedicalAidAgent {self.unique_id}] treated victim at {self.pos}, kits left: {self.first_aid_kits}")
                else:
                    print(f"[MedicalAidAgent {self.unique_id}] has no first aid kits left!")

    def setup_field_hospital(self):
        if random.random() < 0.05 and self.pos not in self.model.field_hospitals:
            self.model.field_hospitals.append(self.pos)
            print(f"[MedicalAidAgent {self.unique_id}] set up field hospital at {self.pos}")
