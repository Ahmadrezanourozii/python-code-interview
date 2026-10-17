# Part 4 - object-oriented programming (just what a live task needs)

# %% class_basic
class Car:
    wheels = 4                               # class attribute (shared)

    def __init__(self, model: str, year: int, km: float = 0):
        self.model = model                   # instance attributes
        self.year = year
        self.km = km

    def drive(self, distance: float) -> None:
        if distance < 0:
            raise ValueError("distance must be positive")
        self.km += distance

    def needs_service(self, interval: int = 25_000) -> bool:
        return self.km >= interval

    def __repr__(self):                      # how the object is printed
        return f"Car({self.model!r}, {self.year}, km={self.km})"


c = Car("C200", 2021)
c.drive(30_000)
print(c, c.needs_service(), Car.wheels)

# %% inheritance
class ElectricCar(Car):
    def __init__(self, model, year, battery_kwh, km=0):
        super().__init__(model, year, km)    # reuse the parent __init__
        self.battery_kwh = battery_kwh

    def range_km(self, kwh_per_100km=18):
        return round(self.battery_kwh / kwh_per_100km * 100)

    def __repr__(self):                      # override the parent method
        return f"ElectricCar({self.model!r}, {self.battery_kwh} kWh)"


eqs = ElectricCar("EQS", 2022, 108)
eqs.drive(100)                               # inherited from Car
print(eqs, eqs.range_km(), eqs.km, isinstance(eqs, Car))

# %% composition
class Fleet:
    def __init__(self):
        self.cars = []                       # a Fleet HAS cars

    def add(self, car):
        self.cars.append(car)

    def __len__(self):
        return len(self.cars)

    def total_km(self):
        return sum(c.km for c in self.cars)

    def due_for_service(self, interval=25_000):
        return [c.model for c in self.cars if c.needs_service(interval)]


fleet = Fleet()
for model, year, km in [("C200", 2020, 40_000), ("E300", 2022, 9_000),
                        ("S500", 2019, 61_000)]:
    fleet.add(Car(model, year, km))
print(len(fleet), fleet.total_km(), fleet.due_for_service())

# %% property
class Battery:
    def __init__(self, level=100):
        self.level = level                   # goes through the setter

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if not 0 <= value <= 100:
            raise ValueError("level must be between 0 and 100")
        self._level = value


b = Battery(80)
b.level = 55
print(b.level)
try:
    b.level = 120
except ValueError as e:
    print("error:", e)

# %% dataclass
from dataclasses import dataclass, field


@dataclass
class Task:
    title: str
    owner: str
    hours: float = 0.0
    done: bool = False
    tags: list = field(default_factory=list)  # never use tags: list = []


t = Task("Write report", "Ali", 3)
t.tags.append("docs")
print(t)
print(t == Task("Write report", "Ali", 3, tags=["docs"]))  # __eq__ is free

# %% dunder_sort
from dataclasses import dataclass


@dataclass(order=True)                       # adds <, > based on fields
class Version:
    major: int
    minor: int


versions = [Version(2, 1), Version(1, 9), Version(2, 0)]
print(sorted(versions)[0], max(versions))
