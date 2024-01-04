class GameCharacter:
    def __init__(self, name, map_position, hp, sp):
        self.name = name
        self.map_position = map_position  # 非战斗状态下的地图坐标
        self.hp = hp  # 角色的HP
        self.sp = sp  # 角色的SP
        self.is_in_battle = False  # 是否为战斗状态

    def set_battle_status(self, battle_status):
        self.is_in_battle = battle_status

    def get_map_position(self):
        return self.map_position

    def get_hp(self):
        return self.hp

    def get_sp(self):
        return self.sp

    def is_alive(self):
        return self.hp > 0

    def has_enough_sp(self, sp_cost):
        return self.sp >= sp_cost

    def take_damage(self, damage):
        self.hp -= damage
        if not self.is_alive():
            self.die()

    def restore_hp(self, hp_amount):
        self.hp += hp_amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def restore_sp(self, sp_amount):
        self.sp += sp_amount
        if self.sp > self.max_sp:
            self.sp = self.max_sp

    def die(self):
        print(f"{self.name} has died.")

    def show_status(self):
        print(f"Character: {self.name}")
        print(f"Map Position: {self.map_position}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"SP: {self.sp}/{self.max_sp}")
        print(f"Battle Status: {'In Battle' if self.is_in_battle else 'Not in Battle'}")

if __name__ == "__main__":
# Example usage:
    character = GameCharacter(name="Hero", map_position=(10, 20), hp=100, sp=50)
    character.set_battle_status(True)
    character.take_damage(30)
    character.show_status()
