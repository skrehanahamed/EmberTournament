#!/usr/bin/env python3
"""Writes prompts/ALL_PROMPTS.md: one complete, copy-paste image prompt per asset (Ember Tournament)."""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prompts", "ALL_PROMPTS.md")

STYLE = ("High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. "
         "Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, "
         "light from the top-left, rich saturated colours, maximum 24 colours. "
         "NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. "
         "Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.")

ALPHA = ("Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, "
         "no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.")

CHARS = {
    "kaito": {
        "title": "Kaito (all-rounder, hero)",
        "dna": ("KAITO: a young male martial artist, athletic medium build, tan skin, determined dark-brown eyes, short spiky black hair, "
                "small scar on the left cheek, white sleeveless karate gi jacket open at the chest, white loose gi trousers, "
                "a red cloth sash belt with two hanging ends, red hand wraps on both fists, bare feet with red ankle wraps"),
        "special": "pushes both open palms forward together in a palm-strike pose to release a ball of orange energy (do NOT draw the energy ball itself)",
        "color": "orange",
    },
    "brutus": {
        "title": "Brutus (grappler, heavy)",
        "dna": ("BRUTUS: a huge, very muscular male brawler, extra-wide shoulders and thick arms (about 1.2 times wider than a normal fighter), "
                "dark-brown skin, bald head, thick black beard, angry expression, open dark-red sleeveless leather vest showing the chest, "
                "dark-grey baggy trousers, a wide gold belt buckle, spiked steel bracers on both forearms, heavy black boots"),
        "special": "swings both fists forward and down in a heavy two-handed smash to throw a ball of red magma energy (do NOT draw the energy ball itself)",
        "color": "red",
    },
    "valeria": {
        "title": "Valeria (rushdown assassin)",
        "dna": ("VALERIA: a slim, agile female assassin, light-tan skin, sharp green eyes, red hair tied in two buns with loose strands, "
                "black crop top with gold trim, short black shorts with a crimson sash, gold wraps on both forearms, "
                "black wrapped legs, light black boots with gold buckles"),
        "special": "sweeps one open hand across the body and flicks it forward to throw a crimson fire ball (do NOT draw the fire ball itself)",
        "color": "crimson",
    },
    "mira": {
        "title": "Mira (storm mage, zoner)",
        "dna": ("MIRA: a tall slender female storm mage, dark-brown skin, glowing cyan eyes, long flowing silver-white hair, "
                "a dark-navy combat robe with cyan trim and a side slit, fingerless dark gloves, glowing cyan rune tattoos on both arms, "
                "dark boots with cyan details"),
        "special": "raises one hand up, then points it forward to launch a ball of cyan lightning (do NOT draw the lightning ball itself)",
        "color": "cyan",
    },
}

