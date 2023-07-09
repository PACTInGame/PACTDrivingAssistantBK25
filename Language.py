class Language:
    def __init__(self):
        self.translations = {
            'en': {
                'Menu': 'Menu',
                'OutGauge_fail': 'Failed to connect to OutGauge. Maybe it was still active.',
                'Hit the road': 'Waiting for you to hit the road.',
                'Main Menu': 'Main Menu',
                'Driving': 'Driving',
                'Parking': 'Parking',
                'Bus_Sim': 'Bus Simulation',
                'Language': 'Language',
                'Close': 'Close',
            },
            'de': {
                'Menu': 'Men\xfc',
                'Outgauge_fail': 'Verbindung zu OutGauge fehlgeschlagen. Vielleicht war es noch aktiv.',
                'Hit the road': 'Warten auf Spielstart.',
                'Main Menu': 'Hauptmen\xfc',
                'Driving': 'Fahren',
                'Parking': 'Parken',
                'Bus_Sim': 'Bus Simulation',
                'Language': 'Sprache',
                'Close': 'Schlie\xdfen',
            },
            # Add more languages and translations as needed
        }

    def translation(self, language, key):
        if language in self.translations and key in self.translations[language]:
            return self.translations[language][key]
        # Return the key itself if no translation is found
        return key


