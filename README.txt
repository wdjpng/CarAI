Der bereitgestellte Source-Code enthält eine vollständige Implementierung der Autosimulation. Eine Simulation besteht aus einer Strecke (Track), einem Auto (Car) und einer KI (Brain), welche das Auto steuert. Es stehen standardmäßig 6 unterschiedliche Strecken in Form von Levels zur Verfügung. Diese können über Track.level() geladen werden. Das Auto selbst (Car) muss normalerweise nicht angepasst werden und es kann die bereitgestellte Implementierung verwendet werden. 
Um eine neue KI zu erstellen, fügt man in der brains.py-Datei eine neue Brain-Klasse hinzu. Die Klasse stellt zwei Methoden bereit: setup() setzt die initialen KI-Werte, installiert Sensoren am Auto, usw.; update() wird alle paar Sekunden aufgerufen und steuert das Auto. Die beiden Beispiel-KIs zeigen, wie man Sensoren installiert und deren Werte ausliest.
class DoNothingBrain(Brain):
    def setup(self):
        pass
    def update(self):
        pass

Hat man ein neues Brain erstellt, muss man es nur noch dem Auto zuweisen. Dafür ändert man die folgende Zeile in der main.py.
# create car 
car = Car(track, brains.DoNothingBrain(), color="blue")

Die Implementierung besteht aus den folgenden Dateien:
- main.py  Das Hauptprogramm: Hier wird die Simulation konfiguriert. Welche Strecke soll verwendet werden, welche KI, usw.
- brains.py  Enthält die KI-Implementierungen: Jede KI wird als Brain implementiert. Zwei einfache Implementierungen dienen als Beispiel.
- trackeditor.py  Einfacher Editor, mit dem man eigene Strecken zeichnen kann: Mit [s] werden die gezeichneten Punkte in der Konsole ausgegeben. Die erstellten Punkte kann man dann als midline_points der Track Klasse übergeben.
- lib/car.py: Implementierung des Autos (Car).
- lib/math2d.py: Mathematische Klassen und Methoden für 2d.
- lib/sensors.py: Abstand- und Zielsensoren.
- lib/tracks.py: Strecke (Track).

Die Klassen im "lib"-Ordner müssen normalerweise nicht angepasst werden. Hier kann man nachschauen, wie die Sensoren oder die Tracks genau funktionieren. Im "solutions"-Ordner gibt es einige Lösungen.

Gestartet wird für gewöhnlich immer über main.py

Einzige Ausnahme: Für eine Lösung des genetischen Algorithmus wird statt main.py die Datei solutions/population_handler.py gestartet. Sie verwendet das "brains_genetic"-File und organisiert das Vererben von Fähigkeiten.
