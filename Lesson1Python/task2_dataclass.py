from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    age: int
    active: bool = True


if __name__ == "__main__":
    user1 = User(1, "Богдан", 20)
    user2 = User(2, "Сергій", 19, active=False)
    user3 = User(1, "Марія", 20)

    print(user1)
    print(user2)
    print(user3)
    print("-" * 30)


    print("user1 == user3:", user1 == user3)
    print("user1 == user2:", user1 == user2)
