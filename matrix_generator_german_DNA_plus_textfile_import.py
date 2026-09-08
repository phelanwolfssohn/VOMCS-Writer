import numpy as np
from PIL import Image
import os

class VomcsHybridWriter:
    def __init__(self, size=300):
        self.size = size
        # 0 = Klares Harz, 1 = Hohlraum/Bit
        self.matrix = np.zeros((size, size, size), dtype=int)
        
        # Hardware-Zentral-Marker (Permanent 1 bei 150,150,150)
        self.mitte = size // 2
        self.matrix[self.mitte, self.mitte, self.mitte] = 1
        
        # Tracking für die Massen-Injektion (Phase 2)
        self.aktuelle_schicht_p2 = 0

    def text_to_bits(self, text):
        """Konvertiert Text in eine Liste aus echten Bits (0 und 1)."""
        bits = []
        for char in text:
            bin_char = format(ord(char), '08b')
            bits.extend([int(b) for b in bin_char])
        return bits

    # ==========================================
    # GEOMETRISCHE SCHREIB-MUSTER (GEOMETRIEN)
    # ==========================================
    def inject_pattern_spiral(self, layer_z, bits, overwrite=False):
        """MUSTER 0x01: Webt Bits spiralförmig von außen nach innen."""
        x, y = 0, 0
        direction = "down"
        for bit in bits:
            if 0 <= x < self.size and 0 <= y < self.size:
                # Kollisionsschutz: Nur schreiben, wenn Platz frei ist oder Overwrite erlaubt
                if overwrite or self.matrix[x, y, layer_z] == 0:
                    if bit == 1: self.matrix[x, y, layer_z] = 1
                if direction == "down":
                    if x < self.size - 1: x += 1
                    else: direction = "right"; y += 1
                elif direction == "right":
                    if y < self.size - 1: y += 1
                    else: break

    def inject_pattern_zigzag(self, layer_z, bits, overwrite=False):
        """MUSTER 0x03: Webt Bits im klassischen Zickzack-Raster."""
        x, y = 0, 0
        direction = 1 # 1 = Rechts, -1 = Links
        for bit in bits:
            if 0 <= x < self.size and 0 <= y < self.size:
                if overwrite or self.matrix[x, y, layer_z] == 0:
                    if bit == 1: self.matrix[x, y, layer_z] = 1
                if (direction == 1 and y < self.size - 1) or (direction == -1 and y > 0):
                    y += direction
                else:
                    if x < self.size - 1:
                        x += 1
                        direction *= -1
                    else: break

    # ==========================================
    # COMPILER-PHASEN
    # ==========================================
    def execute_phase_1_dna(self):
        """PHASE 1: Einbrennen des linguistischen Fundaments (Feste Zonen)."""
        print("\n[PHASE 1] Starte Einbrennen der deutschen Sprach-DNA...")

        # Kern-Zone (Zickzack-Grammatik)
        grammatik_bruecken = ["DASS", "WEIL", "WENN", "DANN", "OBWOHL", "ABER", "ODER", "SONDERN"]
        for idx, wort in enumerate(grammatik_bruecken):
            bits = self.text_to_bits(wort)
            ziel_z = 140 + idx if idx < 4 else 151 + (idx - 4)
            self.inject_pattern_zigzag(ziel_z, bits, overwrite=True)

        # Mittel-Zone (Top-100 Wörter)
        top_100_words = ["und", "der", "die", "das", "den", "von", "zu", "mit", "in", "auf", "ist", "nicht", "ein", "eine", "ich", "er", "sie", "es", "wir"]
        for idx, wort in enumerate(top_100_words):
            bits = self.text_to_bits(wort.upper())
            ziel_z = 80 + idx if idx < 10 else 161 + (idx - 10)
            self.inject_pattern_spiral(ziel_z, bits, overwrite=True)

        # Rand-Zone (Rotierendes Alphabet)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß.,!?-+0123456789 "
        for ziel_z in list(range(0, 40)) + list(range(260, 300)):
            rotierte_basis = alphabet[ziel_z % len(alphabet):] + alphabet[:ziel_z % len(alphabet)]
            bits = self.text_to_bits(rotierte_basis)
            self.inject_pattern_spiral(ziel_z, bits, overwrite=True)

        print("[PHASE 1] Deutsche Sprach-DNA erfolgreich eingebrannt.")

    def execute_phase_2_massive(self, text_bits):
        """PHASE 2: Fluten der restlichen Matrix mit dem echten Fließtext."""
        print(f"\n[PHASE 2] Starte Massen-Injektion des Fließtexts ({len(text_bits)} Bits)...")
        bit_index = 0
        total_bits = len(text_bits)
        
        while bit_index < total_bits and self.aktueller_x < self.size:
            # Sicherheitsabstand zum Hardware-Marker im Zentrum
            if self.aktuelle_schicht_p2 == self.mitte:
                self.aktuelle_schicht_p2 += 1
                continue
                
            # Wir nehmen 8000 Bits große Happen pro Schicht
            haepchen_groesse = min(8000, total_bits - bit_index)
            aktuelle_bits = text_bits[bit_index : bit_index + haepchen_groesse]
            
            # Dynamischer Musterwechsel pro Schicht, ohne das Fundament zu zerstören!
            if self.aktuelle_schicht_p2 % 2 == 0:
                self.inject_pattern_spiral(self.aktuelle_schicht_p2, aktuelle_bits, overwrite=False)
            else:
                self.inject_pattern_zigzag(self.aktuelle_schicht_p2, aktuelle_bits, overwrite=False)
                
            bit_index += haepchen_groesse
            self.aktuelle_schicht_p2 += 1
            
            # Loop-Schutz: Wenn wir oben ankommen, fangen wir unten wieder in den Lücken an
            if self.aktuelle_schicht_p2 >= self.size:
                self.aktuelle_schicht_p2 = 0
                
        print(f"[PHASE 2] Fließtext integriert. Letzte genutzte Schicht: Z={self.aktuelle_schicht_p2-1}")

    def export_to_sla_slices(self, output_folder="vomics_slices"):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        print(f"\n[Slicer] Exportiere {self.size} hochauflösende PNGs...")
        for z in range(self.size):
            img_array = np.full((self.size, self.size), 255, dtype=np.uint8)
            img_array[self.matrix[:, :, z] == 1] = 0
            img = Image.fromarray(img_array, mode='L')
            filename = os.path.join(output_folder, f"layer_{z:03d}.png")
            img.save(filename)
        print(f"🎉 ENGINE COMPLETE! Alle Schichten in '{output_folder}' generiert.")

