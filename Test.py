def berechne_notwendige_verzoegerung(abstand, relative_geschwindigkeit, verzoegerung_B):
    """
    Berechnet die notwendige Verzögerung, um eine Kollision zu vermeiden.

    :param abstand: Der Abstand zwischen den Fahrzeugen in Metern (m)
    :param relative_geschwindigkeit: Die relative Geschwindigkeit der Fahrzeuge in Metern pro Sekunde (m/s)
    :param verzoegerung_B: Die Verzögerung des vorausfahrenden Fahrzeugs in Metern pro Sekunde zum Quadrat (m/s^2)
    :return: Die notwendige Verzögerung des folgenden Fahrzeugs in Metern pro Sekunde zum Quadrat (m/s^2)
    """
    # Die Zeit bis zur Kollision berechnen (ohne Verzögerung)
    if relative_geschwindigkeit <= 0:
        return 0  # Wenn relative Geschwindigkeit <= 0, ist keine Verzögerung notwendig

    zeit_bis_kollision = abstand / relative_geschwindigkeit

    # Die Strecke berechnen, die Fahrzeug B in dieser Zeit zurücklegt
    strecke_B = 0.5 * verzoegerung_B * zeit_bis_kollision ** 2

    # Die notwendige Verzögerung für Fahrzeug A berechnen, um vor der Kollision zum Stillstand zu kommen
    notwendige_verzoegerung = (relative_geschwindigkeit ** 2) / (2 * (abstand - strecke_B))

    return -notwendige_verzoegerung


# Beispielanwendung
abstand = 15  # Meter
relative_geschwindigkeit = 15  # m/s
verzoegerung_B = 0  # m/s^2 (angenommene Verzögerung des vorausfahrenden Fahrzeugs)

notwendige_verzoegerung = berechne_notwendige_verzoegerung(abstand, relative_geschwindigkeit, verzoegerung_B)
print(f"Notwendige Verzögerung: {notwendige_verzoegerung:.2f} m/s^2")


def berechne_beschleunigung(v1, v2, zeit):
    """
    Berechnet die Beschleunigung bzw. Verzögerung in m/s^2.

    :param v1: Anfangsgeschwindigkeit in m/s
    :param v2: Endgeschwindigkeit in m/s
    :param zeit: Zeitspanne in Sekunden
    :return: Beschleunigung bzw. Verzögerung in m/s^2
    """
    if zeit == 0:
        raise ValueError("Die Zeitspanne darf nicht null sein.")

    beschleunigung = (v2 - v1) / zeit
    return beschleunigung


# Beispielanwendung
v1 = 20  # Anfangsgeschwindigkeit in m/s
v2 = 10  # Endgeschwindigkeit in m/s
zeit = 2  # Zeitspanne in Sekunden

beschleunigung = berechne_beschleunigung(v1, v2, zeit)
print(f"Beschleunigung/Verzögerung: {beschleunigung:.2f} m/s^2")
