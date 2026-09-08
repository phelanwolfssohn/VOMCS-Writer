import numpy as np

class VomcsMatrixGenerator:
    def __init__(self, size=300):
        self.size = size
        # Erzeuge leere 3D-Matrix (alles Nullen)
        self.matrix = np.zeros((size, size, size), dtype=int)
        # Setze den zentralen Hardware-Marker permanent auf 1
        mitte = size // 2
        self.matrix[mitte, mitte, mitte] = 1

    def text_to_bits(self, text):
        """Konvertiert einen String in eine Liste aus echten Bits (0 und 1)."""
        bits = []
        for char in text:
            # Wandle Zeichen in 8-Bit Binärstring um
            bin_char = format(ord(char), '08b')
            bits.extend([int(b) for b in bin_char])
        return bits

    def inject_pattern_spiral_style(self, layer_z, bits):
        """
        Webt eine Bitkette gezielt in eine bestimmte Schicht (Z-Ebene) ein.
        Nutzt die Logik der linksdrehenden Spirale (von außen nach innen).
        """
        # Beispielhafter Pfadverlauf für die äußeren Ränder einer Schicht
        # In der echten 300x300 Matrix wird dies mathematisch hochgerechnet
        x, y = 0, 0
        direction = "down"
        
        for bit in bits:
            if x < self.size and y < self.size:
                self.matrix[x, y, layer_z] = bit
                
                # Einfache Schrittmechanik entlang der Außenkante abwärts
                if direction == "down":
                    if x < self.size - 1: x += 1
                    else: direction = "right"; y += 1
                elif direction == "right":
                    if y < self.size - 1: y += 1
                    else: break # Für den PoC stoppen wir an der Ecke

    def generate_german_optimized_cube(self):
        """Füttert die Matrix mit den häufigsten Bausteinen der deutschen Sprache."""
        print(f"[Generator] Starte Matrix-Optimierung für deutsche Sprache ({self.size}^3 Bits)...")
        
        # 1. Die Top-Trigramme (Silben) des Deutschen
        top_silben = ["UND", "DER", "DIE", "DEN", "ICH", "SCH", "EIN"]
        
        # 2. Wir weben diese Silben in die wichtigsten inneren Schichten (nahe dem Zentrum)
        zentrum_start_z = (self.size // 2) - len(top_silben)
        
        for idx, silbe in enumerate(top_silben):
            silben_bits = self.text_to_bits(silbe)
            ziel_schicht = zentrum_start_z + idx
            
            # Gezielte Injektion
            self.inject_pattern_spiral_style(ziel_schicht, silben_bits)
            print(f" -> Silbe '{silbe}' ({len(silben_bits)} Bits) erfolgreich in Schicht Z={ziel_schicht} gewebt.")
            
        print("[Generator] Struktur-Generierung abgeschlossen. Bereit für den SLA-Export.")
        return self.matrix

# --- TESTLAUF DES GENERATORS ---
if __name__ == "__main__":
    # Wir testen es mit einer kleineren Matrix (z.B. 30x30x30) für die Konsole
    generator = VomcsMatrixGenerator(size=30)
    optimierte_matrix = generator.generate_german_optimized_cube()
    
    # Überprüfung, ob Daten angekommen sind
    print(f"\n[Verifikation] Gesamtanzahl gesetzter Bits (Zustand 1): {np.sum(optimierte_matrix)}")
