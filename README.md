# Projekt na Fizykę

## Klasy:

### `Vector`
Wektor o współrzędnych `x: float` i `y: float`
- `value` - wartość wektora *(niepotrzebne?)*
- `v1 + v2` - wektory można dodawać

### `Particle`
Pojednycza cząsteczka o współrzędnych `x: float` i `y : float` oraz wektorze prędkości `v: Vector`
- `move(t: float)` - przesuń cząsteczkę zgodnie z wektorem prędkości i krokiem czasu Δt
- `distance_to(Particle)` - odległość między cząsteczkami
- `collide_with(Particle)` - zderzenie dwóch cząsteczek **(do zrobienia)**

### `Box`
Pudełko, w którym poruszają się cząsteczki
- `Box(width: float, height: float, start_width: float, W: float, radius: float)` - inicjalizacja
  - `width: float` - szerokość pudełka
  - `height: float` - wysokość pudełka
  - `start_width: float` - początkowa szerokość pudełka (tutaj będą na początku cząsteczki)
  - `W: float` - maksymalne początkowe wartości współrzędnych wektora prędkości
  - `radius: float` - promień pojedynczej cząsteczki
- `create_particles(int)` - tworzenie n cząsteczek
  - cząsteczki o losowych współrzędnych, współrzędna `x` ograniczona przez `startWidth`
  - losowe współrzędne wektora prędkości (ograniczone przez `maxV`)
- `detect_particle_collisions()` - wykrywanie zderzeń cząsteczek ze sobą
- `detect_wall_collisions()` - wykrywanie i obsługa zderzeń ze ścianami **(do zrobienia)**
- `show_box()` - pokazywanie pozycji cząsteczek na ekranie
- `simulate()` - symulacja "1 sekundy" ruchu cząsteczek
- `start()` - pętla symulacji (zamknięcie okna kończy symulację)

<br>

---

## Do zrobienia
- [x] szkielet
- [ ] kolizje ze ścianami
- [ ] kolizje cząsteczek ze sobą
- [x] pokazywanie pozycji cząsteczek
- [ ] liczenie entropii
- [ ] wykres entropii
