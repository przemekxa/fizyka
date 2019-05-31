import math
import random
import matplotlib.pyplot as plt
import pygame
import os #pozycja okna animacji



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
    @property
    def angle(self):
        """ Wartość kąta """
        b = math.acos(self.x / self.value)
        if self.y < 0:
            b = math.radians(360) - b
        return b


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
        angle1 = self.v.angle
        angle2 = x.v.angle
        contact_angle = math.atan2((self.y - x.y), (self.x - x.x))

        self.v.x = (v2 * math.cos(angle2 - contact_angle)) * math.cos(contact_angle) + v1 * math.sin(
            angle1 - contact_angle) * math.sin(contact_angle)

        self.v.y = (v2 * math.cos(angle2 - contact_angle)) * math.sin(contact_angle) + v1 * math.sin(
            angle1 - contact_angle) * math.cos(contact_angle)

        x.v.x = (v1 * math.cos(angle1 - contact_angle)) * math.cos(contact_angle) + v2 * math.sin(
            angle2 - contact_angle) * math.sin(contact_angle)

        x.v.y = (v1 * math.cos(angle1 - contact_angle)) * math.sin(contact_angle) + v2 * math.sin(
            angle2 - contact_angle) * math.cos(contact_angle)



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
        return


class Box:
    """ Pudełko, w którym poruszają się cząsteczki  """

    def __init__(self, width: float, height: float, start_width: float, W: float, radius: float, grid_s_R: int, grid_s_V: int):
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
    
        # Dane wykresu
        self.wykres_xdata = []
        self.wykres_ydata = []
        self.wykres_line = None

        # Stany i liczba kul
        self.grid_R = grid_s_R
        self.grid_V = grid_s_V
        self.state = [[[[0]*grid_s_V]*grid_s_V]*grid_s_R]*grid_s_R
        

    def detect_wall_collisions(self):
        """ Wykrywanie i obsługa zderzeń ze ścianami """

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

        collision_distance = 1.0000001 * 2 * self.radius

        for i in range(len(self.particles)):

            j = i + 1
            while j < len(self.particles) and self.particles[j].x - self.particles[i].x <= collision_distance:
                if self.particles[i].distance_to(self.particles[j]) <= collision_distance:
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

    def update_states(self):
        self.state = [[[[0]*self.grid_V]*self.grid_V]*self.grid_R]*self.grid_R
        for prtcl in self.particles:
            Rx = int( prtcl.x/(self.grid_R*self.width) )
            if Rx >= self.grid_R:
                Rx = self.grid_R - 1
            if Rx < 0:
                Rx = 0

            Ry = int( prtcl.y/(self.grid_R*self.height) )
            if Ry >= self.grid_R:
                Ry = self.grid_R - 1
            if Ry < 0:
                Ry = 0

            Vx = int( (prtcl.v.x + self.W)/(2*self.W/self.grid_V) )
            if Vx >= self.grid_V:
                Vx = self.grid_V - 1
            if Vx < 0:
                Vx = 0

            Vy = int( (prtcl.v.y + self.W)/(2*self.W/self.grid_V) )
            if Vy >= self.grid_V:
                Vy = self.grid_V - 1
            if Vy < 0:
                Vy = 0
            #print( Rx, Ry, Vx, Vy )
            self.state[Rx][Ry][Vx][Vy] += 1
    

    def calculate_entropy(self):
        S = 0.0
        N = self.grid_V**2 * self.grid_R**2
        S = N * math.log(N) - N
        self.update_states()
        for Rx in range(self.grid_R):
            for Ry in range(self.grid_R):
                for Vx in range(self.grid_V):
                    for Vy in range(self.grid_V):
                        if self.state[Rx][Ry][Vx][Vy] > 0:
                            n = self.state[Rx][Ry][Vx][Vy]
                            S -= n * math.log(n) - n
        return S * -1.38



    def simulate(self):
        """ Symulacja 1 klatki ruchu cząsteczek """
        
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

        # co 1/3 sekunde symulacji
        if self.times_simulated % (self.tps_max/3) == 1:
            
            # Liczenie entropii
            entropia = self.calculate_entropy()
            print( entropia )
            
            # Pokazywanie wykresu
            self.update_plot( self.times_simulated, entropia)

    def set_plot(self ):
        plt.show()
        axes = plt.gca()
        # Skala osi
        axes.set_xlim(0, 2500)
        axes.set_ylim(0, 1000000)
        # Opisy osi
        axes.set_xlabel('time [1/30s]')
        axes.set_ylabel('entropia *10^(23)')
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
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (750,0)
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


b = Box(width=500.0, height=375.0, start_width=100, W=2.0, radius=7, grid_s_R=20, grid_s_V=10)
b.create_particles(100)
b.start()

#CTRL+F os.environ (pozycja startowa okna)


