# THE HOLLOW EMPEROR - sprite sheets for the final boss

Make them in order in ChatGPT (one image each). Attach `emperor_model.png` to every sheet after the first.
Save as `Assets/Hollow Emperor <name>.png` (names below) and tell me - I cut them into the game.
Files wanted: model, locomotion, attacks, reactions, extras (+ optional portrait and boss-intro picture at the end).

# CHARACTER: The Hollow Emperor (final boss)

### `characters/emperor/emperor_model.png`  (make FIRST, no attachment)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

TASK: ONE character model sheet of ONE character: THE HOLLOW EMPEROR: a tall, muscular man, a dark burning mirror-copy of a repairman hero: short black curly hair, a short beard and thin glasses, wearing a torn, ash-black version of a rolled-sleeve work shirt and dark trousers with a worn tool belt. His whole body is made of black stone-like skin cracked with glowing violet light, glowing violet eyes with no pupils, black-violet fire licking from his shoulders and fists, and a glowing violet letter R burning on his chest and on his right hand. Dark armoured boots with violet cracks.
Draw the SAME character FOUR times in a single horizontal row with wide empty gaps between them, all at exactly the same scale, feet on the same line, full body visible and nothing cropped: (1) front view in a relaxed standing pose, (2) side view facing right in a relaxed standing pose, (3) back view in a relaxed standing pose, (4) side view facing RIGHT in a ready fighting stance: knees bent, front fist at chin height, rear fist near the jaw, intense expression. Only this one character, no text, no labels.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### `characters/emperor/emperor_locomotion.png`  (SHEET 1 - MOVEMENT; attach emperor_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: THE HOLLOW EMPEROR: a tall, muscular man, a dark burning mirror-copy of a repairman hero: short black curly hair, a short beard and thin glasses, wearing a torn, ash-black version of a rolled-sleeve work shirt and dark trousers with a worn tool belt. His whole body is made of black stone-like skin cracked with glowing violet light, glowing violet eyes with no pupils, black-violet fire licking from his shoulders and fists, and a glowing violet letter R burning on his chest and on his right hand. Dark armoured boots with violet cracks. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - IDLE (6 frames, columns 1-6, a seamless looping breathing cycle): Frame 1: relaxed fighting stance, fists raised near the chin, knees slightly bent; Frame 2: chest rises by one pixel, body a tiny bit taller; Frame 3: highest point of the breath, shoulders slightly raised; Frame 4: chest starts to lower; Frame 5: knees dip slightly, body a tiny bit lower; Frame 6: lowest point, almost identical to frame 1 so the loop is seamless.

ROW 2 - WALK FORWARD (8 frames, columns 1-8, a seamless looping walk cycle moving to the right, fists kept up in guard): Frame 1: right foot far forward, left foot back, guard up; Frame 2: right foot lands, body lowest; Frame 3: left leg passes under the body, body rising; Frame 4: left foot lifted, high point; Frame 5: left foot far forward, right foot back, guard up; Frame 6: left foot lands, body lowest; Frame 7: right leg passes under the body, body rising; Frame 8: right foot lifted, high point.

ROW 3 - WALK BACK (8 frames, columns 1-8, a seamless looping backward walk (retreat), fists kept up in guard, still facing right): Frame 1: left foot far back, right foot forward, guard up, leaning slightly back; Frame 2: left foot lands behind, body lowest; Frame 3: right leg slides back, body rising; Frame 4: right foot lifted, high point; Frame 5: right foot far back, left foot forward, guard up; Frame 6: right foot lands behind, body lowest; Frame 7: left leg slides back, body rising; Frame 8: left foot lifted, high point.

