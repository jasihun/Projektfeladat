import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

class Auto(ABC):
    """Absztrakt alaposztály az autók számára."""
    def __init__(self, rendszam, tipus, berleti_dij):
        self._rendszam = rendszam
        self._tipus = tipus
        self._berleti_dij = berleti_dij

    @property
    def rendszam(self):
        return self._rendszam

    @property
    def tipus(self):
        return self._tipus

    @property
    def berleti_dij(self):
        return self._berleti_dij

    @abstractmethod
    def get_specifikacio(self):
        """Absztrakt metódus az egyedi tulajdonságok visszaadására."""
        pass


class Szemelyauto(Auto):
    """Személyautó osztály, amely az Auto osztályból örököl."""
    def __init__(self, rendszam, tipus, berleti_dij, ajtok_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self._ajtok_szama = ajtok_szama

    @property
    def ajtok_szama(self):
        return self._ajtok_szama

    def get_specifikacio(self):
        return f"{self._ajtok_szama} ajtós"


class Teherauto(Auto):
    """Teherautó osztály, amely az Auto osztályból örököl."""
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras_kg):
        super().__init__(rendszam, tipus, berleti_dij)
        self._teherbiras_kg = teherbiras_kg

    @property
    def teherbiras_kg(self):
        return self._teherbiras_kg

    def get_specifikacio(self):
        return f"{self._teherbiras_kg} kg teherbírás"


class Berles:
    """Egy adott autó egy napra szóló bérlését tároló osztály."""
    def __init__(self, auto, datum):
        self._auto = auto
        self._datum = datum

    @property
    def auto(self):
        return self._auto

    @property
    def datum(self):
        return self._datum

    def __str__(self):
        tipus_nev = "Személyautó" if isinstance(self._auto, Szemelyauto) else "Teherautó"
        return f"[{tipus_nev}] {self._auto.tipus} ({self._auto.rendszam}) - Dátum: {self._datum} - Ár: {self._auto.berleti_dij} Ft"


