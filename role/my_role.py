from my_image import my_image

class GameCharacter:
    def __init__(self):
        role = None

    def show_sence(self):
        a = my_image.my_image()
        print(a.get_prop(30, 30, 1000, 800, "herbs"))
    def show_status(self):
        print(f"Character: {self.name}")
        print(f"Map Position: {self.map_position}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"SP: {self.sp}/{self.max_sp}")
        print(f"Battle Status: {'In Battle' if self.is_in_battle else 'Not in Battle'}")

if __name__ == "__main__":
# Example usage:
    a = GameCharacter()
    a.show_sence()
