from dataclasses import dataclass, field
import random
import sys

sys.setrecursionlimit(10000)

@dataclass
class Army:
    name: str
    troops: int
    vehicles: int
    tanks: int
    artillery: int
    missle: int

    def troops_recruit(self) -> None:
        generate_number_troops = random.randrange(700, 10000)
        self.troops += generate_number_troops

    def get_vehicle(self) -> None:
        generate_number_vehicle = random.randrange(10, 100)
        self.vehicles += generate_number_vehicle

    def get_tanks(self) -> None:
        generate_number_tank = random.randrange(2, 20)
        self.vehicles += generate_number_tank


@dataclass
class Squad:
    name: str = "No Squad"
    troop: int = 0
    vehicle: int = 0
    tank: int = 0
    recon: bool = False
    skill_value: int = 1
    TROOPS_POWER = 1
    VEHICLE_POWER = 3
    TANK_POWER = 7

    def squad_info(self) -> list:
        return [self.name, self.troop,
                self.vehicle, self.tank]

    def troops_power(self) -> int:
        high_troops_power = (self.troop *
                             self.TROOPS_POWER *
                             self.skill_value)
        return random.randrange(1, high_troops_power)

    def vehicle_power(self) -> int:
        high_vehicle_power = (self.vehicle *
                              self.VEHICLE_POWER *
                              self.skill_value)
        return random.randrange(1, high_vehicle_power)

    def tank_power(self) -> int:
        high_tank_power = self.tank * self.TANK_POWER * self.skill_value
        return random.randrange(1, high_tank_power)

    def squad_power(self) -> float:
        power_sum = (((self.troop * self.TROOPS_POWER) +
                     (self.vehicle * self.VEHICLE_POWER) +
                     (self.tank * self.TANK_POWER)) *
                     self.skill_value)
        return power_sum

    def skill_up(self):
        self.skill_value += 1

    def check_squad_num(self):
        if self.troop <= 0:
            self.__dict__["troop"] = 0

    def check_tech(self):
        if self.troop < 11:
            self.__dict__["recon"] = True
        elif self.troop >= 11 and self.troop <= 44:
            self.__dict__["vehicle"] = self.troop // 11
        elif self.troop > 44 and self.troop <= 53:
            self.__dict__["vehicle"] = (self.troop - 9) // 11
            self.__dict__["tank"] = (self.troop - 44) // 3
        else:
            pass


