"""
Reel Instagram - Dilatance
Concept: Fluide non newtonien qui durcit au choc
Format vertical 9:16 (1080x1920 @ 60fps) - Safe Zone centrée
Généré automatiquement le 2026-09-26 11:28
"""

from manim import *
import numpy as np

# ─── Configuration Reel Instagram 9:16 ───
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.background_color = "#0F0F1A"

# ─── Constantes Safe Zone ───
SAFE_ZONE_TOP = config.frame_height * 0.15
SAFE_ZONE_BOTTOM = config.frame_height * 0.15
SAFE_ZONE_SIDES = config.frame_width * 0.10

SAFE_TOP = config.frame_height / 2 - SAFE_ZONE_TOP
SAFE_BOTTOM = -config.frame_height / 2 + SAFE_ZONE_BOTTOM
SAFE_LEFT = -config.frame_width / 2 + SAFE_ZONE_SIDES
SAFE_RIGHT = config.frame_width / 2 - SAFE_ZONE_SIDES
SAFE_CENTER = ORIGIN
SAFE_WIDTH = SAFE_RIGHT - SAFE_LEFT
SAFE_HEIGHT = SAFE_TOP - SAFE_BOTTOM


class Reel068(Scene):
    """Reel 60s - Dilatance - Format 9:16"""

    # Couleur principale injectée
    COULEUR_PRINCIPALE = "#EC4899"
    COULEUR_ACCENT = "#FF2A93"
    COULEUR_SECONDAIRE = "#EC4848"

    def construct(self):
        colors = {
            "bg": "#0F0F1A",
            "white": "#FFFFFF",
            "primary": self.COULEUR_PRINCIPALE,
            "accent": self.COULEUR_ACCENT,
            "secondary": self.COULEUR_SECONDAIRE,
            "gray": "#64748B",
            "yellow": "#EAB308",
        }

        # ═══════════════════════════════════════════════════════
        # SCÈNE 1 : HOOK (0-5s)
        # ═══════════════════════════════════════════════════════
        titre_hook = Text(
            "La physique derrière Dilatance",
            font_size=56,
            weight=BOLD,
            color=colors["white"],
        ).move_to(SAFE_CENTER + UP * 2.5)

        sous_titre = Text(
            "Fluide non newtonien qui durcit au choc",
            font_size=32,
            color=colors["gray"],
        ).next_to(titre_hook, DOWN, buff=0.4)

        self.play(
            Write(titre_hook, run_time=1.5),
            FadeIn(sous_titre, shift=UP * 0.3, run_time=1),
        )
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════
        # SCÈNE 2 : VISUALISATION PRINCIPALE (5-25s)
        # ═══════════════════════════════════════════════════════
        self.play(
            FadeOut(titre_hook, shift=UP * 0.5, run_time=0.5),
            FadeOut(sous_titre, shift=UP * 0.5, run_time=0.5),
        )

        # Construction de la visualisation centrale
        visualisation = self._creer_visualisation(colors)
        visualisation.move_to(SAFE_CENTER)

        self.play(Create(visualisation, run_time=3, rate_func=smooth))
        self.wait(1)

        # Animation dynamique selon le concept
        self._animer_concept(visualisation, colors)
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════
        # SCÈNE 3 : FORMULE / RÉSULTAT CLÉ (25-40s)
        # ═══════════════════════════════════════════════════════
        formule = self._creer_formule_cle(colors)
        self.play(
            FadeOut(visualisation, run_time=0.8),
            Write(formule, run_time=2),
        )
        self.wait(1.5)

        # ═══════════════════════════════════════════════════════
        # SCÈNE 4 : OUTRO (40-60s)
        # ═══════════════════════════════════════════════════════
        self.play(FadeOut(formule, run_time=0.5))

        outro = VGroup(
            Text("Les maths, c'est visuel 🧠", font_size=48, weight=BOLD, color=colors["white"]),
            Text("Abonne-toi pour plus !", font_size=32, color=colors["accent"]),
        ).arrange(DOWN, buff=0.4).move_to(SAFE_CENTER)

        self.play(
            Write(outro[0], run_time=1),
            FadeIn(outro[1], shift=UP * 0.3, run_time=0.8),
        )
        self.wait(1)

    # ─── MÉTHODES À PERSONNALISER SELON LE CONCEPT ───

    def _creer_visualisation(self, colors):
        """Crée la visualisation centrale - À ADAPTER selon le concept"""
        # Par défaut : cercle pulsant avec la couleur principale
        cercle = Circle(radius=2, color=colors["primary"], stroke_width=6)
        cercle.set_fill(colors["primary"], opacity=0.15)

        label = Text("Fluide non newtonien qui durcit au choc", font_size=36, color=colors["white"]).next_to(cercle, DOWN, buff=0.5)

        return VGroup(cercle, label)

    def _animer_concept(self, visualisation, colors):
        """Animation dynamique du concept - À ADAPTER"""
        cercle = visualisation[0]
        # Animation par défaut : pulsation + rotation
        self.play(
            cercle.animate.scale(1.3).set_fill(colors["primary"], opacity=0.3),
            rate_func=there_and_back,
            run_time=2,
        )
        self.play(Rotate(cercle, angle=PI, run_time=2, rate_func=smooth))
        self.play(
            cercle.animate.scale(1/1.3).set_fill(colors["primary"], opacity=0.15),
            rate_func=smooth,
            run_time=1,
        )

    def _creer_formule_cle(self, colors):
        """Formule ou résultat clé - À ADAPTER"""
        formule = MathTex(
            r"	ext{Concept cl'e}", r"ightarrow", r"	ext{R'esultat}",
            font_size=64,
            color=colors["white"],
        )
        formule[0].set_color(colors["primary"])
        formule[2].set_color(colors["accent"])

        box = SurroundingRectangle(
            formule,
            color=colors["yellow"],
            stroke_width=4,
            buff=0.5,
            corner_radius=0.2,
        )
        box.set_fill(colors["bg"], opacity=0.9)

        groupe = VGroup(box, formule)
        groupe.move_to(SAFE_CENTER)
        return groupe


# ─── RENDU LIGNE DE COMMANDE ───
# manim -pqh generated_reels/Reel_{id}_{titre}.py Reel{id}