# animation: (file, frame count, per-frame description list, loop-note)
ANIMS = [
    ("idle", 6, ["relaxed fighting stance, fists raised near the chin, knees slightly bent",
                 "chest rises by one pixel, body a tiny bit taller",
                 "highest point of the breath, shoulders slightly raised",
                 "chest starts to lower",
                 "knees dip slightly, body a tiny bit lower",
                 "lowest point, almost identical to frame 1 so the loop is seamless"], "a seamless looping breathing cycle"),
    ("walk_forward", 8, ["right foot far forward, left foot back, guard up",
                         "right foot lands, body lowest",
                         "left leg passes under the body, body rising",
                         "left foot lifted, high point",
                         "left foot far forward, right foot back, guard up",
                         "left foot lands, body lowest",
                         "right leg passes under the body, body rising",
                         "right foot lifted, high point"], "a seamless looping walk cycle moving to the right, fists kept up in guard"),
    ("walk_back", 8, ["left foot far back, right foot forward, guard up, leaning slightly back",
                      "left foot lands behind, body lowest",
                      "right leg slides back, body rising",
                      "right foot lifted, high point",
                      "right foot far back, left foot forward, guard up",
                      "right foot lands behind, body lowest",
                      "left leg slides back, body rising",
                      "left foot lifted, high point"], "a seamless looping backward walk (retreat), fists kept up in guard, still facing right"),
    ("crouch", 2, ["halfway down into a crouch, knees bent, fists up",
                   "full low crouch, torso low, fists guarding the face, hold pose"], "going into a crouch and holding it"),
    ("jump", 6, ["knees bent deeply, preparing to jump",
                 "pushing off the ground, legs stretching, body rising",
                 "rising, knees tucked, fists up",
                 "top of the jump, knees tucked high",
                 "falling, legs extending downward",
                 "landing impact, knees bent absorbing the landing"], "a full jump arc; frames 2 to 5 are in the air (feet above the baseline), frames 1 and 6 on the ground"),
    ("punch_light", 5, ["fighting stance, weight shifting",
                        "front arm pulled back, shoulder twisting",
                        "ARM FULLY EXTENDED jab, fist at head height (contact frame)",
                        "arm still extended, slight lean forward",
                        "arm pulled back to guard, returning to stance"], "a fast jab with the front hand"),
    ("punch_heavy", 7, ["fighting stance",
                        "body lowers, knees bend, rear fist pulled far back",
                        "torso twists back, maximum wind-up",
                        "torso whips forward, rear fist starting to travel",
                        "BIG LUNGING PUNCH, rear arm fully extended, front foot stepping forward (contact frame)",
                        "follow-through, body leaning far forward",
                        "recovering back to the fighting stance"], "a slow, powerful straight punch with the rear hand"),
    ("kick", 7, ["fighting stance",
                 "weight shifts onto the back leg, front knee starts lifting",
                 "knee lifted high, leg chambered",
                 "LEG FULLY EXTENDED in a horizontal front kick at waist height (contact frame)",
                 "kick held, torso leaning back for balance",
                 "leg pulled back to the chambered position",
                 "foot lands, back to the fighting stance"], "a strong front kick with the front leg"),
    ("special", 8, ["fighting stance, beginning to crouch",
                    "hands drawn back to the hip, gathering energy, body low",
                    "gathering energy, body tense, leaning back",
                    "hands begin to thrust forward",
                    "{SPECIAL} (release frame)",
                    "arms fully extended forward, follow-through",
                    "arms still forward, body leaning in",
                    "arms lowering, returning to the fighting stance"], "a special-move throw. The character {SPECIAL}"),
    ("block", 2, ["arms start to rise to guard, body leaning back slightly",
                  "full standing guard, both forearms crossed in front of the face, torso leaning slightly back"], "a standing block, hold on the last frame"),
    ("hit", 3, ["impact: head snaps back, face grimacing, body jolted backward",
                "maximum recoil: torso bent back, one foot sliding backwards",
                "starting to recover, head coming forward again"], "a hit reaction (flinch) after being punched in the face; no effects drawn, only the character"),
    ("knockdown", 6, ["struck, body lifted off the ground, leaning back",
                      "flying backwards through the air, body almost horizontal",
                      "tumbling, feet above the head height of the body",
                      "slamming onto the ground on the back",
                      "small bounce, body slightly lifted",
                      "lying flat on the back on the ground, arms spread, hold pose"], "being knocked down and landing on the back; the character moves LEFT (backwards) as they fall"),
    ("getup", 5, ["lying flat on the back",
                  "rolling up, one hand pushing on the ground",
                  "kneeling on one knee, head up",
                  "rising to standing, fists coming up",
                  "back in the fighting stance"], "getting up from the ground back into the fighting stance"),
    ("ko", 6, ["staggering backwards, head down, arms hanging",
               "knees buckling, falling backwards",
               "falling, body tilted back at 45 degrees",
               "hits the ground hard on the back",
               "slight bounce, limbs loose",
               "lying completely still, defeated, eyes closed, hold pose"], "being knocked out and falling backwards; the last frame is the final defeated pose"),
    ("win", 6, ["standing straight, catching breath",
                "raising one fist toward the sky",
                "fist high, chest out, shouting",
                "holding the victory pose, confident smile",
                "slight bounce of the victory pose",
                "holding the victory pose"], "a victory celebration, ending in a held pose"),
]


def strip_layout(n):
    return (f"Draw exactly {n} frames of the SAME character in ONE single horizontal row, left to right, in time order. "
            f"Leave a wide empty gap (at least 25 percent of the character's width) between neighbouring frames so each frame can be cut out separately. "
            f"All frames must have exactly the same scale. The feet (or the lowest point of the standing body) must rest on the same invisible horizontal line in every frame, "
            f"except frames where the move lifts the character off the ground. The character faces RIGHT in every frame. "
            f"The full body is always visible and never cropped. ONE row only: no second row, no extra characters, no extra drawings, no ground, no text.")


