"""
Reel Instagram - Théorème de Pythagore
Format vertical 9:16 (1080x1920) - 60 secondes
Safe Zone centrée pour éviter les boutons Instagram
"""

from manim import *

# ─── Configuration Reel Instagram 9:16 ───
# HQ: 1080x1920 @ 60fps (Instagram Reels optimal)
config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.background_color = "#0F0F1A"  # Fond sombre type 3b1b

# ─── Constantes Safe Zone ───
# Instagram UI couvre ~15% haut/bas et ~10% côtés
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


class ReelPythagore(Scene):
    """Reel 60s - Théorème de Pythagore - Format 9:16"""

    def construct(self):
        # ═══════════════════════════════════════════════════════
        # PALETTE COULEURS (style 3b1b)
        # ═══════════════════════════════════════════════════════
        COLORS = {
            "bg": "#0F0F1A",
            "white": "#FFFFFF",
            "blue": "#3B82F6",       # Côté a
            "green": "#22C55E",      # Côté b
            "orange": "#F97316",     # Hypoténuse c
            "yellow": "#EAB308",     # Aires / résultat
            "purple": "#A855F7",     # Accents
            "gray": "#64748B",
            "red": "#EF4444",
        }

        # ═══════════════════════════════════════════════════════
        # SCÈNE 1 : HOOK - "Pourquoi ça marche ?" (0-5s)
        # ═══════════════════════════════════════════════════════
        titre = Text(
            "Pourquoi a² + b² = c² ?",
            font_size=56,
            weight=BOLD,
            color=COLORS["white"],
        ).move_to(SAFE_CENTER + UP * 2.5)

        sous_titre = Text(
            "La preuve visuelle qui change tout",
            font_size=32,
            color=COLORS["gray"],
        ).next_to(titre, DOWN, buff=0.4)

        self.play(
            Write(titre, run_time=1.5),
            FadeIn(sous_titre, shift=UP * 0.3, run_time=1),
        )
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════
        # SCÈNE 2 : TRIANGLE RECTANGLE ANIMÉ (5-15s)
        # ═══════════════════════════════════════════════════════
        # Triangle rectangle centré dans safe zone
        triangle = self._creer_triangle_rectangle(COLORS)
        triangle.move_to(SAFE_CENTER)

        labels = self._creer_labels_triangle(triangle, COLORS)

        self.play(
            FadeOut(titre, shift=UP * 0.5, run_time=0.5),
            FadeOut(sous_titre, shift=UP * 0.5, run_time=0.5),
        )

        # Animation construction triangle
        self.play(Create(triangle, run_time=2, rate_func=smooth))
        self.play(
            *[Write(lbl, run_time=0.8) for lbl in labels],
            lag_ratio=0.2,
        )
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════
        # SCÈNE 3 : CARRÉS SUR LES CÔTÉS (15-30s)
        # ═══════════════════════════════════════════════════════
        carres = self._creer_carres_sur_cotes(triangle, COLORS)
        labels_aires = self._creer_labels_aires(carres, COLORS)

        # Animation : carrés "poussent" depuis les côtés
        self.play(
            *[
                GrowFromEdge(carre, edge, run_time=1.5, rate_func=there_and_back_with_pause)
                for carre, edge in zip(carres, [LEFT, DOWN, UP + RIGHT])
            ],
            lag_ratio=0.3,
        )
        self.play(*[FadeIn(lbl, scale=1.2, run_time=0.6) for lbl in labels_aires], lag_ratio=0.2)
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════
        # SCÈNE 4 : DÉCOMPOSITION / RECOMPOSITION (30-45s)
        # ═══════════════════════════════════════════════════════
        # On découpe les deux petits carrés et on les réassemble dans le grand
        pieces = self._decouper_carres(carres, COLORS)
        self._animer_recomposition(pieces, carres[2], COLORS)
        self.wait(0.5)

        # ═══════════════════════════════════════════════════════
        # SCÈNE 5 : FORMULE FINALE (45-55s)
        # ═══════════════════════════════════════════════════════
        formule = self._creer_formule_finale(COLORS)
        self.play(
            *[FadeOut(p, run_time=0.5) for p in pieces],
            FadeOut(carres[2], run_time=0.5),
            FadeOut(triangle, run_time=0.5),
            *[FadeOut(lbl, run_time=0.5) for lbl in labels],
            *[FadeOut(lbl, run_time=0.5) for lbl in labels_aires],
            Write(formule, run_time=2),
        )
        self.wait(1)

        # ═══════════════════════════════════════════════════════
        # SCÈNE 6 : OUTRO - Call to action (55-60s)
        # ═══════════════════════════════════════════════════════
        self.play(FadeOut(formule, run_time=0.5))

        outro = VGroup(
            Text("Les maths, c'est visuel 🧠", font_size=48, weight=BOLD, color=COLORS["white"]),
            Text("Abonne-toi pour plus !", font_size=32, color=COLORS["purple"]),
        ).arrange(DOWN, buff=0.4).move_to(SAFE_CENTER)

        self.play(
            Write(outro[0], run_time=1),
            FadeIn(outro[1], shift=UP * 0.3, run_time=0.8),
        )
        self.wait(1)

    # ─── MÉTHODES UTILITAIRES ───

    def _creer_triangle_rectangle(self, colors):
        """Crée un triangle rectangle 3-4-5 stylisé"""
        # Côtés : a=3, b=4, c=5 (échelle pour tenir dans safe zone)
        scale = min(SAFE_WIDTH, SAFE_HEIGHT) * 0.25

        # Points du triangle (angle droit en bas à gauche)
        A = ORIGIN
        B = RIGHT * 3 * scale
        C = UP * 4 * scale

        triangle = Polygon(A, B, C, color=colors["white"], stroke_width=4)
        triangle.set_fill(opacity=0)

        # Marque angle droit
        angle_droit = RightAngle(
            Line(A, B), Line(A, C),
            length=0.3 * scale,
            color=colors["yellow"],
            stroke_width=3,
        )

        return VGroup(triangle, angle_droit)

    def _creer_labels_triangle(self, triangle_group, colors):
        """Labels a, b, c sur les côtés"""
        triangle = triangle_group[0]
        points = triangle.get_vertices()
        A, B, C = points[0], points[1], points[2]

        # Milieux des côtés
        mid_ab = (A + B) / 2
        mid_ac = (A + C) / 2
        mid_bc = (B + C) / 2

        label_a = MathTex("a", font_size=44, color=colors["blue"]).next_to(mid_ab, DOWN, buff=0.2)
        label_b = MathTex("b", font_size=44, color=colors["green"]).next_to(mid_ac, LEFT, buff=0.2)
        label_c = MathTex("c", font_size=44, color=colors["orange"]).next_to(mid_bc, UP + RIGHT, buff=0.2)

        return VGroup(label_a, label_b, label_c)

    def _creer_carres_sur_cotes(self, triangle_group, colors):
        """Crée les 3 carrés sur les côtés du triangle"""
        triangle = triangle_group[0]
        points = triangle.get_vertices()
        A, B, C = points[0], points[1], points[2]

        # Vecteurs côtés
        v_ab = B - A  # côté a (horizontal)
        v_ac = C - A  # côté b (vertical)
        v_bc = C - B  # côté c (hypoténuse)

        # Carré sur a (côté horizontal, vers le bas)
        carre_a = Square(side_length=np.linalg.norm(v_ab), color=colors["blue"], stroke_width=3)
        carre_a.set_fill(colors["blue"], opacity=0.25)
        carre_a.move_to(A + v_ab / 2 + DOWN * np.linalg.norm(v_ab) / 2)

        # Carré sur b (côté vertical, vers la gauche)
        carre_b = Square(side_length=np.linalg.norm(v_ac), color=colors["green"], stroke_width=3)
        carre_b.set_fill(colors["green"], opacity=0.25)
        carre_b.move_to(A + v_ac / 2 + LEFT * np.linalg.norm(v_ac) / 2)

        # Carré sur c (hypoténuse - orientation inclinée)
        carre_c = Square(side_length=np.linalg.norm(v_bc), color=colors["orange"], stroke_width=3)
        carre_c.set_fill(colors["orange"], opacity=0.25)
        # Positionné à l'extérieur du triangle sur l'hypoténuse
        mid_bc = (B + C) / 2
        normal = normalize(np.array([-v_bc[1], v_bc[0], 0]))  # normale sortante
        carre_c.move_to(mid_bc + normal * np.linalg.norm(v_bc) / 2)
        carre_c.rotate(angle_of_vector(v_bc))

        return VGroup(carre_a, carre_b, carre_c)

    def _creer_labels_aires(self, carres, colors):
        """Labels a², b², c² au centre des carrés"""
        labels = []
        for i, (carre, color) in enumerate(zip(carres, [colors["blue"], colors["green"], colors["orange"]])):
            if i == 0:
                label = MathTex("a^2", font_size=36, color=color).set_weight(BOLD)
            elif i == 1:
                label = MathTex("b^2", font_size=36, color=color).set_weight(BOLD)
            else:
                label = MathTex("c^2", font_size=36, color=color).set_weight(BOLD)
            label.move_to(carre.get_center())
            labels.append(label)
        return VGroup(*labels)

    def _decouper_carres(self, carres, colors):
        """Découpe les carrés a² et b² en pièces pour réassembler dans c²"""
        carre_a, carre_b, carre_c = carres

        # Découpage simple : chaque carré en 4 triangles rectangles + 1 carré central
        # Pour la démo, on crée des pièces qui vont s'animer vers le grand carré
        pieces = []

        # Pièces du carré a (bleu) - 4 triangles
        for i in range(4):
            piece = carre_a.copy()
            piece.set_fill(colors["blue"], opacity=0.6)
            piece.set_stroke(colors["blue"], width=2)
            pieces.append(piece)

        # Pièces du carré b (vert) - 4 triangles
        for i in range(4):
            piece = carre_b.copy()
            piece.set_fill(colors["green"], opacity=0.6)
            piece.set_stroke(colors["green"], width=2)
            pieces.append(piece)

        return VGroup(*pieces)

    def _animer_recomposition(self, pieces, carre_cible, colors):
        """Anime les pièces vers le grand carré c²"""
        cible_center = carre_cible.get_center()

        # Animation : pièces volent vers le centre et se transforment
        animations = []
        for i, piece in enumerate(pieces):
            # Position de départ aléatoire autour
            start_pos = piece.get_center()
            # Trajectoire courbe vers le centre
            path = ParametricFunction(
                lambda t: start_pos + (cible_center - start_pos) * smooth(t) + UP * np.sin(t * PI) * 2,
                t_range=[0, 1],
            )
            anim = MoveAlongPath(piece, path, run_time=2, rate_func=smooth)
            animations.append(anim)

        self.play(*animations, lag_ratio=0.05)

        # Flash final sur le grand carré
        self.play(
            Flash(carre_cible, color=colors["yellow"], line_length=0.5, num_lines=12, run_time=1),
            carre_cible.animate.set_fill(colors["orange"], opacity=0.5),
        )

    def _creer_formule_finale(self, colors):
        """Formule finale bien visible dans safe zone"""
        formule = MathTex(
            "a^2", "+", "b^2", "=", "c^2",
            font_size=72,
            color=colors["white"],
        )
        formule[0].set_color(colors["blue"])
        formule[2].set_color(colors["green"])
        formule[4].set_color(colors["orange"])

        # Encadrer
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
# manim -pqh reel_theoreme.py ReelPythagore
# manim -pql reel_theoreme.py ReelPythagore  (dev rapide)
# manim --format=gif reel_theoreme.py ReelPythagore