import math
import random

import matplotlib.pyplot as plt

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
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Particle:
    """ Pojedyncza cząsteczka o współrzędnych x i y oraz prędkości v
        (w przyszłości można dodać jej promień) """
    

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
        return math.sqrt((self.x - to.x) ** 2 + (self.y - to.y) ** 2)

    def collide_with(self, x: "Particle", W: float, r: float):
        """ Zderzenie dwóch cząsteczek """
        # TODO
        
        v1 = self.v.value
        v2 = x.v.value
        angle1 = math.acos(self.v.x / v1)
        #tutaj
        #if self.v.y < 0:
        #    angle1 *= -1
        angle2 = math.acos(x.v.x / v2)
        #tutaj
        #if self.v.y < 0:
        #    angle2 *= -1
        contact_angle = math.atan2((self.y - x.y), (self.x - x.x))
        #tutaj
        #if contact_angle > 0:
        #    contact_angle -= 2 * math.pi
        #contact_angle *= -1

        self.v.x = (v2 * math.cos(angle2 - contact_angle)) * math.cos(contact_angle) + v1 * math.sin(
            angle1 - contact_angle) * math.sin(contact_angle)
        if self.v.x > W:
            self.v.x = W
        elif self.v.x < -W:
            self.v.x = -W
        self.v.y = (v2 * math.cos(angle2 - contact_angle)) * math.sin(contact_angle) + v1 * math.sin(
            angle1 - contact_angle) * math.cos(contact_angle)
        if self.v.y > W:
            self.v.y = W
        elif self.v.y < -W:
            self.v.y = -W
        x.v.x = (v1 * math.cos(angle1 - contact_angle)) * math.cos(contact_angle) + v2 * math.sin(
            angle2 - contact_angle) * math.sin(contact_angle)
        if x.v.x > W:
            x.v.x = W
        elif x.v.x < -W:
            x.v.x = -W
        x.v.y = (v1 * math.cos(angle1 - contact_angle)) * math.sin(contact_angle) + v2 * math.sin(
            angle2 - contact_angle) * math.cos(contact_angle)
        if x.v.y > W:
            x.v.y = W
        elif x.v.y < -W:
            x.v.y = -W
        n = 0
        while self.distance_to(x) < 2 * r and n < 5:
            self.x += self.v.x
            self.y += self.v.y
            x.x += x.v.x
            x.y += x.v.y
            n += 1
        """

        contact_angle = math.atan2((self.y - x.y), (self.x - x.x))
        self.v.x = self.v.x*math.sin(contact_angle) + x.v.x*math.cos(contact_angle)
        self.v.y = self.v.y*math.sin(contact_angle) + x.v.y*math.cos(contact_angle)
        x.v.x = x.v.x*math.sin(contact_angle) + self.v.x*math.cos(contact_angle)
        x.v.y = x.v.y*math.sin(contact_angle) + self.v.y*math.cos(contact_angle)
        while self.distance_to(x) < 2.0*r:
            self.x += self.v.x
            self.y += self.v.y
            x.x += x.v.x
            x.y += x.v.y
        """
        """
        v1 = self.v.value - ((self.v.x - x.v.x)*(self.x - x.x) + (self.v.y - x.v.y)*(self.y-x.y))/(
            math.sqrt((self.x-x.x)**2 + (self.y-x.y)**2)*(
                math.sqrt(self.x ** 2 + self.y ** 2) - math.sqrt(x.x ** 2 + x.y ** 2)))
        v2 = x.v.value - ((x.v.x - self.v.x)*(x.x - self.x) + (x.v.y - self.v.y)*(x.y - self.y))/(
            math.sqrt((x.x-self.x)**2 + (x.y-self.y)**2)*(
                math.sqrt(x.x**2 + x.y**2) - math.sqrt(self.x**2 + self.y**2)))
        vec = Vector(5,1)
        angle1 = math.acos(v1 / vec.x)
        angle2 = math.acos(v2 / vec.x)
        self.v.x = v1*math.cos(angle1)
        self.v.y = v1*math.sin(angle1)
        x.v.x = v2*math.cos(angle2)
        x.v.y = v2*math.sin(angle2)
        """
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

        # Potrzebne do odmierzania czasu
        self.tps_clock = pygame.time.Clock()

        # Rożnice czasu miedzy kolejnymi klatkami
        self.tps_delta = 0.0

        # Liczba klatek na sekunde
        self.tps_max = 30.0
        
        # Ilosc wykonanych symulacji
        self.times_simulated = 0
    
        # Wykres dane
        self.wykres_xdata = []
        self.wykres_ydata = []
        self.wykres_line = None
        

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

            j = i + 1
            while j < len(self.particles) and self.particles[j].x - self.particles[i].x <= (2.02 * self.radius):
                if self.particles[i].distance_to(self.particles[j]) <= (2.02 * self.radius):
                    self.particles[i].collide_with(self.particles[j], self.W, self.radius)
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
        
        # Numer symulacji
        self.times_simulated += 1

        # Przesunięcie cząsteczek o wektor
        for p in self.particles:
            p.move(1.0 / (1 * self.W))

        # Wykrywanie zderzeń ze ścianami
        self.detect_wall_collisions()

        # Wykrywanie zderzeń z cząsteczkami
        self.detect_particle_collisions()

        # Sortowanie tablicy cząsteczek
        self.particles.sort(key=lambda particle: particle.x)

        # Pokazywanie pozycji cząsteczek
        self.show_box()

        # co 1 sekunde symulacji
        if self.times_simulated % self.tps_max == 1:
            # Liczenie entropii
            # TODO
            entropia = random.randint(0,100)
            
            
            
            # Pokazywanie wykresu
            self.update_plot( self.times_simulated, entropia)

    def set_plot(self ):
        plt.show()
        axes = plt.gca()
        # Skala osi
        axes.set_xlim(0, 2000)
        axes.set_ylim(0, 100)
        # Opisy osi
        axes.set_xlabel('tick')
        axes.set_ylabel('entropia')
        # Tytul
        axes.set_title('Entropia')
                        
        self.line, = axes.plot( [], [], 'r-')
    
        
    def update_plot(self, new_x, new_y):
        # Dodaj do tablicy danych nowe dane
        self.wykres_ydata.append( new_y )
        self.wykres_xdata.append( new_x )
        # Zaktualizuj zrodlo danych do wykresu
        self.line.set_xdata(self.wykres_xdata)
        self.line.set_ydata(self.wykres_ydata)
        # Narysuj zaktualizowany wykres
        plt.draw()
        plt.pause(1e-17)
    
        
    def start(self):
        """ Pętla symulacji """

        # Inicjalizacja PyGame
        pygame.init()

        # Inicjalizacja okna
        self.screen = pygame.display.set_mode((int(self.width), int(self.height)))
        end_program = False
        
        # Start wykresu
        self.set_plot()
        
        
        # Pętla programu
        while not end_program:
            
            # Kliknięcie w zamknięcie okna
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end_program = True
        
            self.tps_delta += self.tps_clock.tick() / 1000.0
            while self.tps_delta > 1.0 / self.tps_max:
                self.simulate()
                self.tps_delta -= 1.0 / self.tps_max



b = Box(width=500.0, height=375.0, start_width=100, W=2.0, radius=3)
b.create_particles(50)
b.start()