def anim_prompt(cid, c, anim):
    name, n, frames, note = anim
    special = c["special"]
    note = note.replace("{SPECIAL}", special)
    fr = [f.replace("{SPECIAL}", special) for f in frames]
    lines = "\n".join(f"Frame {i + 1}: {t}" for i, t in enumerate(fr))
    return (f"{STYLE}\n\n"
            f"Use the attached reference image(s) of this exact character: {c['dna']}. "
            f"The face, hair, outfit, colours and proportions must be IDENTICAL to the reference in every frame.\n\n"
            f"TASK: an animation strip of the '{name.replace('_', ' ')}' animation: {note}.\n\n"
            f"{lines}\n\n"
            f"{strip_layout(n)}\n\n{ALPHA}")


def reference_prompt(c):
    return (f"{STYLE}\n\n"
            f"TASK: a character design reference sheet of ONE character: {c['dna']}.\n"
            f"Show the SAME character three times in a single horizontal row, with wide empty gaps between them: "
            f"(1) front view, (2) side view facing right, (3) back view. All three in a relaxed neutral standing pose, arms slightly away from the body, "
            f"full body visible, all the same size, feet on the same line. Only this one character, nothing else.\n\n{ALPHA}")


def stance_prompt(c):
    return (f"{STYLE}\n\n"
            f"Use the attached reference sheet of this exact character: {c['dna']}.\n"
            f"TASK: ONE single image of the character in a ready fighting stance, side view facing RIGHT: knees bent, front fist at chin height, rear fist near the jaw, "
            f"weight on the balls of the feet, intense expression. Full body visible with a little empty space around it. Exactly one character, one pose, nothing else. "
            f"This image will be the master pose used to draw every animation, so make it clean and perfectly consistent with the sheet.\n\n{ALPHA}")


def fx_strip(n, what, frames, extra=""):
    lines = "\n".join(f"Frame {i + 1}: {t}" for i, t in enumerate(frames))
    return (f"{STYLE.split(' Realistic')[0]}\n\nTASK: a visual-effect animation strip: {what}\n\n{lines}\n\n"
            f"Draw exactly {n} frames in ONE single horizontal row, left to right, in time order, all the same size and centred on the same horizontal line, "
            f"with a wide empty gap between frames. Only the effect: no characters, no hands, no text. {extra}\n\n{ALPHA}")


def stage_prompt(desc):
    return (f"{STYLE.split(' Realistic')[0]}\n\n"
            f"TASK: ONE side-view background for a 2D fighting game, wide 16:9 composition. {desc}\n"
            f"Layout: the flat fighting floor is a clean, level, readable surface occupying the BOTTOM 22 percent of the image with no objects on it; "
            f"the detailed scenery fills the upper part with strong depth (far, middle and near layers). "
            f"Absolutely NO characters, NO people, NO text, NO logos, NO UI, NO fog covering the floor. Fully opaque image, no transparency. "
            f"Strict pixel-art look: no anti-aliasing, no blur, no photographic textures.")



GROUPS = [
    ("locomotion", "SHEET 1 - MOVEMENT", ["idle", "walk_forward", "walk_back", "jump"]),
    ("attacks", "SHEET 2 - ATTACKS", ["punch_light", "punch_heavy", "kick", "special"]),
    ("reactions", "SHEET 3 - DEFENCE AND DEFEAT", ["block", "hit", "crouch", "ko"]),
    ("extras", "SHEET 4 - EXTRAS (make later)", ["knockdown", "getup", "win"]),
]
ADICT = {a[0]: a for a in ANIMS}


def model_sheet(c):
    return (f"{STYLE}\n\nTASK: ONE character model sheet of ONE character: {c['dna']}.\n"
            f"Draw the SAME character FOUR times in a single horizontal row with wide empty gaps between them, all at exactly the same scale, "
            f"feet on the same line, full body visible and nothing cropped: (1) front view in a relaxed standing pose, (2) side view facing right in a relaxed standing pose, "
            f"(3) back view in a relaxed standing pose, (4) side view facing RIGHT in a ready fighting stance: knees bent, front fist at chin height, rear fist near the jaw, intense expression. "
            f"Only this one character, no text, no labels.\n\n{ALPHA}")


