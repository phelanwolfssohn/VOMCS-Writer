import numpy as np
from PIL import Image
import os

class VomcsMatrixWriter:
    def __init__(self, size=300):
        self.size = size
        # Erzeuge leere 3D-Matrix (alles Nullen)
        self.matrix = np.zeros((size, size, size), dtype=int)
        # Setze den zentralen Hardware-Marker permanent auf 1 (Marker-Bit)
        mitte = size // 2
        self.matrix[mitte, mitte, mitte] = 1

    def text_to_bits(self, text):
        """Konvertiert Text in eine Liste aus echten Bits (0 und 1)."""
        bits = []
        for char in text:
            bin_char = format(ord(char), '08b')
            bits.extend([int(b) for b in bin_char])
        return bits

    def inject_pattern_spiral_style(self, layer_z, bits):
        """Webt eine Bitkette entlang der äußeren Spiralkante einer Schicht ein."""
        x, y = 0, 0
        direction = "down"
        
        for bit in bits:
            if x < self.size and y < self.size:
                self.matrix[x, y, layer_z] = bit
                if direction == "down":
                    if x < self.size - 1: x += 1
                    else: direction = "right"; y += 1
                elif direction == "right":
                    if y < self.size - 1: y += 1
                    else: break

    def generate_german_optimized_cube(self):
        """Füttert die Matrix mit den häufigsten Bausteinen der deutschen Sprache."""
        print(f"[Writer] Starte linguistische Optimierung ({self.size}^3 Bits)...")
        top_silben = ["UND", "DER", "DIE", "DEN", "ICH", "SCH", "EIN"]
        zentrum_start_z = (self.size // 2) - len(top_silben)
        
        for idx, silbe in enumerate(top_silben):
            silben_bits = self.text_to_bits(silbe)
            ziel_schicht = zentrum_start_z + idx
            self.inject_pattern_spiral_style(ziel_schicht, silben_bits)
        return self.matrix

    def export_to_sla_slices(self, output_folder="vomics_slices"):
        """
        Übersetzt die 3D-Matrix in echte, hochauflösende PNG-Schichten für den SLA-Drucker.
        Invertiert die Logik: 0 = Weiß (solides Harz), 1 = Schwarz (Hohlraum/Bit).
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        print(f"\n[Slicer] Generiere {self.size} PNG-Schichten für den Elegoo Mars...")
        
        for z in range(self.size):
            # Erzeuge ein leeres Bild (2D-Array) für die aktuelle Schicht
            # Standardmäßig weiß (255) -> Harz härtet aus (Zustand 0)
            img_array = np.full((self.size, self.size), 255, dtype=np.uint8)
            
            # Finde alle Bits mit Zustand 1 in dieser Schicht
            # Diese werden schwarz (0) -> LCD blockiert Licht -> Hohlraum entsteht
            img_array[self.matrix[:, :, z] == 1] = 0
            
            # Erstelle das PNG und speichere es ab
            img = Image.fromarray(img_array, mode='L')
            
            # Optional: Skaliere das Bild hoch, falls der Drucker eine höhere Auflösung verlangt
            # Für diesen PoC belassen wir es bei der nativen 300x300 Pixel Auflösung
            filename = os.path.join(output_folder, f"layer_{z:03d}.png")
            img.save(filename)
            
        print(f"🎉 EXPORT ERFOLGREICH! {self.size} Schichten im Ordner '{output_folder}' gespeichert.")
        print("[Hinweis] Diese PNGs können nun in Chitubox/Lychee importiert oder direkt zu einer .ctb-Datei gepackt werden.")

# --- COMPILER RUN ---
if __name__ == "__main__":
    # Wir initialisieren den echten Writer für den 6-cm-Kompaktwürfel
    writer = VomcsMatrixWriter(size=300)
    writer.generate_german_optimized_cube()
    writer.export_to_sla_slices()
