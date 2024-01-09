class CopAssist:
    def __init__(self, game_object):
        self.game_object = game_object
        self.use_indicators = False
        self.use_light = False
        self.use_extra_light = False

    def run(self):
        self.game_object.send_message("CopAssist is running")
        # Example in Test.py
        # TODO: implement