@dataclass
class Point:
    name: str = ""
    enemy_squad: Squad = field(default_factory=Squad)
    wagner_squad: Squad = field(default_factory=Squad)
    recon_status: bool = False
    clear_status: bool = False

    def generate_enemy_name(self) -> str:
        names = random.choice(["Азов",
                               "138ОБР",
                               "Кракен"])
        number_of_squad = random.randrange(1, 101)
        return f"{names} отряд номер {number_of_squad}"

    def generate_enemy_forces(self) -> int:
        troops_enemy = random.randrange(0, 54)
        return troops_enemy

    def squad_enemy_create(self) -> Squad:
        name_enemy = self.generate_enemy_name()
        enemy_forces = self.generate_enemy_forces()
        squad = Squad(name_enemy,
                      troop=enemy_forces,
                      skill_value=random.randrange(0, 2))
        squad.check_tech()
        return squad

    def __post_init__(self):
        self.__dict__['enemy_squad'] = self.squad_enemy_create()
        self.__dict__['name'] = self.enemy_squad.name


    def fallback_squad(self):
        self.__dict__['wagner_squad'] = Squad()

    def fallback_enemy(self):
        self.__dict__['enemy_squad'] = Squad()
    
    def clear_point(self):
        self.fallback_enemy()
        self.clear_status = True

    def place_wagner_squad(self, squad: Squad):
        self.__dict__['wagner_squad'] = squad

    def empty_squad_check(self):
        if self.wagner_squad.name == "No Squad":
            return "No Squad"

    def strike_power(self):
        wagner_power = self.wagner_squad.squad_power()
        enemy_power = self.enemy_squad.squad_power()
        power_strike_wagner = random.choice(range(1, int(wagner_power)))
        power_strike_enemy = random.choice(range(1, int(enemy_power)))
        if power_strike_wagner > power_strike_enemy:
            damage_sum_wagner = int((int(wagner_power) // 2) +
                                    power_strike_wagner)
            damage_sum_enemy = int((int(wagner_power) // 4) +
                                   power_strike_enemy)
            tech_damage_wagner = random.choice(range(2, 5))
            tank_damage_wagner = random.choice(range(1, 3))
            tech_damage_enemy = random.choice(range(0, 2))
            tank_damage_enemy = 0
            damage_final = {"Wagner": [damage_sum_wagner,
                                       tech_damage_wagner,
                                       tank_damage_wagner],
                            "Enemy": [damage_sum_enemy,
                                      tech_damage_enemy,
                                      tank_damage_enemy]}
            return damage_final
        elif power_strike_wagner == power_strike_enemy:
            damage_sum_wagner = int((int(wagner_power) // 2) +
                                    power_strike_wagner)
            damage_sum_enemy = int((int(wagner_power) // 2) +
                                   power_strike_enemy)
            tech_damage_wagner = random.choice(range(1, 2))
            tank_damage_wagner = 0
            tech_damage_enemy = random.choice(range(1, 2))
            tank_damage_enemy = 0
            damage_final = {"Wagner": [damage_sum_wagner,
                                       tech_damage_wagner,
                                       tank_damage_wagner],
                            "Enemy": [damage_sum_enemy,
                                      tech_damage_enemy,
                                      tank_damage_enemy]}
            return damage_final
        else:
            damage_sum_wagner = int((int(wagner_power) // 4) +
                                    power_strike_wagner)
            damage_sum_enemy = int((int(wagner_power) // 2) +
                                   power_strike_enemy)
            tech_damage_wagner = random.choice(range(0, 2))
            tank_damage_wagner = 0
            tech_damage_enemy = random.choice(range(2, 5))
            tank_damage_enemy = random.choice(range(1, 3))
            damage_final = {"Wagner": [damage_sum_wagner,
                                       tech_damage_wagner,
                                       tank_damage_wagner],
                            "Enemy": [damage_sum_enemy,
                                      tech_damage_enemy,
                                      tank_damage_enemy]}
            return damage_final

    def battle_on_point(self):
        damage = self.strike_power()
        wagner_damage = damage["Wagner"]
        enemy_damage = damage["Enemy"]
        self.wagner_squad.troop -= enemy_damage[0]
        self.wagner_squad.troop -= enemy_damage[1]
        self.wagner_squad.troop -= enemy_damage[2]
        self.enemy_squad.troop -= wagner_damage[0]
        self.enemy_squad.troop -= wagner_damage[1]
        self.enemy_squad.troop -= wagner_damage[2]
        self.wagner_squad.check_squad_num()
        self.enemy_squad.check_squad_num()
        if self.enemy_squad.troop <= 0:
            self.clear_point()
            return "Вагнер одержал победу"
        elif self.wagner_squad.troop <= 0:
            self.fallback_squad()
            return "Отряд Вагнера уничтожен"
        self.battle_on_point()

    def recon_point(self):
        if self.wagner_squad.recon is True:
            self.__dict__["recon_status"] = True
            return "Отдряд провёл разведку"
        elif self.wagner_squad.recon is False:
            return "Отряд не пригоден для разведки"


@dataclass
class Battlefield:
    points: dict

    def create_points(self):
        for i in range(3):
            point = Point()
            self.points[point.name] = point

    def complete_mission(self):
        safe_d = self.points.copy()
        for name in safe_d.keys():
            if self.points[name].clear_status is True:
                del self.points[name]

    def clear_points(self):
        self.points.clear()


@dataclass
class Game:
    wagner_group: Army
    hohol_group: Army
    squad_dict: dict
    turn_number: int = 0
    cooldown_battle: int = 10
    cooldown_recruit: int = 10
    control_city: int = 50
    order_status: bool = False

    def recruit_troop(self) -> None:
        if self.cooldown_recruit == 0:
            self.cooldown_recruit += 30
            self.wagner_group.troops_recruit()

    def recruit_vehicle(self) -> None:
        if self.cooldown_recruit == 0:
            self.cooldown_recruit += 35
            self.wagner_group.get_vehicle()

    def recruit_tank(self) -> None:
        if self.cooldown_recruit == 0:
            self.cooldown_recruit += 40
            self.wagner_group.get_tanks()

    def squad_add(self, squad: Squad) -> None:
        if squad.troop != 0:
            squad.check_tech()
            self.wagner_group.troops -= squad.troop
            self.wagner_group.vehicles -= squad.vehicle
            self.wagner_group.tanks -= squad.tank
            self.squad_dict[squad.name] = squad

    def recruit_cooldown(self):
        if self.cooldown_recruit == 0:
            pass
        elif self.cooldown_recruit < 0:
            self.cooldown_recruit = 0
        else:
            self.cooldown_recruit -= 5

    def battlefield_control_change(self, battlefield: Battlefield):
        for point in battlefield.points.values():
            if point.clear_status is False:
                self.control_city -= 5

    def battlefield_cooldown(self, battlefield: Battlefield):
        if self.cooldown_battle == 0:
            self.cooldown_battle += 25
            self.battlefield_control_change(battlefield)
            battlefield.clear_points()
            battlefield.create_points()
        else:
            self.cooldown_battle -= 5

    def update_battlefield(self, battlefield: Battlefield):
        for point in battlefield.points.values():
            if point.clear_status is True:
                self.control_city += 5
        battlefield.complete_mission()

    def next_turn(self, battlefield: Battlefield):
        self.update_battlefield(battlefield)
        self.battlefield_cooldown(battlefield)
        self.recruit_cooldown()
        self.turn_number += 1

    def send_squad(self, name_squad: str):
        del self.squad_dict[name_squad]

    def return_squad(self, squad: Squad):
        self.squad_dict[squad.name] = squad

    def order_to_squad(self):
        self.__dict__['order_status'] = True

    def end_order_to_squad(self):
        self.__dict__['order_status'] = False
