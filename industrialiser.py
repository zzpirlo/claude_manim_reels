#!/usr/bin/env python3
"""
Industrialisateur de Reels Manim - Lecture de projets.csv et génération/rendu automatique
Format: 9:16 vertical (1080x1920 @ 60fps) pour Instagram Reels
"""

import csv
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime
from string import Template

# ─── CONFIGURATION ───
CSV_PATH = Path("projets.csv")
TEMPLATE_DIR = Path("templates")
OUTPUT_DIR = Path("generated_reels")
RENDER_QUALITY = "h"  # h = high (1080p60), m = medium, l = low
MANIM_CMD = "manim"

# ─── PALETTE COULEURS (noms CSV → hex Manim) ───
COLOR_MAP = {
    "RED": "#EF4444", "BLUE": "#3B82F6", "GREEN": "#22C55E", "YELLOW": "#EAB308",
    "ORANGE": "#F97316", "PURPLE": "#A855F7", "PINK": "#EC4899", "CYAN": "#06B6D4",
    "TEAL": "#14B8A6", "GOLD": "#FBBF24", "SILVER": "#94A3B8", "MAROON": "#7F1D1D",
    "NAVY": "#1E3A5F", "BROWN": "#8B4513", "GREY": "#64748B", "GRAY": "#64748B",
    "BLACK": "#111827", "WHITE": "#F9FAFB", "RGB": "#FFFFFF", "RAINBOW": "#FFFFFF",
}

# ─── TEMPLATE MANIM 9:16 (basé sur reel_theoreme.py) ───
MANIM_TEMPLATE = '''"""
Reel Instagram - ${titre}
Concept: ${concept}
Format vertical 9:16 (1080x1920 @ 60fps) - Safe Zone centrée
Généré automatiquement le ${date_gen}
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


class Reel${id}(Scene):
    """Reel 60s - ${titre} - Format 9:16"""

    # Couleur principale injectée
    COULEUR_PRINCIPALE = "${couleur_hex}"
    COULEUR_ACCENT = "${couleur_accent_hex}"
    COULEUR_SECONDAIRE = "${couleur_secondaire_hex}"

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
            "${titre_hook}",
            font_size=56,
            weight=BOLD,
            color=colors["white"],
        ).move_to(SAFE_CENTER + UP * 2.5)

        sous_titre = Text(
            "${concept_short}",
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

        label = Text("${concept_short_value}", font_size=36, color=colors["white"]).next_to(cercle, DOWN, buff=0.5)

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
            r"\\text{Concept cl\'e}", r"\\rightarrow", r"\\text{R\'esultat}",
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
'''

# ─── HOOKS SPÉCIALISÉS PAR TYPE DE CONCEPT ───
CONCEPT_TEMPLATES = {
    "default": {
        "titre_hook": "Pourquoi ${titre} ?",
        "concept_short": "${concept}",
        "visualisation": "cercle_pulsant",
    },
    "geometrie": {
        "titre_hook": "La preuve visuelle de ${titre}",
        "concept_short": "Géométrie pure",
        "visualisation": "triangle_cercles",
    },
    "calcul": {
        "titre_hook": "Comment calculer ${titre} ?",
        "concept_short": "Analyse en mouvement",
        "visualisation": "courbe_animee",
    },
    "physique": {
        "titre_hook": "La physique derrière ${titre}",
        "concept_short": "Simulation temps réel",
        "visualisation": "particules_animation",
    },
    "probabilite": {
        "titre_hook": "Le paradoxe de ${titre}",
        "concept_short": "Probabilités visuelles",
        "visualisation": "distribution_animee",
    },
    "algo": {
        "titre_hook": "Comment marche ${titre} ?",
        "concept_short": "Algorithme pas à pas",
        "visualisation": "graphe_parcours",
    },
}


def get_color_variants(couleur_nom):
    """Génère une palette harmonieuse à partir de la couleur principale"""
    import colorsys

    hex_color = COLOR_MAP.get(couleur_nom.upper(), "#3B82F6")
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)

    # Variante accent (même teinte, saturation légèrement différente)
    accent_r, accent_g, accent_b = colorsys.hsv_to_rgb(h, min(s*1.2, 1.0), min(v*1.3, 1.0))
    accent_hex = f"#{int(accent_r*255):02x}{int(accent_g*255):02x}{int(accent_b*255):02x}"

    # Variante secondaire (teinte décalée de 30°)
    sec_r, sec_g, sec_b = colorsys.hsv_to_rgb((h + 30/360) % 1.0, s, v)
    sec_hex = f"#{int(sec_r*255):02x}{int(sec_g*255):02x}{int(sec_b*255):02x}"

    return hex_color.upper(), accent_hex.upper(), sec_hex.upper()


