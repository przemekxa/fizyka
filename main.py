from __future__ import annotations
import math
import random


class Vector:

    """ Wektor """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other) -> Vector:
        """ Dodaj dwa wektory do siebie """
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self) -> str:
        return "vector({:.2f}, {:.2f})".format(self.x, self.y)

    @property
    def value(self) -> float:
        """ Wartość wektora """
        return math.sqrt(self.x**2 + self.y**2)


class Particle:

    """ Pojedyncza cząsteczka o współrzędnych x i y oraz prędkości v
        (w przyszłości można dodać jej promień)
    """
    def __init__(self, x: float, y: float, v: Vector):
        self.x = x
        self.y = y
        self.v = v

    def __str__(self) -> str:
        return "particle([{:.2f}, {:.2f}, {})".format(self.x, self.y, self.v)

    def move(self):
        """ Przesuń cząsteczkę zgodnie z wektorem prędkości """
        self.x += self.v.x
        self.y += self.v.y

    def distance_to(self, to: Particle) -> float:
        """ Odległość od innej cząsteczki """
        return math.sqrt((self.x - to.x)**2 + (self.y - to.y)**2 )

    def collide_with(self, x: Particle):
        """ Zderzenie dwóch cząsteczek """
        # TODO
        return


class Box:

    """ Pudełko, w którym poruszają się cząsteczki  """

    def __init__(self, width: float, height: float, start_width: float, max_v: float, collision_distance: float):
        # Wymiary pudełka
        self.width = width
        self.height = height

        # Początkowa szerokość
        self.startWidth = start_width

        # Maksymalna wartość składowych prędkości
        self.maxV = max_v

        # Odległośc przy której dochodzi do zderzenia
        self.collisionDistance = collision_distance

    def detect_wall_collisions(self):
        """ Wykrywanie i obsługa zderzeń ze ścianami """
        # TODO
        for p in self.particles:

            if p.x <= self.collisionDistance and p.v.x < 0:
                p.v.x *= -1
            elif p.x >= (self.width - self.collisionDistance) and p.v.x > 0:
                p.v.x *= -1
            if p.y <= self.collisionDistance and p.v.y < 0:
                p.v.y *= -1
            elif p.y >= (self.height - self.collisionDistance) and p.v.y > 0:
                p.v.y *= -1

    def detect_particle_collisions(self):
        """ Wykrywanie zderzeń cząsteczek ze sobą """
        for i in range(len(self.particles)):

            j = i+1
            while j<len(self.particles) and self.particles[j].x - self.particles[i].x <= self.collisionDistance:
                if self.particles[i].distance_to(self.particles[j]) <= self.collisionDistance:
                    self.particles[i].collide_with(self.particles[j])
                j += 1

    def show_box(self):
        """ Pokazywanie pozycji cząsteczek w formie graficznej """
        # TODO
        return

    def create_particles(self, n: int):
        """ Tworzenie n cząsteczek
            - cząsteczki o losowych współrzędnych, współrzędna x ograniczona przez startWidth
            - losowe współrzędne wektora prędkości (ograniczone przez maxV)
        """
        self.particles = []
        for i in range(n):
            v = Vector((random.random() * 2 *self.maxV) - self.maxV, (random.random() * 2 * self.maxV) - self.maxV)
            p = Particle(random.random() * self.startWidth, random.random() * self.height, v)
            self.particles.append(p)

    def simulate(self):
        """ Symulacja '1 sekundy' ruchu cząsteczek """

        # Przesunięcie cząsteczek o wektor
        for p in self.particles:
            p.move()

        # Wykrywanie zderzeń ze ścianami
        self.detect_wall_collisions()

        # Wykrywanie zderzeń z cząsteczkami
        self.detect_particle_collisions()

        # Sortowanie tablicy cząsteczek
        self.particles.sort(key=lambda particle: particle.x)

        # Pokazywanie pozycji cząsteczek
        self.show_box()

        # Liczenie entropii
        # TODO

        # Pokazywanie wykresu
        # TODO


b = Box(width=100.0, height=100.0, start_width=20.0, max_v=1.0, collision_distance=1.0)

b.create_particles(5)

for p in b.particles:
    print(p)

for _ in range(1000):
    b.simulate()

print("\n")

for p in b.particles:
    print(p)