def sheet_prompt(c, rows):
    n = len(rows)
    parts = []
    for i, key in enumerate(rows, 1):
        name, cnt, frames, note = ADICT[key]
        sp = c["special"]
        fr = "; ".join(f"Frame {k + 1}: " + f.replace("{SPECIAL}", sp) for k, f in enumerate(frames))
        note = note.replace("{SPECIAL}", sp)
        parts.append(f"ROW {i} - {name.replace('_', ' ').upper()} ({cnt} frames, columns 1-{cnt}, {note}): {fr}.")
    rowtxt = "\n\n".join(parts)
    return (f"{STYLE}\n\n"
            f"Use the attached model sheet of this exact character: {c['dna']}. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.\n\n"
            f"TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of {n} ROWS and 8 COLUMNS on a single image. "
            f"Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. "
            f"Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. "
            f"In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). "
            f"The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.\n\n"
            f"{rowtxt}\n\n"
            f"Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.\n\n{ALPHA}")


def fx_sheet():
    rows = [
        ("HIT SPARK (6 frames)", "a white-yellow impact flash for a punch hit as spiky star-shaped pixel bursts: tiny bright white dot; small white-yellow star burst; large spiky white-yellow burst with orange tips (peak); burst fading with thinner spikes; a few orange spark lines flying outward; last tiny orange sparks."),
        ("BLOCK SPARK (5 frames)", "a blue-white metallic block flash: small blue-white dot; growing ring of blue-white light with short lines; largest ring with bright white centre (peak); ring fading; a few tiny blue sparks."),
        ("ORANGE FIREBALL (4 frames, looping)", "an orange and yellow fire energy ball with a short flame tail pointing left, flying to the right; the same ball in 4 slightly different flame shapes so it loops smoothly."),
        ("ORANGE FIREBALL EXPLOSION (6 frames)", "the explosion when that ball hits a target: small bright flash; round burst growing; largest burst with a bright core (peak); burst breaking into sparks; sparks flying outward; last tiny embers."),
    ]
    txt = "\n\n".join(f"ROW {i} - {t}: {d}" for i, (t, d) in enumerate(rows, 1))
    return (f"{STYLE.split(' Realistic')[0]}\n\nTASK: ONE visual-effects sprite sheet, a strict grid of 4 ROWS and 6 COLUMNS. Each row is one effect animation drawn left to right in time order starting in column 1; unused columns stay empty. "
            f"Every cell is the same size, each effect is centred in its cell and never touches the cell edge, clear empty space between cells. No grid lines, borders, labels or numbers. Only the effects: no characters, no hands, no text.\n\n{txt}\n\n{ALPHA}")


def fx_sheet2():
    rows = [
        ("DUST PUFF (5 frames)", "a small grey-beige dust puff kicked up at the feet on landing, round pixel clouds on a flat bottom line: tiny puff; puff grows and splits in two; two larger round clouds; clouds spreading and thinning; faint small remains."),
        ("RED FIREBALL (4 frames, looping)", "a dark-red magma energy ball with black cracks and a short ember tail pointing left, flying to the right; 4 slightly different flame shapes so it loops."),
        ("CRIMSON FIREBALL (4 frames, looping)", "a crimson and orange flame ball with a swirling fire tail pointing left, flying to the right; 4 slightly different flame shapes so it loops."),
        ("CYAN LIGHTNING BALL (4 frames, looping)", "a cyan and white lightning energy ball with small electric arcs and a short tail pointing left, flying to the right; 4 slightly different shapes so it loops."),
    ]
    txt = "\n\n".join(f"ROW {i} - {t}: {d}" for i, (t, d) in enumerate(rows, 1))
    return (f"{STYLE.split(' Realistic')[0]}\n\nTASK: ONE visual-effects sprite sheet, a strict grid of 4 ROWS and 6 COLUMNS. Each row is one effect animation drawn left to right in time order starting in column 1; unused columns stay empty. "
            f"Every cell is the same size, each effect is centred in its cell and never touches the cell edge, clear empty space between cells. No grid lines, borders, labels or numbers. Only the effects: no characters, no hands, no text.\n\n{txt}\n\n{ALPHA}")


