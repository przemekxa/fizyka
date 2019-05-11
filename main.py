import math
import random
import pygame


class Vector:

    """ Wektor """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y

    def __add__(self, other) -> "Vector":
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

    def move(self, t: float):
        """ Przesuń cząsteczkę zgodnie z wektorem prędkości """
        self.x += t * self.v.x
        self.y += t * self.v.y

    def distance_to(self, to: "Particle") -> float:
        """ Odległość od innej cząsteczki """
        return math.sqrt((self.x - to.x)**2 + (self.y - to.y)**2 )

    def collide_with(self, x: "Particle"):
        """ Zderzenie dwóch cząsteczek """
        # TODO
        return


class Box:

    """ Pudełko, w którym poruszają się cząsteczki  """

    def __init__(self, width: float, height: float, start_width: float, W: float, radius: float):
        # Wymiary pudełka
        self.width = width
        self.height = height

        # Początkowa szerokość
        self.startWidth = start_width

        # Maksymalna wartość składowych prędkości
        self.W = W

        # Promień pojedynczej cząsteczki
        self.radius = radius

        # Okno, w którym cząsteczki będą wyświetlane
        self.screen = None

    def detect_wall_collisions(self):
        """ Wykrywanie i obsługa zderzeń ze ścianami """
        # TODO

        collision_distance = 1.01 * self.radius

        for p in self.particles:

            if p.x <= collision_distance and p.v.x < 0:
                p.v.x *= -1
            elif p.x >= (self.width - collision_distance) and p.v.x > 0:
                p.v.x *= -1
            if p.y <= collision_distance and p.v.y < 0:
                p.v.y *= -1
            elif p.y >= (self.height - collision_distance) and p.v.y > 0:
                p.v.y *= -1

    def detect_particle_collisions(self):
        """ Wykrywanie zderzeń cząsteczek ze sobą """
        for i in range(len(self.particles)):

            j = i+1
            while j < len(self.particles) and self.particles[j].x - self.particles[i].x <= (2.01 * self.radius):
                if self.particles[i].distance_to(self.particles[j]) <= (2.01 * self.radius):
                    self.particles[i].collide_with(self.particles[j])
                j += 1

    def show_box(self):
        """ Pokazywanie pozycji cząsteczek na ekranie """
        self.screen.fill((0, 0, 0))
        for particle in self.particles:
            pygame.draw.circle(self.screen, (0, 255, 255), [int(particle.x), int(particle.y)], int(self.radius))
        pygame.display.flip()

    def create_particles(self, n: int):
        """ Tworzenie n cząsteczek
            - cząsteczki o losowych współrzędnych, współrzędna x ograniczona przez startWidth
            - losowe współrzędne wektora prędkości (ograniczone przez W)
        """
        self.particles = []
        for i in range(n):
            v = Vector((random.random() * 2 * self.W) - self.W, (random.random() * 2 * self.W) - self.W)
            p = Particle(random.random() * self.startWidth, random.random() * self.height, v)
            self.particles.append(p)

    def simulate(self):
        """ Symulacja '1 sekundy' ruchu cząsteczek """

        # Przesunięcie cząsteczek o wektor
        for p in self.particles:
            p.move(1.0 / (1.0 * self.W))

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

    def start(self):
        """ Pętla symulacji """

        # Inicjalizacja PyGame
        pygame.init()

        # Inicjalizacja okna
        self.screen = pygame.display.set_mode((int(self.width), int(self.height)))

        end_program = False

        # Pętla programu
        while not end_program:
            # Kliknięcie w zamknięcie okna
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_program = True

            self.simulate()


b = Box(width=800.0, height=600.0, start_width=20, W=2.0, radius=0.1)
b.create_particles(300)
b.start()