class Autokolcsonzo:
    """Az autókölcsönzőt reprezentáló osztály."""
    def __init__(self, nev):
        self._nev = nev
        self._autok = []
        self._berlesek = []

    @property
    def nev(self):
        return self._nev

    @property
    def autok(self):
        return self._autok

    @property
    def berlesek(self):
        return self._berlesek

    def auto_hozzaadas(self, auto):
        self._autok.append(auto)

    def berles_letrehozas(self, rendszam, datum_str):
        """Új bérlés létrehozása validációkkal."""
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Hibás dátum formátum! Kérjük, YYYY-MM-DD formátumot használjon (pl. 2026-06-15).")

        if datum < datetime.today().date():
            raise ValueError("Nem lehet múltbéli dátumra autót bérelni!")

        kivalasztott_auto = None
        for auto in self._autok:
            if auto.rendszam == rendszam:
                kivalasztott_auto = auto
                break

        if not kivalasztott_auto:
            raise ValueError(f"Sajnáljuk, nem található autó ezzel a rendszámmal: {rendszam}")

        for berles in self._berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                raise ValueError(f"A(z) {rendszam} rendszámú autó már foglalt ezen a napon ({datum_str})!")

        uj_berles = Berles(kivalasztott_auto, datum)
        self._berlesek.append(uj_berles)
        return kivalasztott_auto.berleti_dij

    def berles_lemondas(self, rendszam, datum_str):
        """Létező bérlés lemondása validációval."""
        try:
            datum = datetime.strptime(datum_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Hibás dátum formátum! Kérjük, YYYY-MM-DD formátumot használjon.")

        torlendo_berles = None
        for berles in self._berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                torlendo_berles = berles
                break

        if not torlendo_berles:
            raise ValueError(f"Nem található aktív bérlés a(z) {rendszam} rendszámra a következő napon: {datum_str}")

        self._berlesek.remove(torlendo_berles)
        return True

    def berlesek_listazasa(self):
        """Az összes aktuális bérlés visszaadása."""
        if not self._berlesek:
            return "Jelenleg nincsenek aktív bérlések a rendszerben."
        
        rendezett_berlesek = sorted(self._berlesek, key=lambda x: x.datum)
        return "\n".join([str(b) for b in rendezett_berlesek])


def rendszer_inicializalas():
    """Rendszer indításakor előre feltölti a kölcsönzőt 10 autóval és 5 bérléssel."""
    kolcsonzo = Autokolcsonzo("JASI Autokölcsönző")

    # 10 autó létrehozása (7 személyautó, 3 teherautó)
    autok = [
        Szemelyauto("ABC-123", "Opel Astra", 12000, 5),
        Szemelyauto("XYZ-789", "BMW 320d", 25000, 4),
        Teherauto("MNO-456", "Ford Transit", 32000, 1500),
        Szemelyauto("VWE-003", "Volkswagen ID.3 elektromos", 18000, 5),
        Szemelyauto("SUZ-001", "Suzuki Vitara", 14000, 5),
        Teherauto("MER-002", "Mercedes Sprinter", 35000, 2000),
        Szemelyauto("SKO-004", "Skoda Octavia", 15000, 5),
        Teherauto("REN-005", "Renault Master", 30000, 1400),
        Szemelyauto("TOY-006", "Toyota Corolla", 16000, 5),
        Szemelyauto("KIA-007", "Kia Ceed", 13000, 5)
    ]

    for auto in autok:
        kolcsonzo.auto_hozzaadas(auto)

    # 5 bérlés előre feltöltése dinamikus, jövőbeli dátumokkal
    ma = datetime.today().date()
    
    kolcsonzo.berles_letrehozas("ABC-123", (ma + timedelta(days=1)).strftime("%Y-%m-%d"))
    kolcsonzo.berles_letrehozas("VWE-003", (ma + timedelta(days=1)).strftime("%Y-%m-%d"))
    kolcsonzo.berles_letrehozas("MNO-456", (ma + timedelta(days=2)).strftime("%Y-%m-%d"))
    kolcsonzo.berles_letrehozas("SKO-004", (ma + timedelta(days=2)).strftime("%Y-%m-%d"))
    kolcsonzo.berles_letrehozas("KIA-007", (ma + timedelta(days=3)).strftime("%Y-%m-%d"))

    return kolcsonzo


def main():
    kolcsonzo = rendszer_inicializalas()

    while True:
        print(f"\n========================================")
        print(f"    Üdvözli az {kolcsonzo.nev}")
        print(f"========================================")
        print("1. Elérhető autók (flotta) megtekintése")
        print("2. Autó bérlése (1 napra)")
        print("3. Bérlés lemondása")
        print("4. Aktuális bérlések listázása")
        print("5. Kilépés a programból")
        print("========================================")
        
        valasztas = input("Kérjük, válasszon egy menüpontot (1-5): ").strip()

        if valasztas == "1":
            print("\n--- JÁRMŰFLOTTA ---")
            for auto in kolcsonzo.autok:
                tipus_nev = "Személyautó" if isinstance(auto, Szemelyauto) else "Teherautó"
                print(f"Rendszám: {auto.rendszam} | Típus: {auto.tipus} ({tipus_nev}) | "
                      f"Specifikáció: {auto.get_specifikacio()} | Bérleti díj: {auto.berleti_dij} Ft/nap")
        
        elif valasztas == "2":
            print("\n--- ÚJ BÉRLÉS RÖGZÍTÉSE ---")
            rendszam = input("Adja meg a választott autó rendszámát (pl. ABC-123): ").strip().upper()
            datum_str = input("Adja meg a bérlet kívánt napját (ÉÉÉÉ-HH-NN): ").strip()
            
            try:
                ar = kolcsonzo.berles_letrehozas(rendszam, datum_str)
                print(f"\n[SIKER] A bérlés sikeresen rögzítve!")
                print(f"Fizetendő összeg (1 napra): {ar} Ft")
            except ValueError as e:
                print(f"\n[HIBA] Nem sikerült a bérlés: {e}")

        elif valasztas == "3":
            print("\n--- BÉRLÉS LEMONDÁSA ---")
            rendszam = input("Adja meg a lemondani kívánt autó rendszámát: ").strip().upper()
            datum_str = input("Adja meg a lemondani kívánt napot (ÉÉÉÉ-HH-NN): ").strip()
            
            try:
                if kolcsonzo.berles_lemondas(rendszam, datum_str):
                    print(f"\n[SIKER] A bérlés törlése megtörtént.")
            except ValueError as e:
                print(f"\n[HIBA] Lemondás sikertelen: {e}")

        elif valasztas == "4":
            print("\n--- AKTUÁLIS BÉRLÉSEK ---")
            print(kolcsonzo.berlesek_listazasa())

        elif valasztas == "5":
            print("\nKöszönjük, hogy a mi rendszerünket használta! Bízunk benne, hogy elnyerte tetszését és kapok egy j jegyet :)!")
            break
        else:
            print("\n[FIGYELMEZTETÉS] Érvénytelen menüpont! Kérjük, 1 és 5 közötti számot adjon meg.")

if __name__ == "__main__":
    main()