def main():
    out = ["# EMBER TOURNAMENT - grouped image prompts (one image = one whole sheet)\n",
           "## How to use\n",
           "1. Use ONE chat per character. First make the **model sheet**, then attach it to every sprite-sheet prompt in that same chat.",
           "2. Image size: **1536 x 1024 (landscape)** for every sheet. Backgrounds: widest size available. Logo: any.",
           "3. A sprite sheet is 8 columns x 4 rows, so every frame cell is about 192 x 256 px. I will cut and clean it.",
           "4. If ONE row is bad, regenerate the WHOLE sheet (never a single row, it will drift). Reply: *\"Redo the whole sheet. Real transparent background, same character in every cell, clear gaps between cells.\"*",
           "5. If the character drifts, reply: *\"Every cell must be identical to the attached model sheet. Redo.\"*",
           "6. Save with the file name in the heading, do not resize or edit.\n"]
    n = 0
    for cid, c in CHARS.items():
        out.append(f"\n---\n\n# CHARACTER: {c['title']}\n")
        n += 1
        out.append(f"### {n}. `characters/{cid}/{cid}_model.png`  (make FIRST, no attachment)\n```\n{model_sheet(c)}\n```\n")
        for gname, gtitle, rows in GROUPS:
            n += 1
            out.append(f"### {n}. `characters/{cid}/{cid}_{gname}.png`  ({gtitle}; attach {cid}_model.png)\n```\n{sheet_prompt(c, rows)}\n```\n")
    out.append("\n---\n\n# EFFECTS\n")
    for fname, p in [("fx/fx_sheet1.png", fx_sheet()), ("fx/fx_sheet2.png", fx_sheet2())]:
        n += 1
        out.append(f"### {n}. `{fname}`\n```\n{p}\n```\n")
    out.append("\n---\n\n# STAGES (opaque backgrounds)\n")
    stages = [
        ("stages/stage1_neon_city.png", "A rainy neon cyberpunk city street at night: tall buildings with glowing pink, cyan and purple neon signs (no readable text), wet reflective road, parked vehicles far behind, steam vents, power lines, a big moon behind the skyline."),
        ("stages/stage2_temple.png", "A hilltop dojo temple courtyard at sunset: large red torii gate, stone lanterns, cherry-blossom trees with falling petals, far mountains and a huge orange sun, wooden dojo building, stone floor tiles."),
        ("stages/stage3_volcano.png", "A volcano arena at night: black stone ring platform with glowing orange cracks, rivers of lava in the background, a giant erupting volcano with an ash-filled red sky, burning torches on iron poles, floating embers."),
    ]
    for fname, d in stages:
        n += 1
        out.append(f"### {n}. `{fname}`\n```\n{stage_prompt(d)}\n```\n")
    out.append("\n---\n\n# USER INTERFACE\n")
    logo = (f"{STYLE.split(' Realistic')[0]}\n\nTASK: a game title logo that reads exactly EMBER TOURNAMENT on two lines: EMBER on the first line (large) and TOURNAMENT on the second line (smaller, wide letter spacing). Spelled exactly E-M-B-E-R and T-O-U-R-N-A-M-E-N-T. Big chunky pixel-art lettering with a thick dark outline, fiery orange-to-yellow metallic fill with glowing embers floating off the letters, a small flame crest between the two lines. Only the logo, centred, with empty space around it. Check that the spelling is exactly EMBER TOURNAMENT.\n\nOutput a PNG with a REAL transparent background (alpha channel), no checkerboard, no extra text.")
    n += 1
    out.append(f"### {n}. `ui/title_logo.png`\n```\n{logo}\n```\n")
    n += 1
    out.append(f"### {n}. `ui/portraits.png`  (one sheet with all 4 portraits; attach the 4 model sheets)\n```\n{STYLE.split(' Realistic')[0]}\n\nUse the attached model sheets of these four characters: {' | '.join(c['dna'] for c in CHARS.values())}.\nTASK: ONE image with FOUR head-and-shoulders portrait icons in a single horizontal row with wide gaps, in this order: KAITO, BRUTUS, VALERIA, MIRA. Each is facing slightly right with a fierce expression, same size, centred, identical to its model sheet. No text, no labels.\n\n{ALPHA}\n```\n")
    out.append(f"\n---\n\nTotal prompts: {n}\n")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write("\n".join(out))
    print("wrote", os.path.abspath(OUT), "prompts:", n)


main()
