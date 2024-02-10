class Language:
    def __init__(self, game_obj):
        self.game_obj = game_obj
        self.translations = self.get_states()
        # Add more languages and translations as needed

    def get_states(self):
        # TODO check translations outside the menu, bc they seem to be just german lol
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
                'Update': 'Update available',
                'Google_Drive': 'This will forward you to Google Drive. Continue?',
                'Bus_enabled': f'{"^2 Enabled" if self.game_obj.settings.bus_simulation else "^1 Disabled"}',
                'Door_Sound': f'{"^2" if self.game_obj.settings.bus_door_sound else "^1"}Door Sound',
                'Route_Sound': f'{"^2" if self.game_obj.settings.bus_route_sound else "^1"}Route Sound',
                'Announcements': f'{"^2" if self.game_obj.settings.bus_announce_sound else "^1"}Announcements',
                'Sound_effects': f'{"^2" if self.game_obj.settings.bus_sound_effects else "^1"}Sound effects',
                'Start_offline_sim': "^1Stop Simulation" if self.game_obj.settings.bus_offline_sim else "^2Start Simulation",
                'Forward_Collision_Warning': f'{"^2" if self.game_obj.settings.forward_collision_warning else "^1"}Forward Collision Warning',
                'Collision_Warning_Distance': f'{"Close" if self.game_obj.settings.collision_warning_distance == 0 else "Medium" if self.game_obj.settings.collision_warning_distance == 1 else "Far"}',
                'Blind_Spot_Warning': f'{"^2" if self.game_obj.settings.blind_spot_warning else "^1"}Blind Spot Warning',
                'Side_Collision_Prevention': f'{"^2" if self.game_obj.settings.side_collision_prevention else "^1"}Side Collision Prevention',
                'Cross_Traffic_Warning': f'{"^2" if self.game_obj.settings.cross_traffic_warning else "^1"}Cross Traffic Warning',
                'PSC': f'{"^2" if self.game_obj.settings.PSC else "^1"}Stability Control',
                'Light_Assist': f'{"^2" if self.game_obj.settings.light_assist else "^1"}Light Assist',
                'Automatic_Indicator_Turnoff': f'{"^2" if self.game_obj.settings.automatic_indicator_turnoff else "^1"}Automatic Indicator Turnoff',
                'Parking_Emergency_Brake': f'{"^2" if self.game_obj.settings.park_emergency_brake else "^1"}Parking Emergency Brake',
                'Park_Distance_Control': f'{"^2" if self.game_obj.settings.park_distance_control else "^1"}Park Distance Control',
                'Visual_Parking_Aid': f'{"^2" if self.game_obj.settings.visual_parking_aid else "^1"}Visual Parking Aid',
                'Gearbox': f'{"^2" if self.game_obj.settings.automatic_gearbox else "^1"}Automatic Gearbox',
                'General': 'General',
                'Units': 'Units',
                'Metric': 'Metric',
                'Imperial': 'Imperial',
                'HUD': f'{"^2" if self.game_obj.settings.head_up_display else "^1"}Head-Up Display',
                'Board_computer': f'{"^2" if self.game_obj.settings.bc else "^1"}Board Computer',
                'Range': 'Range',
                'Distance': 'Distance',
                'off': 'off',
                'up': 'up',
                'down': 'down',
                'left': 'left',
                'right': 'right',
                'Audible_Parking_Aid': f'{"^2" if self.game_obj.settings.audible_parking_aid else "^1"}Audible Parking Aid',
                'Emergency_Brake': f'{"^2" if self.game_obj.settings.automatic_emergency_braking else "^1"}Braking Intervention',
                'Emergency_Brake_Setting': f'^7{"Warn and Brake" if self.game_obj.settings.automatic_emergency_braking else "Warn only"}',
                'Indicator_Sound': f'{"^2" if self.game_obj.settings.indicator_sound else "^1"}Indicator Sounds',
                'Adaptive_Brake_Light': f'{"^2" if self.game_obj.settings.adaptive_brake_light else "^1"}Adaptive Brake Light',
                'Adaptive_Brake_Light_Style': f'{"^7Indicators" if self.game_obj.settings.adaptive_brake_light_style else "^7Lights"}',
                'Keys_Axes': 'Keys and Axes',
                'All_on': '^7All on',
                'All_off': '^1All off',
                'Cop_Mode': '^4Cop/Rescue',
                'Race_Mode': '^6Race',
                'Strobe': 'Strobe',
                'Siren': 'Siren',
                'Automatic_Siren': f'{"^2" if self.game_obj.settings.automatic_siren else "^1"}Automatic Siren',
                'Use_Indicators': f'{"^2" if self.game_obj.settings.use_indicators else "^1"}Use Indicators',
                'Use_Lights': f'{"^2" if self.game_obj.settings.use_light else "^1"}Use Light',
                'Use_Extra_Light': f'{"^2" if self.game_obj.settings.use_extra_light else "^1"}Use Extra Light',
                'Use_Fog_Light': f'{"^2" if self.game_obj.settings.use_fog_light else "^1"}Use Fog Lights',
                'Track_Suspect': f'{"^2" if self.game_obj.settings.suspect_tracker else "^1"}Suspect Tracker',
                'Shift_Up': 'Shift Up',
                'Shift_Down': 'Shift Down',
                'Ignition': 'Ignition',
                'Handbrake': 'Handbrake',
                'Throttle_Axis': 'Throttle Axis',
                'Brake_Axis': 'Brake Axis',
                'Steer_Axis': 'Steer Axis',
                'Clutch_Axis': 'Clutch Axis',
                'Throttle_Key': 'Throttle Key',
                'Brake_Key': 'Brake Key',
                'Spare_Key1': 'Spare Key 1',
                'Spare_Key2': 'Spare Key 2',
                'Cop_Menu': 'Cop Menu',


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
                'Update': b'Update verf\xfcgbar',
                'Google_Drive': 'Sie werden zu Google Drive weitergeleitet. Fortfahren?',
                'Bus_enabled': f'{"^2 Aktiviert" if self.game_obj.settings.bus_simulation else "^1 Deaktiviert"}',
                'Door_Sound': (b"^2" if self.game_obj.settings.bus_door_sound else b"^1") + b'T\xfcr Sound',
                'Route_Sound': (b"^2" if self.game_obj.settings.bus_route_sound else b"^1")+ b"Linien Ansage",
                'Announcements': f'{"^2" if self.game_obj.settings.bus_announce_sound else "^1"}Halt Ansagen',
                'Sound_effects': f'{"^2" if self.game_obj.settings.bus_sound_effects else "^1"}Soundeffekte',
                'Start_offline_sim': "^1Simulation stoppen" if self.game_obj.settings.bus_offline_sim else "^2Simulation starten",
                'Forward_Collision_Warning': f'{"^2" if self.game_obj.settings.forward_collision_warning else "^1"}Kollisionswarnung',
                'Collision_Warning_Distance': f'{"Nah" if self.game_obj.settings.collision_warning_distance == 0 else "Mittel" if self.game_obj.settings.collision_warning_distance == 1 else "Weit"}',
                'Blind_Spot_Warning': f'{"^2" if self.game_obj.settings.blind_spot_warning else "^1"}Totwinkelwarnung',
                'Side_Collision_Prevention': f'{"^2" if self.game_obj.settings.side_collision_prevention else "^1"}Seitenkollisionsvermeidung',
                'Cross_Traffic_Warning': f'{"^2" if self.game_obj.settings.cross_traffic_warning else "^1"}Querverkehrswarnung',
                'PSC': (b"^2" if self.game_obj.settings.PSC else b"^1")+b"Stabilit\xe4tskontrolle",
                'Light_Assist': f'{"^2" if self.game_obj.settings.light_assist else "^1"}Lichtassistent',
                'Automatic_Indicator_Turnoff': (b"^2" if self.game_obj.settings.automatic_indicator_turnoff else b"^1")+b"Autom. deaktivi. Blinker",
                'Parking_Emergency_Brake': f'{"^2" if self.game_obj.settings.park_emergency_brake else "^1"}Parknotbremsung',
                'Park_Distance_Control': f'{"^2" if self.game_obj.settings.park_distance_control else "^1"}Parkabstandskontrolle',
                'Visual_Parking_Aid': f'{"^2" if self.game_obj.settings.visual_parking_aid else "^1"}Visuelle Parkhilfe',
                'Gearbox': f'{"^2" if self.game_obj.settings.automatic_gearbox else "^1"}Automatikgetriebe',
                'General': 'Allgemein',
                'Units': 'Einheiten',
                'Metric': 'Metrisch',
                'Imperial': 'Imperial',
                'HUD': f'{"^2" if self.game_obj.settings.head_up_display else "^1"}Head-Up Display',
                'Board_computer': f'{"^2" if self.game_obj.settings.bc else "^1"}Bordcomputer',
                'Range': 'Reichweite',
                'Distance': 'Distanz',
                'off': 'aus',
                'up': 'hoch',
                'down': 'runter',
                'left': 'links',
                'right': 'rechts',
                'Audible_Parking_Aid': f'{"^2" if self.game_obj.settings.audible_parking_aid else "^1"}Akustische Parkhilfe',
                'Emergency_Brake': f'{"^2" if self.game_obj.settings.automatic_emergency_braking else "^1"}Bremseingriff',
                'Emergency_Brake_Setting': f'^7{"Warnung und Bremsung" if self.game_obj.settings.automatic_emergency_braking else "Nur Warnung"}',
                'Indicator_Sound': f'{"^2" if self.game_obj.settings.indicator_sound else "^1"}Blinkersound',
                'Adaptive_Brake_Light': f'{"^2" if self.game_obj.settings.adaptive_brake_light else "^1"}Adaptives Bremslicht',
                'Adaptive_Brake_Light_Style': f'{"^7Blinker" if self.game_obj.settings.adaptive_brake_light_style else "^7Lichter"}',
                'Keys_Axes': 'Tasten und Achsen',
                'All_on': '^7Alle aktiv',
                'All_off': '^1Alles aus',
                'Cop_Mode': '^4Einsatzfahrzeug',
                'Race_Mode': '^6Rennen',
                'Strobe': 'Blaulicht',
                'Siren': 'Horn',
                'Automatic_Siren': f'{"^2" if self.game_obj.settings.automatic_siren else "^1"}Automatisches Horn',
                'Use_Indicators': f'{"^2" if self.game_obj.settings.use_indicators else "^1"}Blinker verw.',
                'Use_Lights': f'{"^2" if self.game_obj.settings.use_light else "^1"}Licht verw.',
                'Use_Extra_Light': f'{"^2" if self.game_obj.settings.use_extra_light else "^1"}Zusatzlicht verw.',
                'Use_Fog_Light': f'{"^2" if self.game_obj.settings.use_fog_light else "^1"}Nebellicht verw.',
                'Track_Suspect': f'{"^2" if self.game_obj.settings.suspect_tracker else "^1"}Suspect Tracker',
                'Shift_Up': 'Hochschalten',
                'Shift_Down': 'Runterschalten',
                'Ignition': b'Z\xfcndung',
                'Handbrake': 'Handbremse',
                'Throttle_Axis': 'Gas Achse',
                'Brake_Axis': 'Brems Achse',
                'Steer_Axis': 'Lenk Achse',
                'Clutch_Axis': 'Kupplung Achse',
                'Throttle_Key': 'Gas Taste',
                'Brake_Key': 'Brems Taste',
                'Spare_Key1': 'Leere Taste 1',
                'Spare_Key2': 'Leere Taste 2',
                'Cop_Menu': b'Cop Men\xfc',

                # TODO FIX OTHER LANGUAGES WITH SONDERZEICHEN
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
                'Forward_Collision_Warning': f'{"^2" if self.game_obj.settings.forward_collision_warning else "^1"}Avertissement de collision frontale',
                'Collision_Warning_Distance': f'{"Proche" if self.game_obj.settings.collision_warning_distance == 0 else "Moyen" if self.game_obj.settings.collision_warning_distance == 1 else "Loin"}',
                'Blind_Spot_Warning': f'{"^2" if self.game_obj.settings.blind_spot_warning else "^1"}Avertissement d\'angle mort',
                'Side_Collision_Prevention': b"^2Pr\xe9vention des collisions lat\xe9rales" if self.game_obj.settings.side_collision_prevention else b"^1Pr\xe9vention des collisions lat\xe9rales",
                'Cross_Traffic_Warning': f'{"^2" if self.game_obj.settings.cross_traffic_warning else "^1"}Avertissement de circulation transversale',
                'PSC': b"^2Contr\xf4le de stabilit\xe9" if self.game_obj.settings.PSC else b"^1Contr\xf4le de stabilit\xe9",
                'Light_Assist': f'{"^2" if self.game_obj.settings.light_assist else "^1"}Assistance lumineuse',
                'Automatic_Indicator_Turnoff': f'{"^2" if self.game_obj.settings.automatic_indicator_turnoff else "^1"}Extinction automatique des indicateurs',
                'Parking_Emergency_Brake': f'{"^2" if self.game_obj.settings.park_emergency_brake else "^1"}Frein de stationnement d\'urgence',
                'Park_Distance_Control': b"^2Contr\xf4le de distance de stationnement" if self.game_obj.settings.park_distance_control else b"^1Contr\xf4le de distance de stationnement",
                'Visual_Parking_Aid': f'{"^2" if self.game_obj.settings.visual_parking_aid else "^1"}Aide au stationnement visuelle',
                'Gearbox': b"^2Bo\xeete de vitesses automatique" if self.game_obj.settings.automatic_gearbox else b"^1Bo\xeete de vitesses automatique",
                'General': b'G\xe9n\xe9ral',
                'Units': b'Unit\xe9s',
                'Metric': b'M\xe9trique',
                'Imperial': b'Imp\xe9rial',
                'HUD': b"^2Affichage t\xeate haute" if self.game_obj.settings.head_up_display else b"^1Affichage t\xeate haute",
                'Board_computer': f'{"^2" if self.game_obj.settings.bc else "^1"}Ordinateur de bord',
                'Range': b'Port\xe9e',
                'Distance': 'Distance',
                'off': 'off',
                'up': 'haut',
                'down': 'bas',
                'left': 'gauche',
                'right': 'droite',
                'Audible_Parking_Aid': f'{"^2" if self.game_obj.settings.audible_parking_aid else "^1"}Aide au stationnement sonore',
                'Emergency_Brake': f'{"^2" if self.game_obj.settings.automatic_emergency_braking else "^1"}Intervention de freinage',
                'Emergency_Brake_Setting': f'^7{"Avertissement et freinage" if self.game_obj.settings.automatic_emergency_braking else "Avertissement uniquement"}',
                'Indicator_Sound': f'{"^2" if self.game_obj.settings.indicator_sound else "^1"}Son des indicateurs',
                'Adaptive_Brake_Light': f'{"^2" if self.game_obj.settings.adaptive_brake_light else "^1"}Feu stop adaptatif',
                'Adaptive_Brake_Light_Style': f'{"^7Clignotants" if self.game_obj.settings.adaptive_brake_light_style else "^7Feux"}',
                'Keys_Axes': 'Touches et axes',
                'All_on': b'^7Tout activ\xe9',
                'All_off': b'^1Tout d\xe9sactiv\xe9',
                'Cop_Mode': '^4Police/Secours',
                'Race_Mode': '^6Course',
                'Strobe': 'Stroboscope',
                'Siren': b'Sir\xe8ne',
                'Automatic_Siren': b"^2Sir\xe8ne automatique" if self.game_obj.settings.automatic_siren else b"^1Sir\xe8ne automatique",
                'Use_Indicators': f'{"^2" if self.game_obj.settings.use_indicators else "^1"}Util. des indicateurs',
                'Use_Lights': f'{"^2" if self.game_obj.settings.use_light else "^1"}Util. des feux',
                'Use_Extra_Light': f'{"^2" if self.game_obj.settings.use_extra_light else "^1"}Util. des feux de route',
                'Use_Fog_Light': f'{"^2" if self.game_obj.settings.use_fog_light else "^1"}Util. des feux de brouillard',
                'Track_Suspect': f'{"^2" if self.game_obj.settings.suspect_tracker else "^1"}Suivi du suspect',
                'Shift_Up': b'Passer \xe0 la vitesse sup\xe9rieure',
                'Shift_Down': b'Passer \xe0 la vitesse inf\xe9rieure',
                'Ignition': 'Allumage',
                'Handbrake': 'Frein',
                'Throttle_Axis': 'Axe des gaz',
                'Brake_Axis': 'Axe de frein',
                'Steer_Axis': 'Axe de direction',
                'Clutch_Axis': 'Axe d\'embrayage',
                'Throttle_Key': 'Touches des gaz',
                'Brake_Key': 'Touches de frein',
                'Spare_Key1': 'Touches libres 1',
                'Spare_Key2': 'Touches libres 2',
                'Cop_Menu': 'Menu de police',


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
                'Forward_Collision_Warning': f'{"^2" if self.game_obj.settings.forward_collision_warning else "^1"}Advertencia de colisi\xf3n frontal',
                'Collision_Warning_Distance': f'{"Cerca" if self.game_obj.settings.collision_warning_distance == 0 else "Medio" if self.game_obj.settings.collision_warning_distance == 1 else "Lejos"}',
                'Blind_Spot_Warning': f'{"^2" if self.game_obj.settings.blind_spot_warning else "^1"}Advertencia de punto ciego',
                'Side_Collision_Prevention': f'{"^2" if self.game_obj.settings.side_collision_prevention else "^1"}Prevenci\xf3n de colisi\xf3n lateral',
                'Cross_Traffic_Warning': f'{"^2" if self.game_obj.settings.cross_traffic_warning else "^1"}Advertencia de tr\xe1fico cruzado',
                'PSC': f'{"^2" if self.game_obj.settings.PSC else "^1"}Control de estabilidad',
                'Light_Assist': f'{"^2" if self.game_obj.settings.light_assist else "^1"}Asistencia de luz',
                'Automatic_Indicator_Turnoff': f'{"^2" if self.game_obj.settings.automatic_indicator_turnoff else "^1"}Apagado autom\xe1tico del indicador',
                'Parking_Emergency_Brake': f'{"^2" if self.game_obj.settings.park_emergency_brake else "^1"}Freno de emergencia de estacionamiento',
                'Park_Distance_Control': f'{"^2" if self.game_obj.settings.park_distance_control else "^1"}Control de distancia de estacionamiento',
                'Visual_Parking_Aid': f'{"^2" if self.game_obj.settings.visual_parking_aid else "^1"}Ayuda de estacionamiento visual',
                'Gearbox': f'{"^2" if self.game_obj.settings.automatic_gearbox else "^1"}Caja de cambios autom\xe1tica',
                'General': b'General',
                'Units': b'Unidades',
                'Metric': b'M\xe9trico',
                'Imperial': b'Imperial',
                'HUD': b"^2 Pantalla frontal" if self.game_obj.settings.head_up_display else b"^1 Pantalla frontal",
                'Board_computer': f'{"^2" if self.game_obj.settings.bc else "^1"}Ordenador de a bordo',
                'Range': b'Alcance',
                'Distance': b'Distancia',
                'off': b'apagado',
                'up': b'arriba',
                'down': b'abajo',
                'left': b'izquierda',
                'right': b'derecha',
                'Audible_Parking_Aid': f'{"^2" if self.game_obj.settings.audible_parking_aid else "^1"}Ayuda de estacionamiento audible',
                'Emergency_Brake': f'{"^2" if self.game_obj.settings.automatic_emergency_braking else "^1"}Intervenci\xf3n de frenado',
                'Emergency_Brake_Setting': f'^7{"Advertir y frenar" if self.game_obj.settings.automatic_emergency_braking else "Solo advertir"}',
                'Indicator_Sound': f'{"^2" if self.game_obj.settings.indicator_sound else "^1"}Sonido del indicador',
                'Adaptive_Brake_Light': f'{"^2" if self.game_obj.settings.adaptive_brake_light else "^1"}Luz de freno adaptativa',
                'Adaptive_Brake_Light_Style': f'{"^7Intermitentes" if self.game_obj.settings.adaptive_brake_light_style else "^7Luces"}',
                'Keys_Axes': b'Teclas y ejes',
                'All_on': b'^7Todo activado',
                'All_off': b'^1Todo desactivado',
                'Cop_Mode': b'^4Polic\xeda/Rescate',
                'Race_Mode': b'^6Carrera',
                'Strobe': b'Estrobosc\xf3pico',
                'Siren': b'Sirena',
                'Automatic_Siren': b"^2Sirena autom\xe1tica" if self.game_obj.settings.automatic_siren else b"^1Sirena autom\xe1tica",
                'Use_Indicators': f'{"^2" if self.game_obj.settings.use_indicators else "^1"}Usar indicadores',
                'Use_Lights': f'{"^2" if self.game_obj.settings.use_light else "^1"}Usar luz',
                'Use_Extra_Light': f'{"^2" if self.game_obj.settings.use_extra_light else "^1"}Usar luz extra',
                'Use_Fog_Light': f'{"^2" if self.game_obj.settings.use_fog_light else "^1"}Usar luces antiniebla',
                'Track_Suspect': f'{"^2" if self.game_obj.settings.suspect_tracker else "^1"}Seguimiento de sospechosos',
                'Shift_Up': b'Subir de marcha',
                'Shift_Down': b'Bajar de marcha',
                'Ignition': b'Encend',
                'Handbrake': b'Freno de mano',
                'Throttle_Axis': b'Eje del acelerador',
                'Brake_Axis': b'Eje de freno',
                'Steer_Axis': b'Eje de direcci\xf3n',
                'Clutch_Axis': b'Eje del embrague',
                'Throttle_Key': b'Tecla del acelerador',
                'Brake_Key': b'Tecla de freno',
                'Spare_Key1': b'Tecla de repuesto 1',
                'Spare_Key2': b'Tecla de repuesto 2',
                'Cop_Menu': b'Men\xfa de polic\xeda',


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
                'Forward_Collision_Warning': f'{"^2" if self.game_obj.settings.forward_collision_warning else "^1"}Avviso di collisione frontale',
                'Collision_Warning_Distance': f'{"Vicino" if self.game_obj.settings.collision_warning_distance == 0 else "Medio" if self.game_obj.settings.collision_warning_distance == 1 else "Lontano"}',
                'Blind_Spot_Warning': f'{"^2" if self.game_obj.settings.blind_spot_warning else "^1"}Avviso di punto cieco',
                'Side_Collision_Prevention': f'{"^2" if self.game_obj.settings.side_collision_prevention else "^1"}Prevenzione delle collisioni laterali',
                'Cross_Traffic_Warning': f'{"^2" if self.game_obj.settings.cross_traffic_warning else "^1"}Avviso di traffico incrociato',
                'PSC': f'{"^2" if self.game_obj.settings.PSC else "^1"}Controllo di stabilit\xe0',
                'Light_Assist': f'{"^2" if self.game_obj.settings.light_assist else "^1"}Assistente di luce',
                'Automatic_Indicator_Turnoff': f'{"^2" if self.game_obj.settings.automatic_indicator_turnoff else "^1"}Spegnimento automatico dell\'indicatore',

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
                'Forward_Collision_Warning': f'{"^2" if self.game_obj.settings.forward_collision_warning else "^1"}\xf6n \xe7arpma uyar\xfds\xfd',
                'Collision_Warning_Distance': f'{"Yakin" if self.game_obj.settings.collision_warning_distance == 0 else "Orta" if self.game_obj.settings.collision_warning_distance == 1 else "Uzak"}',
                'Blind_Spot_Warning': f'{"^2" if self.game_obj.settings.blind_spot_warning else "^1"}K\xf6r nokta uyar\xfds\xfd',
                'Side_Collision_Prevention': f'{"^2" if self.game_obj.settings.side_collision_prevention else "^1"}Yan \xe7arpma \xf6nleme',
                'Cross_Traffic_Warning': f'{"^2" if self.game_obj.settings.cross_traffic_warning else "^1"}Trafik uyar\xfds\xfd',
                'PSC': f'{"^2" if self.game_obj.settings.PSC else "^1"}Stabilite kontrol\xfc',
                'Light_Assist': f'{"^2" if self.game_obj.settings.light_assist else "^1"}I\xfe\xfdk asistan\xfd',
                'Automatic_Indicator_Turnoff': f'{"^2" if self.game_obj.settings.automatic_indicator_turnoff else "^1"}Otomatik sinyal iptali',

            },
        }
        return translations

    def translation(self, language, key):
        self.translations = self.get_states()

        if language in self.translations and key in self.translations[language]:
            return self.translations[language][key]
        # Return the key itself if no translation is found

        return key