# ==========================================
# RUNTIME INTERFACE
# ==========================================
if __name__ == "__main__":
    compiler = VomcsHybridWriter(size=300)
    
    # 1. Phase 1 ausführen (Die DNA-Basis)
    compiler.execute_phase_1_dna()
    
    # 2. Prüfen, ob die Roman-Textdatei existiert
    dateiname = "mein_roman_kapitel.txt"
    if not os.path.exists(dateiname):
        print(f"[System] Erzeuge massive Dummy-Textbasis in '{dateiname}'...")
        with open(dateiname, "w", encoding="utf-8") as f:
            # Wir simulieren ein gigantisches Kapitel deines Buches
            kapitel_text = "Kapitel 1: Der VOMCS-Würfel erwacht. Die Kristalle glühten im nahen Infrarotbereich. " * 3000
            f.write(kapitel_text)

    # Text einlesen
    with open(dateiname, "r", encoding="utf-8") as f:
        echter_roman_text = f.read()
    print(f"[System] Textdatei geladen: '{dateiname}' ({len(echter_roman_text)} Zeichen).")
    
    # 3. Phase 2 ausführen (Den Text dazwischenweben)
    text_bits = compiler.text_to_bits(echter_roman_text)
    compiler.execute_phase_2_massive(text_bits)
    
    # 4. Bilder für den Elegoo Mars ausgeben
    compiler.export_to_sla_slices()