ROW 4 - JUMP (6 frames, columns 1-6, a full jump arc; frames 2 to 5 are in the air (feet above the baseline), frames 1 and 6 on the ground): Frame 1: knees bent deeply, preparing to jump; Frame 2: pushing off the ground, legs stretching, body rising; Frame 3: rising, knees tucked, fists up; Frame 4: top of the jump, knees tucked high; Frame 5: falling, legs extending downward; Frame 6: landing impact, knees bent absorbing the landing.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### `characters/emperor/emperor_attacks.png`  (SHEET 2 - ATTACKS; attach emperor_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: THE HOLLOW EMPEROR: a tall, muscular man, a dark burning mirror-copy of a repairman hero: short black curly hair, a short beard and thin glasses, wearing a torn, ash-black version of a rolled-sleeve work shirt and dark trousers with a worn tool belt. His whole body is made of black stone-like skin cracked with glowing violet light, glowing violet eyes with no pupils, black-violet fire licking from his shoulders and fists, and a glowing violet letter R burning on his chest and on his right hand. Dark armoured boots with violet cracks. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - PUNCH LIGHT (5 frames, columns 1-5, a fast jab with the front hand): Frame 1: fighting stance, weight shifting; Frame 2: front arm pulled back, shoulder twisting; Frame 3: ARM FULLY EXTENDED jab, fist at head height (contact frame); Frame 4: arm still extended, slight lean forward; Frame 5: arm pulled back to guard, returning to stance.

ROW 2 - PUNCH HEAVY (7 frames, columns 1-7, a slow, powerful straight punch with the rear hand): Frame 1: fighting stance; Frame 2: body lowers, knees bend, rear fist pulled far back; Frame 3: torso twists back, maximum wind-up; Frame 4: torso whips forward, rear fist starting to travel; Frame 5: BIG LUNGING PUNCH, rear arm fully extended, front foot stepping forward (contact frame); Frame 6: follow-through, body leaning far forward; Frame 7: recovering back to the fighting stance.

ROW 3 - KICK (7 frames, columns 1-7, a strong front kick with the front leg): Frame 1: fighting stance; Frame 2: weight shifts onto the back leg, front knee starts lifting; Frame 3: knee lifted high, leg chambered; Frame 4: LEG FULLY EXTENDED in a horizontal front kick at waist height (contact frame); Frame 5: kick held, torso leaning back for balance; Frame 6: leg pulled back to the chambered position; Frame 7: foot lands, back to the fighting stance.

ROW 4 - SPECIAL (8 frames, columns 1-8, a special-move throw. The character raises one hand up, then points it forward to launch a ball of black-violet fire (do NOT draw the fire ball itself)): Frame 1: fighting stance, beginning to crouch; Frame 2: hands drawn back to the hip, gathering energy, body low; Frame 3: gathering energy, body tense, leaning back; Frame 4: hands begin to thrust forward; Frame 5: raises one hand up, then points it forward to launch a ball of black-violet fire (do NOT draw the fire ball itself) (release frame); Frame 6: arms fully extended forward, follow-through; Frame 7: arms still forward, body leaning in; Frame 8: arms lowering, returning to the fighting stance.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### `characters/emperor/emperor_reactions.png`  (SHEET 3 - DEFENCE AND DEFEAT; attach emperor_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: THE HOLLOW EMPEROR: a tall, muscular man, a dark burning mirror-copy of a repairman hero: short black curly hair, a short beard and thin glasses, wearing a torn, ash-black version of a rolled-sleeve work shirt and dark trousers with a worn tool belt. His whole body is made of black stone-like skin cracked with glowing violet light, glowing violet eyes with no pupils, black-violet fire licking from his shoulders and fists, and a glowing violet letter R burning on his chest and on his right hand. Dark armoured boots with violet cracks. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 4 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - BLOCK (2 frames, columns 1-2, a standing block, hold on the last frame): Frame 1: arms start to rise to guard, body leaning back slightly; Frame 2: full standing guard, both forearms crossed in front of the face, torso leaning slightly back.

ROW 2 - HIT (3 frames, columns 1-3, a hit reaction (flinch) after being punched in the face; no effects drawn, only the character): Frame 1: impact: head snaps back, face grimacing, body jolted backward; Frame 2: maximum recoil: torso bent back, one foot sliding backwards; Frame 3: starting to recover, head coming forward again.

ROW 3 - CROUCH (2 frames, columns 1-2, going into a crouch and holding it): Frame 1: halfway down into a crouch, knees bent, fists up; Frame 2: full low crouch, torso low, fists guarding the face, hold pose.

