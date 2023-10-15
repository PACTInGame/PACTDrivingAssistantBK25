class Language:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.translations = self.get_states()
        # Add more languages and translations as needed

    def get_states(self):
        translations = {
            'en': {
                'Menu': 'Menu',
                'OutGauge_fail': 'Failed to connect to OutGauge. Maybe it was still active.',
                'Hit the road': 'Waiting for you to hit the road.',
                'Main Menu': 'Main Menu',
                'Driving': 'Driving',
                'Parking': 'Parking',
                'Bus_Sim': 'Bus Simulation',
                'Language': f'Language: English',
                'Close': '^1Close',
                'Bus_Menu': 'Bus Menu',
                'Bus_enabled': f'{"^2 Enabled" if self.game_obj.settings.bus_simulation else "^1 Disabled"}',
                'Door_Sound': f'{"^2" if self.game_obj.settings.bus_door_sound else "^1"}Door Sound',
                'Route_Sound': f'{"^2" if self.game_obj.settings.bus_route_sound else "^1"}Route Sound',
                'Announcements': f'{"^2" if self.game_obj.settings.bus_announce_sound else "^1"}Announcements',
                'Sound_effects': f'{"^2" if self.game_obj.settings.bus_sound_effects else "^1"}Sound effects',
                'Start_offline_sim': "^1Stop Simulation" if self.game_obj.settings.bus_offline_sim else "^2Start Simulation",

            },
            'de': {
                'Menu': b'Men\xfc',
                'Outgauge_fail': 'Verbindung zu OutGauge fehlgeschlagen. Vielleicht war es noch aktiv.',
                'Hit the road': 'Warten auf Spielstart.',
                'Main Menu': b'Hauptmen\xfc',
                'Driving': 'Fahren',
                'Parking': 'Parken',
                'Bus_Sim': 'Bussimulation',
                'Language': 'Sprache: Deutsch',
                'Close': b'^1Schlie\xdfen',
                'Bus_Menu': b'Bus Men\xfc',
                'Bus_enabled': f'{"^2 Aktiviert" if self.game_obj.settings.bus_simulation else "^1 Deaktiviert"}',
                'Door_Sound': (b"^2" if self.game_obj.settings.bus_door_sound else b"^1") + b'T\xfcr Sound',
                'Route_Sound': f'{"^2" if self.game_obj.settings.bus_route_sound else "^1"}Linien Ansage',
                'Announcements': f'{"^2" if self.game_obj.settings.bus_announce_sound else "^1"}Halt Ansagen',
                'Sound_effects': f'{"^2" if self.game_obj.settings.bus_sound_effects else "^1"}Soundeffekte',
                'Start_offline_sim': "^1Simulation stoppen" if self.game_obj.settings.bus_offline_sim else "^2Simulation starten",

            },
            'fr': {
                'Menu': 'Menu',
                'Outgauge_fail': b'Impossible de se connecter \xe0 OutGauge. Peut-\xeatre qu\'il \xe9tait encore actif.',
                'Hit the road': b'En attente de votre d\xe9part.',
                'Main Menu': 'Menu principal',
                'Driving': 'Conduite',
                'Parking': 'Stationnement',
                'Bus_Sim': 'Simulation de bus',
                'Language': b'Langue: Fran\xe7ais',
                'Close': '^1Fermer',
                'Bus_Menu': b'Menu du bus',
                'Bus_enabled': b"^2 Activ\xe9" if self.game_obj.settings.bus_simulation else b"^1 D\xe9sactiv\xe9",
                'Door_Sound': "^2" if self.game_obj.settings.bus_door_sound else "^1" + 'Son de porte',
                'Route_Sound': "^2" if self.game_obj.settings.bus_route_sound else "^1" + 'Son de route',
                'Announcements': "^2" if self.game_obj.settings.bus_announce_sound else "^1" + 'Annonces',
                'Sound_effects': "^2" if self.game_obj.settings.bus_sound_effects else "^1" + 'Effets sonores',
                'Start_offline_sim': b"^1Arr\xeat de la simulation" if self.game_obj.settings.bus_offline_sim else b"^2D\xe9marrer la simulation",

            },
            'es': {
                'Menu': b'Men\xfa',
                'Outgauge_fail': b'No se pudo conectar a OutGauge. Tal vez todav\xeda estaba activo.',
                'Hit the road': b'Esperando que salgas a la carretera.',
                'Main Menu': b'Men\xfa principal',
                'Driving': b'Conducci\xf3n',
                'Parking': b'Estacionamiento',
                'Bus_Sim': b'Simulaci\xf3n de autob\xfases',
                'Language': b'Idioma: Espa\xf1ol',
                'Close': b'^1Cerrar',
                'Bus_Menu': b'Men\xfa de autob\xfases',
                'Bus_enabled': b"^2 Habilitado" if self.game_obj.settings.bus_simulation else b"^1 Deshabilitado",
                'Door_Sound': b"^2" if self.game_obj.settings.bus_door_sound else b"^1" + b'Sonido de puerta',
                'Route_Sound': b"^2" if self.game_obj.settings.bus_route_sound else b"^1" + b'Sonido de ruta',
                'Announcements': b"^2" if self.game_obj.settings.bus_announce_sound else b"^1" + b'Anuncios',
                'Sound_effects': b"^2" if self.game_obj.settings.bus_sound_effects else b"^1" + b'efectos de sonido',
                'Start_offline_sim': b"^1Detener simulaci\xf3n" if self.game_obj.settings.bus_offline_sim else b"^2Iniciar simulaci\xf3n",

            },
            'it': {
                'Menu': 'Menu',
                'Outgauge_fail': b'Impossibile connettersi a OutGauge. Forse era ancora attivo.',
                'Hit the road': b'In attesa che tu colpisca la strada.',
                'Main Menu': b'Menu principale',
                'Driving': b'Guida',
                'Parking': b'Parcheggio',
                'Bus_Sim': b'Simulazione bus',
                'Language': b'Lingua: Italiano',
                'Close': b'^1Chiudi',
                'Bus_Menu': b'Menu bus',
                'Bus_enabled': b"^2 Abilitato" if self.game_obj.settings.bus_simulation else b"^1 Disabilitato",
                'Door_Sound': b"^2" if self.game_obj.settings.bus_door_sound else b"^1" + b'Suono della porta',
                'Route_Sound': b"^2" if self.game_obj.settings.bus_route_sound else b"^1" + b'Suono della strada',
                'Announcements': b"^2" if self.game_obj.settings.bus_announce_sound else b"^1" + b'Annunci',
                'Sound_effects': b"^2" if self.game_obj.settings.bus_sound_effects else b"^1" + b'Effetti sonori',
                'Start_offline_sim': b"^1Arresta la simulazione" if self.game_obj.settings.bus_offline_sim else b"^2Avvia la simulazione",
            },
            'tr': {
                'Menu': b'Men\xfc',
                'Outgauge_fail': b'OutGauge \xe7al\xfd\xfeamad\xfd. Belki de hala aktifti.',
                'Hit the road': b'Yolda vurman\xfd bekliyor.',
                'Main Menu': b'Ana Men\xfc',
                'Driving': b'S\xfcrme',
                'Parking': b'Park',
                'Bus_Sim': b'Otob\xfcs Sim\xfclasyonu',
                'Language': b'Dil: T\xfcrk\xe7e',
                'Close': b'^1Kapat',
                'Bus_Menu': b'Otob\xfcs Men\xfc',
                'Bus_enabled': b"^2 Etkin" if self.game_obj.settings.bus_simulation else b"^1 Devre d\xfe\xfd",
                'Door_Sound': b"^2" if self.game_obj.settings.bus_door_sound else b"^1" + b'Kap\xfd sesi',
                'Route_Sound': b"^2" if self.game_obj.settings.bus_route_sound else b"^1" + b'Yol sesi',
                'Announcements': b"^2" if self.game_obj.settings.bus_announce_sound else b"^1" + b'Duyurular',
                'Sound_effects': b"^2" if self.game_obj.settings.bus_sound_effects else b"^1" + b'Ses efektleri',
                'Start_offline_sim': b"^1Sim\xfclasyonu durdur" if self.game_obj.settings.bus_offline_sim else b"^2Sim\xfclasyonu ba\xfelat",

            },
        }
        return translations

    def translation(self, language, key):
        self.translations = self.get_states()

        if language in self.translations and key in self.translations[language]:
            return self.translations[language][key]
        # Return the key itself if no translation is found

        return key
