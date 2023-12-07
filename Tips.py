import random

tips_en = ["You can use the command $help to get a list of possible commands.",
        "You can switch between miles and kilometers in the general settings.",
        "You can switch off audible parking aid, if you don't like it.",
        "When an update is available, you will be notified with a button above the menu.",
        "You can adjust the HUD height and width offset in the general settings.",
        "You can select a preferred collision warning distance in the settings.",
        "If you like buses, you can enable the offline bus mode, or play online with a bus, and get sound effects and bus specific features.",
        "If you set you car's fuel tank size once in the settings, you can see the fuel consumption in the trip computer.",
        "Any feature requests, or feedback? Contact me via the LFS->Forum->Unofficial Addons->PACT Driving Assistant: lfs.net/forum/thread/102281"]

tips_de = ["Du kannst den Befehl $help benutzen, um eine Liste von möglichen Befehlen zu erhalten.",
        "Du kannst zwischen Meilen und Kilometern in den allgemeinen Einstellungen wechseln.",
        "Du kannst die akustische Einparkhilfe ausschalten, wenn du sie nicht magst.",
        "Wenn ein Update verfügbar ist, wirst du mit einem Button über dem Menü benachrichtigt.",
        "Du kannst den HUD Höhen- und Breitenoffset in den allgemeinen Einstellungen anpassen.",
        "Du kannst in den Einstellungen eine bevorzugte Entfernung für die Kollisionswarnung auswählen.",
        "Wenn du Busse magst, kannst du den Offline-Busmodus aktivieren, oder online auf TC Soundeffekte und Busspezifische Funktionen erhalten.",
        "Wenn du die Tankgröße deines Autos einmal in den Einstellungen eingestellt hast, kannst du den Kraftstoffverbrauch im Bordcomputer sehen.",
        "Irgendwelche Feature-Anfragen oder Feedback? Kontaktiere mich über LFS->Forum->Unofficial Addons->PACT Driving Assistant: lfs.net/forum/thread/102281"]


def get_tip(language):
    if language == "en":
        return random.choice(tips_en)
    elif language == "de":
        return random.choice(tips_de)