ROW 4 - KO (6 frames, columns 1-6, being knocked out and falling backwards; the last frame is the final defeated pose): Frame 1: staggering backwards, head down, arms hanging; Frame 2: knees buckling, falling backwards; Frame 3: falling, body tilted back at 45 degrees; Frame 4: hits the ground hard on the back; Frame 5: slight bounce, limbs loose; Frame 6: lying completely still, defeated, eyes closed, hold pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```

### `characters/emperor/emperor_extras.png`  (SHEET 4 - EXTRAS (make later); attach emperor_model.png)
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached model sheet of this exact character: THE HOLLOW EMPEROR: a tall, muscular man, a dark burning mirror-copy of a repairman hero: short black curly hair, a short beard and thin glasses, wearing a torn, ash-black version of a rolled-sleeve work shirt and dark trousers with a worn tool belt. His whole body is made of black stone-like skin cracked with glowing violet light, glowing violet eyes with no pupils, black-violet fire licking from his shoulders and fists, and a glowing violet letter R burning on his chest and on his right hand. Dark armoured boots with violet cracks. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL to the model sheet in EVERY cell of the whole image.

TASK: ONE animation sprite sheet of this ONE character, laid out as a strict grid of 3 ROWS and 8 COLUMNS on a single image. Each row is one animation, drawn left to right in time order starting in column 1; leave the unused columns of a row completely empty. Every cell has the same size. In every cell the character is centred horizontally, never touches the cell edge, and is drawn at exactly the same scale. In every row the feet rest on the same invisible baseline near the bottom of the cell (except frames where the character is in the air or on the ground lying down). The character faces RIGHT in every cell. Leave clear empty space between cells. Do not draw grid lines, borders, labels or numbers.

ROW 1 - KNOCKDOWN (6 frames, columns 1-6, being knocked down and landing on the back; the character moves LEFT (backwards) as they fall): Frame 1: struck, body lifted off the ground, leaning back; Frame 2: flying backwards through the air, body almost horizontal; Frame 3: tumbling, feet above the head height of the body; Frame 4: slamming onto the ground on the back; Frame 5: small bounce, body slightly lifted; Frame 6: lying flat on the back on the ground, arms spread, hold pose.

ROW 2 - GETUP (5 frames, columns 1-5, getting up from the ground back into the fighting stance): Frame 1: lying flat on the back; Frame 2: rolling up, one hand pushing on the ground; Frame 3: kneeling on one knee, head up; Frame 4: rising to standing, fists coming up; Frame 5: back in the fighting stance.

ROW 3 - WIN (6 frames, columns 1-6, a victory celebration, ending in a held pose): Frame 1: standing straight, catching breath; Frame 2: raising one fist toward the sky; Frame 3: fist high, chest out, shouting; Frame 4: holding the victory pose, confident smile; Frame 5: slight bounce of the victory pose; Frame 6: holding the victory pose.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons, no energy effects, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery. Do not draw any text, letters, numbers, labels, borders or grid lines.
```


---


# EXTRA (optional but recommended)

### `Assets/Hollow Emperor Portrait.png`  (attach emperor_model.png)
```
High-quality 16-bit arcade fighting-game pixel art portrait, chest-up, of THE HOLLOW EMPEROR from the attached model sheet: black cracked stone-like skin glowing with violet light, pupil-less glowing violet eyes, short curly black hair, short beard, thin glasses, black-violet fire rising from his shoulders, a glowing violet letter R burning on his chest. Menacing, intense expression, facing slightly to the right, three-quarter view. Solid flat dark-purple background (single colour, no gradient), clean 1-pixel outline, cel shading, no text.
```

### `Assets/story/boss_intro.png`  (16:9, no attachment needed)
```
Cinematic 16-bit pixel art illustration, wide 16:9 landscape, fighting-game boss-intro style: THE HOLLOW EMPEROR (a dark burning copy of a repairman hero, cracked black skin glowing violet, violet pupil-less eyes, black-violet fire, a glowing violet letter R on his chest) rising from a gothic throne in a huge dark hall, five floating glowing cores around him, dramatic purple and black lighting, embers in the air. No text, no letters, no watermark. Keep the bottom third darker.
```
