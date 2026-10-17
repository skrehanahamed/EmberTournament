# EMBER TOURNAMENT - grouped image prompts (one image = one whole sheet)

## How to use

1. Use ONE chat per character. First make the **model sheet**, then attach it to every sprite-sheet prompt in that same chat.
2. Image size: **1536 x 1024 (landscape)** for every sheet. Backgrounds: widest size available. Logo: any.
3. A sprite sheet is 8 columns x 4 rows, so every frame cell is about 192 x 256 px. I will cut and clean it.
4. If ONE row is bad, regenerate the WHOLE sheet (never a single row, it will drift). Reply: *"Redo the whole sheet. Real transparent background, same character in every cell, clear gaps between cells."*
5. If the character drifts, reply: *"Every cell must be identical to the attached model sheet. Redo."*
6. Save with the file name in the heading, do not resize or edit.


---

# CHARACTER: Kaito (all-rounder, hero)

### 1. `characters/kaito/kaito_model.png`  (make FIRST, no attachment)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

TASK: ONE character model sheet of ONE character: KAITO: a young male martial artist, athletic medium build, tan skin, determined dark-brown eyes, short spiky black hair, small scar on the left cheek, white sleeveless karate gi jacket open at the chest, white loose gi trousers, a red cloth sash belt with two hanging ends, red hand wraps on both fists, bare feet with red ankle wraps.
Draw the SAME character FOUR times in a single horizontal row with wide empty gaps between them, all at exactly the same scale, feet on the same line, full body visible and nothing cropped: (1) front view in a relaxed standing pose, (2) side view facing right in a relaxed standing pose, (3) back view in a relaxed standing pose, (4) side view facing RIGHT in a ready fighting stance: knees bent, front fist at chin height, rear fist near the jaw, intense expression. Only this one character, no text, no labels.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 2. `characters/kaito/kaito_locomotion.png`  (SHEET 1 - MOVEMENT; attach kaito_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: KAITO: a young male martial artist, athletic medium build, tan skin, determined dark-brown eyes, short spiky black hair, small scar on the left cheek, white sleeveless karate gi jacket open at the chest, white loose gi trousers, a red cloth sash belt with two hanging ends, red hand wraps on both fists, bare feet with red ankle wraps. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - IDLE (6 frames, columns 1-6, a seamless looping breathing cycle): Frame 1: relaxed fighting stance, fists raised near the chin, knees slightly bent; Frame 2: chest rises by one pixel, body a tiny bit taller; Frame 3: highest point of the breath, shoulders slightly raised; Frame 4: chest starts to lower; Frame 5: knees dip slightly, body a tiny bit lower; Frame 6: lowest point, almost identical to frame 1 so the loop is seamless.

ROW 2 - WALK FORWARD (8 frames, columns 1-8, a seamless looping walk cycle moving to the right, fists kept up in guard): Frame 1: right foot far forward, left foot back, guard up; Frame 2: right foot lands, body lowest; Frame 3: left leg passes under the body, body rising; Frame 4: left foot lifted, high point; Frame 5: left foot far forward, right foot back, guard up; Frame 6: left foot lands, body lowest; Frame 7: right leg passes under the body, body rising; Frame 8: right foot lifted, high point.

ROW 3 - WALK BACK (8 frames, columns 1-8, a seamless looping backward walk (retreat), fists kept up in guard, still facing right): Frame 1: left foot far back, right foot forward, guard up, leaning slightly back; Frame 2: left foot lands behind, body lowest; Frame 3: right leg slides back, body rising; Frame 4: right foot lifted, high point; Frame 5: right foot far back, left foot forward, guard up; Frame 6: right foot lands behind, body lowest; Frame 7: left leg slides back, body rising; Frame 8: left foot lifted, high point.

ROW 4 - JUMP (6 frames, columns 1-6, a full jump arc; frames 2 to 5 are in the air (feet above the baseline), frames 1 and 6 on the ground): Frame 1: knees bent deeply, preparing to jump; Frame 2: pushing off the ground, legs stretching, body rising; Frame 3: rising, knees tucked, fists up; Frame 4: top of the jump, knees tucked high; Frame 5: falling, legs extending downward; Frame 6: landing impact, knees bent absorbing the landing.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 3. `characters/kaito/kaito_attacks.png`  (SHEET 2 - ATTACKS; attach kaito_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: KAITO: a young male martial artist, athletic medium build, tan skin, determined dark-brown eyes, short spiky black hair, small scar on the left cheek, white sleeveless karate gi jacket open at the chest, white loose gi trousers, a red cloth sash belt with two hanging ends, red hand wraps on both fists, bare feet with red ankle wraps. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - PUNCH LIGHT (5 frames, columns 1-5, a fast jab with the front hand): Frame 1: fighting stance, weight shifting; Frame 2: front arm pulled back, shoulder twisting; Frame 3: ARM FULLY EXTENDED jab, fist at head height (contact frame); Frame 4: arm still extended, slight lean forward; Frame 5: arm pulled back to guard, returning to stance.

ROW 2 - PUNCH HEAVY (7 frames, columns 1-7, a slow, powerful straight punch with the rear hand): Frame 1: fighting stance; Frame 2: body lowers, knees bend, rear fist pulled far back; Frame 3: torso twists back, maximum wind-up; Frame 4: torso whips forward, rear fist starting to travel; Frame 5: BIG LUNGING PUNCH, rear arm fully extended, front foot stepping forward (contact frame); Frame 6: follow-through, body leaning far forward; Frame 7: recovering back to the fighting stance.

ROW 3 - KICK (7 frames, columns 1-7, a strong front kick with the front leg): Frame 1: fighting stance; Frame 2: weight shifts onto the back leg, front knee starts lifting; Frame 3: knee lifted high, leg chambered; Frame 4: LEG FULLY EXTENDED in a horizontal front kick at waist height (contact frame); Frame 5: kick held, torso leaning back for balance; Frame 6: leg pulled back to the chambered position; Frame 7: foot lands, back to the fighting stance.

ROW 4 - SPECIAL (8 frames, columns 1-8, a special-move throw. The character pushes both open palms forward together in a palm-strike pose to release a ball of orange energy (do NOT draw the energy ball itself)): Frame 1: fighting stance, beginning to crouch; Frame 2: hands drawn back to the hip, gathering energy, body low; Frame 3: gathering energy, body tense, leaning back; Frame 4: hands begin to thrust forward; Frame 5: pushes both open palms forward together in a palm-strike pose to release a ball of orange energy (do NOT draw the energy ball itself) (release frame); Frame 6: arms fully extended forward, follow-through; Frame 7: arms still forward, body leaning in; Frame 8: arms lowering, returning to the fighting stance.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 4. `characters/kaito/kaito_reactions.png`  (SHEET 3 - DEFENCE AND DEFEAT; attach kaito_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: KAITO: a young male martial artist, athletic medium build, tan skin, determined dark-brown eyes, short spiky black hair, small scar on the left cheek, white sleeveless karate gi jacket open at the chest, white loose gi trousers, a red cloth sash belt with two hanging ends, red hand wraps on both fists, bare feet with red ankle wraps. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - BLOCK (2 frames, columns 1-2, a standing block, hold on the last frame): Frame 1: arms start to rise to guard, body leaning back slightly; Frame 2: full standing guard, both forearms crossed in front of the face, torso leaning slightly back.

ROW 2 - HIT (3 frames, columns 1-3, a hit reaction (flinch) after being punched in the face; no effects drawn, only the character): Frame 1: impact: head snaps back, face grimacing, body jolted backward; Frame 2: maximum recoil: torso bent back, one foot sliding backwards; Frame 3: starting to recover, head coming forward again.

ROW 3 - CROUCH (2 frames, columns 1-2, going into a crouch and holding it): Frame 1: halfway down into a crouch, knees bent, fists up; Frame 2: full low crouch, torso low, fists guarding the face, hold pose.

ROW 4 - KO (6 frames, columns 1-6, being knocked out and falling backwards; the last frame is the final defeated pose): Frame 1: staggering backwards, head down, arms hanging; Frame 2: knees buckling, falling backwards; Frame 3: falling, body tilted back at 45 degrees; Frame 4: hits the ground hard on the back; Frame 5: slight bounce, limbs loose; Frame 6: lying completely still, defeated, eyes closed, hold pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 5. `characters/kaito/kaito_extras.png`  (SHEET 4 - EXTRAS (make later); attach kaito_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: KAITO: a young male martial artist, athletic medium build, tan skin, determined dark-brown eyes, short spiky black hair, small scar on the left cheek, white sleeveless karate gi jacket open at the chest, white loose gi trousers, a red cloth sash belt with two hanging ends, red hand wraps on both fists, bare feet with red ankle wraps. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 3 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - KNOCKDOWN (6 frames, columns 1-6, being knocked down and landing on the back; the character moves LEFT (backwards) as they fall): Frame 1: struck, body lifted off the ground, leaning back; Frame 2: flying backwards through the air, body almost horizontal; Frame 3: tumbling, feet above the head height of the body; Frame 4: slamming onto the ground on the back; Frame 5: small bounce, body slightly lifted; Frame 6: lying flat on the back on the ground, arms spread, hold pose.

ROW 2 - GETUP (5 frames, columns 1-5, getting up from the ground back into the fighting stance): Frame 1: lying flat on the back; Frame 2: rolling up, one hand pushing on the ground; Frame 3: kneeling on one knee, head up; Frame 4: rising to standing, fists coming up; Frame 5: back in the fighting stance.

ROW 3 - WIN (6 frames, columns 1-6, a victory celebration, ending in a held pose): Frame 1: standing straight, catching breath; Frame 2: raising one fist toward the sky; Frame 3: fist high, chest out, shouting; Frame 4: holding the victory pose, confident smile; Frame 5: slight bounce of the victory pose; Frame 6: holding the victory pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```


---

# CHARACTER: Brutus (grappler, heavy)

### 6. `characters/brutus/brutus_model.png`  (make FIRST, no attachment)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

TASK: ONE character model sheet of ONE character: BRUTUS: a huge, very muscular male brawler, extra-wide shoulders and thick arms (about 1.2 times wider than a normal fighter), dark-brown skin, bald head, thick black beard, angry expression, open dark-red sleeveless leather vest showing the chest, dark-grey baggy trousers, a wide gold belt buckle, spiked steel bracers on both forearms, heavy black boots.
Draw the SAME character FOUR times in a single horizontal row with wide empty gaps between them, all at exactly the same scale, feet on the same line, full body visible and nothing cropped: (1) front view in a relaxed standing pose, (2) side view facing right in a relaxed standing pose, (3) back view in a relaxed standing pose, (4) side view facing RIGHT in a ready fighting stance: knees bent, front fist at chin height, rear fist near the jaw, intense expression. Only this one character, no text, no labels.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 7. `characters/brutus/brutus_locomotion.png`  (SHEET 1 - MOVEMENT; attach brutus_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: BRUTUS: a huge, very muscular male brawler, extra-wide shoulders and thick arms (about 1.2 times wider than a normal fighter), dark-brown skin, bald head, thick black beard, angry expression, open dark-red sleeveless leather vest showing the chest, dark-grey baggy trousers, a wide gold belt buckle, spiked steel bracers on both forearms, heavy black boots. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - IDLE (6 frames, columns 1-6, a seamless looping breathing cycle): Frame 1: relaxed fighting stance, fists raised near the chin, knees slightly bent; Frame 2: chest rises by one pixel, body a tiny bit taller; Frame 3: highest point of the breath, shoulders slightly raised; Frame 4: chest starts to lower; Frame 5: knees dip slightly, body a tiny bit lower; Frame 6: lowest point, almost identical to frame 1 so the loop is seamless.

ROW 2 - WALK FORWARD (8 frames, columns 1-8, a seamless looping walk cycle moving to the right, fists kept up in guard): Frame 1: right foot far forward, left foot back, guard up; Frame 2: right foot lands, body lowest; Frame 3: left leg passes under the body, body rising; Frame 4: left foot lifted, high point; Frame 5: left foot far forward, right foot back, guard up; Frame 6: left foot lands, body lowest; Frame 7: right leg passes under the body, body rising; Frame 8: right foot lifted, high point.

ROW 3 - WALK BACK (8 frames, columns 1-8, a seamless looping backward walk (retreat), fists kept up in guard, still facing right): Frame 1: left foot far back, right foot forward, guard up, leaning slightly back; Frame 2: left foot lands behind, body lowest; Frame 3: right leg slides back, body rising; Frame 4: right foot lifted, high point; Frame 5: right foot far back, left foot forward, guard up; Frame 6: right foot lands behind, body lowest; Frame 7: left leg slides back, body rising; Frame 8: left foot lifted, high point.

ROW 4 - JUMP (6 frames, columns 1-6, a full jump arc; frames 2 to 5 are in the air (feet above the baseline), frames 1 and 6 on the ground): Frame 1: knees bent deeply, preparing to jump; Frame 2: pushing off the ground, legs stretching, body rising; Frame 3: rising, knees tucked, fists up; Frame 4: top of the jump, knees tucked high; Frame 5: falling, legs extending downward; Frame 6: landing impact, knees bent absorbing the landing.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 8. `characters/brutus/brutus_attacks.png`  (SHEET 2 - ATTACKS; attach brutus_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: BRUTUS: a huge, very muscular male brawler, extra-wide shoulders and thick arms (about 1.2 times wider than a normal fighter), dark-brown skin, bald head, thick black beard, angry expression, open dark-red sleeveless leather vest showing the chest, dark-grey baggy trousers, a wide gold belt buckle, spiked steel bracers on both forearms, heavy black boots. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - PUNCH LIGHT (5 frames, columns 1-5, a fast jab with the front hand): Frame 1: fighting stance, weight shifting; Frame 2: front arm pulled back, shoulder twisting; Frame 3: ARM FULLY EXTENDED jab, fist at head height (contact frame); Frame 4: arm still extended, slight lean forward; Frame 5: arm pulled back to guard, returning to stance.

ROW 2 - PUNCH HEAVY (7 frames, columns 1-7, a slow, powerful straight punch with the rear hand): Frame 1: fighting stance; Frame 2: body lowers, knees bend, rear fist pulled far back; Frame 3: torso twists back, maximum wind-up; Frame 4: torso whips forward, rear fist starting to travel; Frame 5: BIG LUNGING PUNCH, rear arm fully extended, front foot stepping forward (contact frame); Frame 6: follow-through, body leaning far forward; Frame 7: recovering back to the fighting stance.

ROW 3 - KICK (7 frames, columns 1-7, a strong front kick with the front leg): Frame 1: fighting stance; Frame 2: weight shifts onto the back leg, front knee starts lifting; Frame 3: knee lifted high, leg chambered; Frame 4: LEG FULLY EXTENDED in a horizontal front kick at waist height (contact frame); Frame 5: kick held, torso leaning back for balance; Frame 6: leg pulled back to the chambered position; Frame 7: foot lands, back to the fighting stance.

ROW 4 - SPECIAL (8 frames, columns 1-8, a special-move throw. The character swings both fists forward and down in a heavy two-handed smash to throw a ball of red magma energy (do NOT draw the energy ball itself)): Frame 1: fighting stance, beginning to crouch; Frame 2: hands drawn back to the hip, gathering energy, body low; Frame 3: gathering energy, body tense, leaning back; Frame 4: hands begin to thrust forward; Frame 5: swings both fists forward and down in a heavy two-handed smash to throw a ball of red magma energy (do NOT draw the energy ball itself) (release frame); Frame 6: arms fully extended forward, follow-through; Frame 7: arms still forward, body leaning in; Frame 8: arms lowering, returning to the fighting stance.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 9. `characters/brutus/brutus_reactions.png`  (SHEET 3 - DEFENCE AND DEFEAT; attach brutus_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: BRUTUS: a huge, very muscular male brawler, extra-wide shoulders and thick arms (about 1.2 times wider than a normal fighter), dark-brown skin, bald head, thick black beard, angry expression, open dark-red sleeveless leather vest showing the chest, dark-grey baggy trousers, a wide gold belt buckle, spiked steel bracers on both forearms, heavy black boots. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - BLOCK (2 frames, columns 1-2, a standing block, hold on the last frame): Frame 1: arms start to rise to guard, body leaning back slightly; Frame 2: full standing guard, both forearms crossed in front of the face, torso leaning slightly back.

ROW 2 - HIT (3 frames, columns 1-3, a hit reaction (flinch) after being punched in the face; no effects drawn, only the character): Frame 1: impact: head snaps back, face grimacing, body jolted backward; Frame 2: maximum recoil: torso bent back, one foot sliding backwards; Frame 3: starting to recover, head coming forward again.

ROW 3 - CROUCH (2 frames, columns 1-2, going into a crouch and holding it): Frame 1: halfway down into a crouch, knees bent, fists up; Frame 2: full low crouch, torso low, fists guarding the face, hold pose.

ROW 4 - KO (6 frames, columns 1-6, being knocked out and falling backwards; the last frame is the final defeated pose): Frame 1: staggering backwards, head down, arms hanging; Frame 2: knees buckling, falling backwards; Frame 3: falling, body tilted back at 45 degrees; Frame 4: hits the ground hard on the back; Frame 5: slight bounce, limbs loose; Frame 6: lying completely still, defeated, eyes closed, hold pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 10. `characters/brutus/brutus_extras.png`  (SHEET 4 - EXTRAS (make later); attach brutus_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: BRUTUS: a huge, very muscular male brawler, extra-wide shoulders and thick arms (about 1.2 times wider than a normal fighter), dark-brown skin, bald head, thick black beard, angry expression, open dark-red sleeveless leather vest showing the chest, dark-grey baggy trousers, a wide gold belt buckle, spiked steel bracers on both forearms, heavy black boots. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 3 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - KNOCKDOWN (6 frames, columns 1-6, being knocked down and landing on the back; the character moves LEFT (backwards) as they fall): Frame 1: struck, body lifted off the ground, leaning back; Frame 2: flying backwards through the air, body almost horizontal; Frame 3: tumbling, feet above the head height of the body; Frame 4: slamming onto the ground on the back; Frame 5: small bounce, body slightly lifted; Frame 6: lying flat on the back on the ground, arms spread, hold pose.

ROW 2 - GETUP (5 frames, columns 1-5, getting up from the ground back into the fighting stance): Frame 1: lying flat on the back; Frame 2: rolling up, one hand pushing on the ground; Frame 3: kneeling on one knee, head up; Frame 4: rising to standing, fists coming up; Frame 5: back in the fighting stance.

ROW 3 - WIN (6 frames, columns 1-6, a victory celebration, ending in a held pose): Frame 1: standing straight, catching breath; Frame 2: raising one fist toward the sky; Frame 3: fist high, chest out, shouting; Frame 4: holding the victory pose, confident smile; Frame 5: slight bounce of the victory pose; Frame 6: holding the victory pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```


---

# CHARACTER: Valeria (rushdown assassin)

### 11. `characters/valeria/valeria_model.png`  (make FIRST, no attachment)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

TASK: ONE character model sheet of ONE character: VALERIA: a slim, agile female assassin, light-tan skin, sharp green eyes, red hair tied in two buns with loose strands, black crop top with gold trim, short black shorts with a crimson sash, gold wraps on both forearms, black wrapped legs, light black boots with gold buckles.
Draw the SAME character FOUR times in a single horizontal row with wide empty gaps between them, all at exactly the same scale, feet on the same line, full body visible and nothing cropped: (1) front view in a relaxed standing pose, (2) side view facing right in a relaxed standing pose, (3) back view in a relaxed standing pose, (4) side view facing RIGHT in a ready fighting stance: knees bent, front fist at chin height, rear fist near the jaw, intense expression. Only this one character, no text, no labels.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 12. `characters/valeria/valeria_locomotion.png`  (SHEET 1 - MOVEMENT; attach valeria_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: VALERIA: a slim, agile female assassin, light-tan skin, sharp green eyes, red hair tied in two buns with loose strands, black crop top with gold trim, short black shorts with a crimson sash, gold wraps on both forearms, black wrapped legs, light black boots with gold buckles. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - IDLE (6 frames, columns 1-6, a seamless looping breathing cycle): Frame 1: relaxed fighting stance, fists raised near the chin, knees slightly bent; Frame 2: chest rises by one pixel, body a tiny bit taller; Frame 3: highest point of the breath, shoulders slightly raised; Frame 4: chest starts to lower; Frame 5: knees dip slightly, body a tiny bit lower; Frame 6: lowest point, almost identical to frame 1 so the loop is seamless.

ROW 2 - WALK FORWARD (8 frames, columns 1-8, a seamless looping walk cycle moving to the right, fists kept up in guard): Frame 1: right foot far forward, left foot back, guard up; Frame 2: right foot lands, body lowest; Frame 3: left leg passes under the body, body rising; Frame 4: left foot lifted, high point; Frame 5: left foot far forward, right foot back, guard up; Frame 6: left foot lands, body lowest; Frame 7: right leg passes under the body, body rising; Frame 8: right foot lifted, high point.

ROW 3 - WALK BACK (8 frames, columns 1-8, a seamless looping backward walk (retreat), fists kept up in guard, still facing right): Frame 1: left foot far back, right foot forward, guard up, leaning slightly back; Frame 2: left foot lands behind, body lowest; Frame 3: right leg slides back, body rising; Frame 4: right foot lifted, high point; Frame 5: right foot far back, left foot forward, guard up; Frame 6: right foot lands behind, body lowest; Frame 7: left leg slides back, body rising; Frame 8: left foot lifted, high point.

ROW 4 - JUMP (6 frames, columns 1-6, a full jump arc; frames 2 to 5 are in the air (feet above the baseline), frames 1 and 6 on the ground): Frame 1: knees bent deeply, preparing to jump; Frame 2: pushing off the ground, legs stretching, body rising; Frame 3: rising, knees tucked, fists up; Frame 4: top of the jump, knees tucked high; Frame 5: falling, legs extending downward; Frame 6: landing impact, knees bent absorbing the landing.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 13. `characters/valeria/valeria_attacks.png`  (SHEET 2 - ATTACKS; attach valeria_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: VALERIA: a slim, agile female assassin, light-tan skin, sharp green eyes, red hair tied in two buns with loose strands, black crop top with gold trim, short black shorts with a crimson sash, gold wraps on both forearms, black wrapped legs, light black boots with gold buckles. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - PUNCH LIGHT (5 frames, columns 1-5, a fast jab with the front hand): Frame 1: fighting stance, weight shifting; Frame 2: front arm pulled back, shoulder twisting; Frame 3: ARM FULLY EXTENDED jab, fist at head height (contact frame); Frame 4: arm still extended, slight lean forward; Frame 5: arm pulled back to guard, returning to stance.

ROW 2 - PUNCH HEAVY (7 frames, columns 1-7, a slow, powerful straight punch with the rear hand): Frame 1: fighting stance; Frame 2: body lowers, knees bend, rear fist pulled far back; Frame 3: torso twists back, maximum wind-up; Frame 4: torso whips forward, rear fist starting to travel; Frame 5: BIG LUNGING PUNCH, rear arm fully extended, front foot stepping forward (contact frame); Frame 6: follow-through, body leaning far forward; Frame 7: recovering back to the fighting stance.

ROW 3 - KICK (7 frames, columns 1-7, a strong front kick with the front leg): Frame 1: fighting stance; Frame 2: weight shifts onto the back leg, front knee starts lifting; Frame 3: knee lifted high, leg chambered; Frame 4: LEG FULLY EXTENDED in a horizontal front kick at waist height (contact frame); Frame 5: kick held, torso leaning back for balance; Frame 6: leg pulled back to the chambered position; Frame 7: foot lands, back to the fighting stance.

ROW 4 - SPECIAL (8 frames, columns 1-8, a special-move throw. The character sweeps one open hand across the body and flicks it forward to throw a crimson fire ball (do NOT draw the fire ball itself)): Frame 1: fighting stance, beginning to crouch; Frame 2: hands drawn back to the hip, gathering energy, body low; Frame 3: gathering energy, body tense, leaning back; Frame 4: hands begin to thrust forward; Frame 5: sweeps one open hand across the body and flicks it forward to throw a crimson fire ball (do NOT draw the fire ball itself) (release frame); Frame 6: arms fully extended forward, follow-through; Frame 7: arms still forward, body leaning in; Frame 8: arms lowering, returning to the fighting stance.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 14. `characters/valeria/valeria_reactions.png`  (SHEET 3 - DEFENCE AND DEFEAT; attach valeria_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: VALERIA: a slim, agile female assassin, light-tan skin, sharp green eyes, red hair tied in two buns with loose strands, black crop top with gold trim, short black shorts with a crimson sash, gold wraps on both forearms, black wrapped legs, light black boots with gold buckles. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - BLOCK (2 frames, columns 1-2, a standing block, hold on the last frame): Frame 1: arms start to rise to guard, body leaning back slightly; Frame 2: full standing guard, both forearms crossed in front of the face, torso leaning slightly back.

ROW 2 - HIT (3 frames, columns 1-3, a hit reaction (flinch) after being punched in the face; no effects drawn, only the character): Frame 1: impact: head snaps back, face grimacing, body jolted backward; Frame 2: maximum recoil: torso bent back, one foot sliding backwards; Frame 3: starting to recover, head coming forward again.

ROW 3 - CROUCH (2 frames, columns 1-2, going into a crouch and holding it): Frame 1: halfway down into a crouch, knees bent, fists up; Frame 2: full low crouch, torso low, fists guarding the face, hold pose.

ROW 4 - KO (6 frames, columns 1-6, being knocked out and falling backwards; the last frame is the final defeated pose): Frame 1: staggering backwards, head down, arms hanging; Frame 2: knees buckling, falling backwards; Frame 3: falling, body tilted back at 45 degrees; Frame 4: hits the ground hard on the back; Frame 5: slight bounce, limbs loose; Frame 6: lying completely still, defeated, eyes closed, hold pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 15. `characters/valeria/valeria_extras.png`  (SHEET 4 - EXTRAS (make later); attach valeria_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: VALERIA: a slim, agile female assassin, light-tan skin, sharp green eyes, red hair tied in two buns with loose strands, black crop top with gold trim, short black shorts with a crimson sash, gold wraps on both forearms, black wrapped legs, light black boots with gold buckles. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 3 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - KNOCKDOWN (6 frames, columns 1-6, being knocked down and landing on the back; the character moves LEFT (backwards) as they fall): Frame 1: struck, body lifted off the ground, leaning back; Frame 2: flying backwards through the air, body almost horizontal; Frame 3: tumbling, feet above the head height of the body; Frame 4: slamming onto the ground on the back; Frame 5: small bounce, body slightly lifted; Frame 6: lying flat on the back on the ground, arms spread, hold pose.

ROW 2 - GETUP (5 frames, columns 1-5, getting up from the ground back into the fighting stance): Frame 1: lying flat on the back; Frame 2: rolling up, one hand pushing on the ground; Frame 3: kneeling on one knee, head up; Frame 4: rising to standing, fists coming up; Frame 5: back in the fighting stance.

ROW 3 - WIN (6 frames, columns 1-6, a victory celebration, ending in a held pose): Frame 1: standing straight, catching breath; Frame 2: raising one fist toward the sky; Frame 3: fist high, chest out, shouting; Frame 4: holding the victory pose, confident smile; Frame 5: slight bounce of the victory pose; Frame 6: holding the victory pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```


---

# CHARACTER: Mira (storm mage, zoner)

### 16. `characters/mira/mira_model.png`  (make FIRST, no attachment)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

TASK: ONE character model sheet of ONE character: MIRA: a tall slender female storm mage, dark-brown skin, glowing cyan eyes, long flowing silver-white hair, a dark-navy combat robe with cyan trim and a side slit, fingerless dark gloves, glowing cyan rune tattoos on both arms, dark boots with cyan details.
Draw the SAME character FOUR times in a single horizontal row with wide empty gaps between them, all at exactly the same scale, feet on the same line, full body visible and nothing cropped: (1) front view in a relaxed standing pose, (2) side view facing right in a relaxed standing pose, (3) back view in a relaxed standing pose, (4) side view facing RIGHT in a ready fighting stance: knees bent, front fist at chin height, rear fist near the jaw, intense expression. Only this one character, no text, no labels.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 17. `characters/mira/mira_locomotion.png`  (SHEET 1 - MOVEMENT; attach mira_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: MIRA: a tall slender female storm mage, dark-brown skin, glowing cyan eyes, long flowing silver-white hair, a dark-navy combat robe with cyan trim and a side slit, fingerless dark gloves, glowing cyan rune tattoos on both arms, dark boots with cyan details. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - IDLE (6 frames, columns 1-6, a seamless looping breathing cycle): Frame 1: relaxed fighting stance, fists raised near the chin, knees slightly bent; Frame 2: chest rises by one pixel, body a tiny bit taller; Frame 3: highest point of the breath, shoulders slightly raised; Frame 4: chest starts to lower; Frame 5: knees dip slightly, body a tiny bit lower; Frame 6: lowest point, almost identical to frame 1 so the loop is seamless.

ROW 2 - WALK FORWARD (8 frames, columns 1-8, a seamless looping walk cycle moving to the right, fists kept up in guard): Frame 1: right foot far forward, left foot back, guard up; Frame 2: right foot lands, body lowest; Frame 3: left leg passes under the body, body rising; Frame 4: left foot lifted, high point; Frame 5: left foot far forward, right foot back, guard up; Frame 6: left foot lands, body lowest; Frame 7: right leg passes under the body, body rising; Frame 8: right foot lifted, high point.

ROW 3 - WALK BACK (8 frames, columns 1-8, a seamless looping backward walk (retreat), fists kept up in guard, still facing right): Frame 1: left foot far back, right foot forward, guard up, leaning slightly back; Frame 2: left foot lands behind, body lowest; Frame 3: right leg slides back, body rising; Frame 4: right foot lifted, high point; Frame 5: right foot far back, left foot forward, guard up; Frame 6: right foot lands behind, body lowest; Frame 7: left leg slides back, body rising; Frame 8: left foot lifted, high point.

ROW 4 - JUMP (6 frames, columns 1-6, a full jump arc; frames 2 to 5 are in the air (feet above the baseline), frames 1 and 6 on the ground): Frame 1: knees bent deeply, preparing to jump; Frame 2: pushing off the ground, legs stretching, body rising; Frame 3: rising, knees tucked, fists up; Frame 4: top of the jump, knees tucked high; Frame 5: falling, legs extending downward; Frame 6: landing impact, knees bent absorbing the landing.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 18. `characters/mira/mira_attacks.png`  (SHEET 2 - ATTACKS; attach mira_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: MIRA: a tall slender female storm mage, dark-brown skin, glowing cyan eyes, long flowing silver-white hair, a dark-navy combat robe with cyan trim and a side slit, fingerless dark gloves, glowing cyan rune tattoos on both arms, dark boots with cyan details. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - PUNCH LIGHT (5 frames, columns 1-5, a fast jab with the front hand): Frame 1: fighting stance, weight shifting; Frame 2: front arm pulled back, shoulder twisting; Frame 3: ARM FULLY EXTENDED jab, fist at head height (contact frame); Frame 4: arm still extended, slight lean forward; Frame 5: arm pulled back to guard, returning to stance.

ROW 2 - PUNCH HEAVY (7 frames, columns 1-7, a slow, powerful straight punch with the rear hand): Frame 1: fighting stance; Frame 2: body lowers, knees bend, rear fist pulled far back; Frame 3: torso twists back, maximum wind-up; Frame 4: torso whips forward, rear fist starting to travel; Frame 5: BIG LUNGING PUNCH, rear arm fully extended, front foot stepping forward (contact frame); Frame 6: follow-through, body leaning far forward; Frame 7: recovering back to the fighting stance.

ROW 3 - KICK (7 frames, columns 1-7, a strong front kick with the front leg): Frame 1: fighting stance; Frame 2: weight shifts onto the back leg, front knee starts lifting; Frame 3: knee lifted high, leg chambered; Frame 4: LEG FULLY EXTENDED in a horizontal front kick at waist height (contact frame); Frame 5: kick held, torso leaning back for balance; Frame 6: leg pulled back to the chambered position; Frame 7: foot lands, back to the fighting stance.

ROW 4 - SPECIAL (8 frames, columns 1-8, a special-move throw. The character raises one hand up, then points it forward to launch a ball of cyan lightning (do NOT draw the lightning ball itself)): Frame 1: fighting stance, beginning to crouch; Frame 2: hands drawn back to the hip, gathering energy, body low; Frame 3: gathering energy, body tense, leaning back; Frame 4: hands begin to thrust forward; Frame 5: raises one hand up, then points it forward to launch a ball of cyan lightning (do NOT draw the lightning ball itself) (release frame); Frame 6: arms fully extended forward, follow-through; Frame 7: arms still forward, body leaning in; Frame 8: arms lowering, returning to the fighting stance.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 19. `characters/mira/mira_reactions.png`  (SHEET 3 - DEFENCE AND DEFEAT; attach mira_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: MIRA: a tall slender female storm mage, dark-brown skin, glowing cyan eyes, long flowing silver-white hair, a dark-navy combat robe with cyan trim and a side slit, fingerless dark gloves, glowing cyan rune tattoos on both arms, dark boots with cyan details. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - BLOCK (2 frames, columns 1-2, a standing block, hold on the last frame): Frame 1: arms start to rise to guard, body leaning back slightly; Frame 2: full standing guard, both forearms crossed in front of the face, torso leaning slightly back.

ROW 2 - HIT (3 frames, columns 1-3, a hit reaction (flinch) after being punched in the face; no effects drawn, only the character): Frame 1: impact: head snaps back, face grimacing, body jolted backward; Frame 2: maximum recoil: torso bent back, one foot sliding backwards; Frame 3: starting to recover, head coming forward again.

ROW 3 - CROUCH (2 frames, columns 1-2, going into a crouch and holding it): Frame 1: halfway down into a crouch, knees bent, fists up; Frame 2: full low crouch, torso low, fists guarding the face, hold pose.

ROW 4 - KO (6 frames, columns 1-6, being knocked out and falling backwards; the last frame is the final defeated pose): Frame 1: staggering backwards, head down, arms hanging; Frame 2: knees buckling, falling backwards; Frame 3: falling, body tilted back at 45 degrees; Frame 4: hits the ground hard on the back; Frame 5: slight bounce, limbs loose; Frame 6: lying completely still, defeated, eyes closed, hold pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 20. `characters/mira/mira_extras.png`  (SHEET 4 - EXTRAS (make later); attach mira_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: MIRA: a tall slender female storm mage, dark-brown skin, glowing cyan eyes, long flowing silver-white hair, a dark-navy combat robe with cyan trim and a side slit, fingerless dark gloves, glowing cyan rune tattoos on both arms, dark boots with cyan details. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 3 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - KNOCKDOWN (6 frames, columns 1-6, being knocked down and landing on the back; the character moves LEFT (backwards) as they fall): Frame 1: struck, body lifted off the ground, leaning back; Frame 2: flying backwards through the air, body almost horizontal; Frame 3: tumbling, feet above the head height of the body; Frame 4: slamming onto the ground on the back; Frame 5: small bounce, body slightly lifted; Frame 6: lying flat on the back on the ground, arms spread, hold pose.

ROW 2 - GETUP (5 frames, columns 1-5, getting up from the ground back into the fighting stance): Frame 1: lying flat on the back; Frame 2: rolling up, one hand pushing on the ground; Frame 3: kneeling on one knee, head up; Frame 4: rising to standing, fists coming up; Frame 5: back in the fighting stance.

ROW 3 - WIN (6 frames, columns 1-6, a victory celebration, ending in a held pose): Frame 1: standing straight, catching breath; Frame 2: raising one fist toward the sky; Frame 3: fist high, chest out, shouting; Frame 4: holding the victory pose, confident smile; Frame 5: slight bounce of the victory pose; Frame 6: holding the victory pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```


---

# EFFECTS

### 21. `fx/fx_sheet1.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos.

TASK: ONE visual-effects sprite sheet, a strict grid of 4 ROWS and 6 COLUMNS. Each row is one effect animation drawn left to right in time order starting in column 1; unused columns stay empty. Every cell is the same size, each effect is centred in its cell and never touches the cell edge, clear empty space between cells. No grid lines, borders, labels or numbers. Only the effects: no characters, no hands, no text.

ROW 1 - HIT SPARK (6 frames): a white-yellow impact flash for a punch hit as spiky star-shaped pixel bursts: tiny bright white dot; small white-yellow star burst; large spiky white-yellow burst with orange tips (peak); burst fading with thinner spikes; a few orange spark lines flying outward; last tiny orange sparks.

ROW 2 - BLOCK SPARK (5 frames): a blue-white metallic block flash: small blue-white dot; growing ring of blue-white light with short lines; largest ring with bright white centre (peak); ring fading; a few tiny blue sparks.

ROW 3 - ORANGE FIREBALL (4 frames, looping): an orange and yellow fire energy ball with a short flame tail pointing left, flying to the right; the same ball in 4 slightly different flame shapes so it loops smoothly.

ROW 4 - ORANGE FIREBALL EXPLOSION (6 frames): the explosion when that ball hits a target: small bright flash; round burst growing; largest burst with a bright core (peak); burst breaking into sparks; sparks flying outward; last tiny embers.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### 22. `fx/fx_sheet2.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos.

TASK: ONE visual-effects sprite sheet, a strict grid of 4 ROWS and 6 COLUMNS. Each row is one effect animation drawn left to right in time order starting in column 1; unused columns stay empty. Every cell is the same size, each effect is centred in its cell and never touches the cell edge, clear empty space between cells. No grid lines, borders, labels or numbers. Only the effects: no characters, no hands, no text.

ROW 1 - DUST PUFF (5 frames): a small grey-beige dust puff kicked up at the feet on landing, round pixel clouds on a flat bottom line: tiny puff; puff grows and splits in two; two larger round clouds; clouds spreading and thinning; faint small remains.

ROW 2 - RED FIREBALL (4 frames, looping): a dark-red magma energy ball with black cracks and a short ember tail pointing left, flying to the right; 4 slightly different flame shapes so it loops.

ROW 3 - CRIMSON FIREBALL (4 frames, looping): a crimson and orange flame ball with a swirling fire tail pointing left, flying to the right; 4 slightly different flame shapes so it loops.

ROW 4 - CYAN LIGHTNING BALL (4 frames, looping): a cyan and white lightning energy ball with small electric arcs and a short tail pointing left, flying to the right; 4 slightly different shapes so it loops.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```


---

# STAGES (opaque backgrounds)

### 23. `stages/stage1_neon_city.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos.

TASK: ONE side-view background for a 2D fighting game, wide 16:9 composition. A rainy neon cyberpunk city street at night: tall buildings with glowing pink, cyan and purple neon signs (no readable text), wet reflective road, parked vehicles far behind, steam vents, power lines, a big moon behind the skyline.
Layout: the flat fighting floor is a clean, level, readable surface occupying the BOTTOM 22 percent of the image with no objects on it; the detailed scenery fills the upper part with strong depth (far, middle and near layers). Absolutely NO characters, NO people, NO text, NO logos, NO UI, NO fog covering the floor. Fully opaque image, no transparency. Strict pixel-art look: no anti-aliasing, no blur, no photographic textures.
```

### 24. `stages/stage2_temple.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos.

TASK: ONE side-view background for a 2D fighting game, wide 16:9 composition. A hilltop dojo temple courtyard at sunset: large red torii gate, stone lanterns, cherry-blossom trees with falling petals, far mountains and a huge orange sun, wooden dojo building, stone floor tiles.
Layout: the flat fighting floor is a clean, level, readable surface occupying the BOTTOM 22 percent of the image with no objects on it; the detailed scenery fills the upper part with strong depth (far, middle and near layers). Absolutely NO characters, NO people, NO text, NO logos, NO UI, NO fog covering the floor. Fully opaque image, no transparency. Strict pixel-art look: no anti-aliasing, no blur, no photographic textures.
```

### 25. `stages/stage3_volcano.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos.

TASK: ONE side-view background for a 2D fighting game, wide 16:9 composition. A volcano arena at night: black stone ring platform with glowing orange cracks, rivers of lava in the background, a giant erupting volcano with an ash-filled red sky, burning torches on iron poles, floating embers.
Layout: the flat fighting floor is a clean, level, readable surface occupying the BOTTOM 22 percent of the image with no objects on it; the detailed scenery fills the upper part with strong depth (far, middle and near layers). Absolutely NO characters, NO people, NO text, NO logos, NO UI, NO fog covering the floor. Fully opaque image, no transparency. Strict pixel-art look: no anti-aliasing, no blur, no photographic textures.
```


---

# USER INTERFACE

### 26. `ui/title_logo.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos.

TASK: a game title logo that reads exactly EMBER TOURNAMENT on two lines: EMBER on the first line (large) and TOURNAMENT on the second line (smaller, wide letter spacing). Spelled exactly E-M-B-E-R and T-O-U-R-N-A-M-E-N-T. Big chunky pixel-art lettering with a thick dark outline, fiery orange-to-yellow metallic fill with glowing embers floating off the letters, a small flame crest between the two lines. Only the logo, centred, with empty space around it. Check that the spelling is exactly EMBER TOURNAMENT.

Output a PNG with a REAL transparent background (alpha channel), no checkerboard, no extra text.
```

### 27. `ui/portraits.png`  (one sheet with all 4 portraits; attach the 4 model sheets)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos.

Use the attached model sheets of these four characters: KAITO: a young male martial artist, athletic medium build, tan skin, determined dark-brown eyes, short spiky black hair, small scar on the left cheek, white sleeveless karate gi jacket open at the chest, white loose gi trousers, a red cloth sash belt with two hanging ends, red hand wraps on both fists, bare feet with red ankle wraps | BRUTUS: a huge, very muscular male brawler, extra-wide shoulders and thick arms (about 1.2 times wider than a normal fighter), dark-brown skin, bald head, thick black beard, angry expression, open dark-red sleeveless leather vest showing the chest, dark-grey baggy trousers, a wide gold belt buckle, spiked steel bracers on both forearms, heavy black boots | VALERIA: a slim, agile female assassin, light-tan skin, sharp green eyes, red hair tied in two buns with loose strands, black crop top with gold trim, short black shorts with a crimson sash, gold wraps on both forearms, black wrapped legs, light black boots with gold buckles | MIRA: a tall slender female storm mage, dark-brown skin, glowing cyan eyes, long flowing silver-white hair, a dark-navy combat robe with cyan trim and a side slit, fingerless dark gloves, glowing cyan rune tattoos on both arms, dark boots with cyan details.
TASK: ONE image with FOUR head-and-shoulders portrait icons in a single horizontal row with wide gaps, in this order: KAITO, BRUTUS, VALERIA, MIRA. Each is facing slightly right with a fierce expression, same size, centred, identical to its model sheet. No text, no labels.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```


---

Total prompts: 27
