# VOMCS Writer — Die Matrix-Generator & SLA-Slicer Engine
**Spezifikation v1.1 — Produktions- und Kompilierungs-Standard (German Text Edition)**

Dieses Repository enthält die Core-Engine zur linguistischen Konditionierung und hardwarenahen Formatierung von volumetrischen VOMCS-Datenwürfeln für den MSLA-Harzdruck (z. B. *Elegoo Mars*).

---

## 🛠️ Technische Funktionsweise (Zwei-Phasen-Compiler)

Die Engine übersetzt unstrukturierte Rohdaten oder Textdateien (`beispiel.txt`) in einem zweistufigen Prozess in physische Schichtbilder (PNGs) oder direkte Maschinencodes:

### 1. Phase 1: Das linguistische Fundament (Feste Zonen)
Der Würfel wird vorab mit der statistischen DNA der deutschen Sprache konditioniert, um die Trefferdichte (Kompression) für Folgedateien massiv zu maximieren.

* **Rand-Zone (Z=0–79 & 221–299 | Äußere Schichten):** Flutet die Ränder mit einer rotierenden Alphabet-Basis (ASCII/UTF-8) und hoch-redundanten Einzelbuchstaben/Bigrammen (E, N, I, T, EN, ER) entlang des linksdrehenden Spiralmusters (`MUSTER_ID: 0x01`).
* **Mittel-Zone (Z=80–139 & 161–220 | Mittlere Schichten):** Webt die 100 häufigsten deutschen Wörter und Silben (DER, DIE, UND, SCH) entlang von raumfüllenden 3D-Hilbert-Kurven (`MUSTER_ID: 0x02`) ein, um semantische Nähe in räumliche Nähe zu übersetzen.
* **Kern-Zone (Z=140–160 | Innere Schichten):** Webt typische deutsche Satzbaumuster und grammatikalische Brücken (DASS, WEIL, WENN...) mittels des Boustrophedon-Scans (`MUSTER_ID: 0x03` / Zickzack) um das absolute Symmetriezentrum.

### 2. Phase 2: Massen-Injektion (Der Ring-Puffer)
Die Engine liest den echten Fließtext ein, konvertiert ihn in einen kontinuierlichen Bitstrom und webt die Daten flüssig in alle verbleibenden Freiräume des Würfels. 

* **Dynamischer Geometrie-Wechsel:** Um maximale geometrische Vielfalt zu erzeugen, wechselt die Engine pro Schicht automatisch zwischen Spirale (gerade Layer) und Zickzack-Raster (ungerade Layer). 
* **Sättigungs-Loop:** Läuft der Text über 300 Schichten hinaus, nutzt die Engine einen **Ring-Puffer**, springt zurück auf Layer 0 und füllt die verbleibenden Lücken in mehreren Umläufen auf.

---

## 💎 Das Phasensprung-Verfahren (Drucker-Firmware-Modifikation)

Um physische Fehldrucke (Abreißen der Schichten durch zu hohe Hohlraum-Sättigung bei massiven Textmengen) komplett zu eliminieren, unterstützt der VOMCS-Standard das **Phasensprung-Verfahren (Dual-Exposure Layer Inversion)**. Der Würfel wird zu 100 % physisch massiv gedruckt, während die Bits rein über optische Dichte-Schlieren (Molekül-Spannungen) im transparenten Harz kodiert werden.

### 1. Das Zwei-Phasen-Belichtungsprotokoll
Der Slicer generiert für jede physische Z-Ebene zwei aufeinanderfolgende Bilder, die die Hardware direkt nacheinander ansteuert:

* **Phase A: Der Massiv-Körper (Solid Base):** Ein komplett weißes Bild ($300 \times 300$ Pixel). Es wird mit der Standard-Herstellerzeit belichtet (z. B. 2,5s). Dies garantiert eine homogene, 100 % stabile Verbindung zwischen den Schichten ohne mechanische Schwachstellen.
* **Phase B: Der Datenstempel (Density Matrix):** Ein invertiertes Bild (komplett schwarz, Datenbits als weiße Pixel). Die Z-Achsen-Bewegung des Druckers wird softwareseitig auf **0,00 mm** fixiert (die Druckplatte verbleibt in Position). Es erfolgt eine kurze Nachbelichtung (z. B. 1,0s). 

An den belichteten Punkten verändern die UV-Strahlen die Molekularstruktur des bereits gehärteten Harzes ein zweites Mal. Es entstehen permanente mikroskopische Trübungen und Dichte-Schlieren, die den Brechungsindex des Lichts verändern.

### 2. Post-Slice-Binary-Patching (Der .ctb-Patcher)
Da Standard-Slicer diese特殊 Doppelbelichtung ohne Z-Achsen-Hub nativ nicht unterstützen, manipuliert ein nachgelagertes Skript (`vomcs_ctb_patcher.py`) die finale Maschinendatei (`.ctb`) auf Byte-Ebene:

1. Die Gesamt-Layer-Anzahl im Datei-Header wird künstlich verdoppelt (von 300 auf 600 Schichten).
2. Zwischen jede originale Schicht wird das entsprechende invertierte VOMCS-Datenbild als Zwischen-Layer injiziert.
3. Die Hebe- und Senkbefehle (Lift/Retract) der Z-Achse werden für jeden ungeraden Zwischen-Layer im Binärcode auf **Null** gesetzt.

Das Ergebnis ist ein makelloser, glasklarer und unzerstörbarer Datenblock, dessen Inhalt für das menschliche Auge unsichtbar ist, aber vom VOMCS-IR-Scanner fehlerfrei ausgelesen werden kann.

---

## 📄 Lizenz & Rechtlicher Hinweis
Dieses Projekt ist lizenziert unter den Bedingungen der **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. 

Die private, wissenschaftliche und gemeinnützige Nutzung, Modifikation und Weiterentwicklung ist ausdrücklich erlaubt und kostenfrei. Jegliche kommerzielle Nutzung, Verwertung im geschäftlichen Betrieb oder Einbindung in proprietäre Produkte ist ohne vorherige, schriftliche Genehmigung und Lizenzierung durch den Urheber untersagt.