def detect_concept_type(concept, titre):
    """Détecte le type de concept pour choisir le bon template"""
    concept_lower = concept.lower()
    titre_lower = titre.lower()

    if any(kw in concept_lower for kw in ["triangle", "cercle", "carré", "géométrie", "angle", "forme", "espace", "rotation", "symétrie", "proportion", "intersection", "conique", "trigo"]):
        return "geometrie"
    if any(kw in concept_lower for kw in ["dérivée", "intégrale", "limite", "fonction", "courbe", "tangente", "pente", "série", "suite", "convergence", "continuité", "différentielle"]):
        return "calcul"
    if any(kw in concept_lower for kw in ["force", "mouvement", "énergie", "masse", "gravité", "onde", "champ", "particule", "vitesse", "accélération", "pression", "température", "chaleur", "optique", "lumière", "son", "magnétique", "électrique", "quantique", "relativité", "thermique", "fluide", "mécanique"]):
        return "physique"
    if any(kw in concept_lower for kw in ["probabilité", "hasard", "aléatoire", "statistique", "distribution", "moyenne", "variance", "bayes", "binomial", "markov", "anniversaire", "fréquence", "échantillon"]):
        return "probabilite"
    if any(kw in concept_lower for kw in ["algorithme", "tri", "recherche", "arbre", "graphe", "chemin", "complexité", "structure", "donnée", "machine", "turing", "compression", "code", "crypto", "rsa", "dijkstra", "huffman"]):
        return "algo"
    return "default"


def generate_manim_file(row, template_str):
    """Génère le fichier Python Manim pour une ligne du CSV"""
    projet_id = row["id"]
    titre = row["titre"]
    concept = row["concept"]
    couleur_nom = row["couleur_principale"]

    # Nettoyer le titre pour nom de fichier/classe
    titre_clean = titre.replace("_", "").replace(" ", "").replace("-", "").replace("é", "e").replace("è", "e").replace("à", "a").replace("û", "u").replace("ô", "o").replace("î", "i")

    # Palette de couleurs
    couleur_hex, couleur_accent_hex, couleur_secondaire_hex = get_color_variants(couleur_nom)

    # Détecter type de concept
    concept_type = detect_concept_type(concept, titre)
    template_config = CONCEPT_TEMPLATES.get(concept_type, CONCEPT_TEMPLATES["default"])

    # Préparer les variables pour le template
    concept_short_val = concept[:50] + "..." if len(concept) > 50 else concept
    template_vars = {
        "id": projet_id,
        "titre": titre,
        "titre_clean": titre_clean,
        "concept": concept,
        "concept_short": concept_short_val,
        "concept_short_value": concept_short_val,
        "couleur_nom": couleur_nom,
        "couleur_hex": f"#{couleur_hex}" if not couleur_hex.startswith("#") else couleur_hex,
        "couleur_accent_hex": couleur_accent_hex,
        "couleur_secondaire_hex": couleur_secondaire_hex,
        "date_gen": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "titre_hook": template_config["titre_hook"].replace("${titre}", titre),
        "visualisation_type": template_config["visualisation"],
    }

    # Générer le code
    template = Template(template_str)
    code = template.substitute(template_vars)

    # Sauvegarder
    filename = f"Reel_{projet_id}_{titre_clean}.py"
    filepath = OUTPUT_DIR / filename
    filepath.write_text(code, encoding="utf-8")

    return filepath, f"Reel{projet_id}"


def update_csv_status(csv_path, projet_id, new_status):
    """Met à jour le statut dans le CSV"""
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["id"] == projet_id:
                row["statut"] = new_status
            rows.append(row)

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def render_manim(filepath, class_name):
    """Lance le rendu Manim"""
    cmd = [MANIM_CMD, f"-pq{RENDER_QUALITY}", str(filepath), class_name]
    print(f"  🎬 Lancement: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        if result.returncode == 0:
            print(f"  ✅ Rendu réussi")
            return True
        else:
            print(f"  ❌ Erreur rendu: {result.stderr[:500]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  ⏱️ Timeout (10 min)")
        return False
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
        return False


def main():
    print("=" * 60)
    print("🏭 INDUSTRIALISATEUR DE REELS MANIM")
    print("=" * 60)

    # Créer dossier de sortie
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Lire le CSV
    projets_en_attente = []
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["statut"].strip().lower() == "en_attente":
                projets_en_attente.append(row)

    if not projets_en_attente:
        print("✅ Aucun projet en attente.")
        return

    print(f"📋 {len(projets_en_attente)} projet(s) en attente trouvés")
    print("-" * 60)

    # Traiter chaque projet
    succes = 0
    echecs = 0

    for i, row in enumerate(projets_en_attente, 1):
        projet_id = row["id"]
        titre = row["titre"]
        print(f"\n[{i}/{len(projets_en_attente)}] 📦 Projet {projet_id}: {titre}")

        # Générer le fichier
        filepath, class_name = generate_manim_file(row, MANIM_TEMPLATE)
        print(f"  📝 Fichier généré: {filepath.name}")

        # Lancer le rendu
        if render_manim(filepath, class_name):
            succes += 1
            update_csv_status(CSV_PATH, projet_id, "termine")
            print(f"  ✅ Statut mis à jour: terminé")
        else:
            echecs += 1
            update_csv_status(CSV_PATH, projet_id, "erreur")
            print(f"  ❌ Statut mis à jour: erreur")

    # Résumé
    print("\n" + "=" * 60)
    print(f"📊 RÉSUMÉ: {succes} réussi(s), {echecs} échec(s)")
    print("=" * 60)


if __name__ == "__main__":
    main()