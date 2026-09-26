from manim import *

class VerticalReel(Scene):
    def configurer_camera(self):
        # Configuration automatique du format smartphone
        self.camera.frame_width = 9
        self.camera.frame_height = 16
        
    def overlay_safe_zone(self):
        # Optionnel: ajoute des repères invisibles pour Claude
        pass
