# SMOOTH victory dances - 16 frames per fighter (two parts)

The first dance sheets had 8 frames, which looks choppy. These are **16 frames per fighter, made as TWO images of 8 frames each**.
Generating 8 at a time keeps the drawing clean and the hands correct.

## How to do it (important)
1. Attach an existing sprite sheet of the fighter to **Part 1** and generate it. Check that the face and clothes match.
2. For **Part 2**, attach the same sheet AND the Part 1 result, so the body and scale continue exactly.
3. If a frame has a bad hand or a different body size, ask ChatGPT to redo only that image, keeping the rest. A few clean 16-frame sets are better than many rough ones.
4. Save as `Assets/dance/<name>_1.png` and `Assets/dance/<name>_2.png` (for example `kaito_1.png`, `kaito_2.png`). Generate at 16:9 landscape (1536x1024 or bigger).
5. Tell me and I will cut them into the game. The old single sheets can stay, the new pair replaces them automatically.

**Rules used in every prompt:** STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

## KAITO - Part 1 of 2  ->  `Assets/dance/kaito_1.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character: KAITO: a young male martial artist, athletic medium build, tan skin, determined dark-brown eyes, short spiky black hair, small scar on the left cheek, white sleeveless karate gi jacket open at the chest, white loose gi trousers, a red cloth sash belt with two hanging ends, red hand wraps on both fists, bare feet with red ankle wraps. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 1 of 2 (frames 1 to 8 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: calm and disciplined: a respectful bow, a slow martial-arts flourish with a sweeping palm, then a proud raised fist. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 1: standing relaxed, fists low; Frame 2: hands begin to rise and join in front of the chest; Frame 3: hands joined at the chest, a slight nod; Frame 4: upper body starts to bend forward; Frame 5: deep respectful bow, head low; Frame 6: body rising from the bow; Frame 7: standing upright, right arm starting to sweep outward; Frame 8: right arm sweeping out, palm open.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## KAITO - Part 2 of 2  ->  `Assets/dance/kaito_2.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character AND the attached Part 1 result (continue exactly from its last frame; the body, scale and feet position must match it): KAITO: a young male martial artist, athletic medium build, tan skin, determined dark-brown eyes, short spiky black hair, small scar on the left cheek, white sleeveless karate gi jacket open at the chest, white loose gi trousers, a red cloth sash belt with two hanging ends, red hand wraps on both fists, bare feet with red ankle wraps. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 2 of 2 (frames 9 to 16 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: calm and disciplined: a respectful bow, a slow martial-arts flourish with a sweeping palm, then a proud raised fist. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 9: palm flourish at full extension, torso twisting slightly; Frame 10: arms drawing back across the body; Frame 11: both arms opening wide, graceful; Frame 12: arms wide, chest open, chin up; Frame 13: right fist starting to rise; Frame 14: right fist rising past the shoulder; Frame 15: fist thrust high into the air, proud; Frame 16: fist lowering back, returning to the standing pose of frame 1.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## BRUTUS - Part 1 of 2  ->  `Assets/dance/brutus_1.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character: BRUTUS: a huge, very muscular male brawler, extra-wide shoulders and thick arms (about 1.2 times wider than a normal fighter), dark-brown skin, bald head, thick black beard, angry expression, open dark-red sleeveless leather vest showing the chest, dark-grey baggy trousers, a wide gold belt buckle, spiked steel bracers on both forearms, heavy black boots. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 1 of 2 (frames 1 to 8 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: loud and aggressive, a showman: chest pounding, flexing, roaring and stomping. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 1: standing proud, fists at his sides; Frame 2: right fist lifting towards the chest; Frame 3: right fist pounds the chest (small impact spark); Frame 4: right fist pulling away; Frame 5: left fist lifting towards the chest; Frame 6: left fist pounds the chest (small impact spark); Frame 7: both arms starting to rise; Frame 8: both arms raised, elbows bent.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## BRUTUS - Part 2 of 2  ->  `Assets/dance/brutus_2.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character AND the attached Part 1 result (continue exactly from its last frame; the body, scale and feet position must match it): BRUTUS: a huge, very muscular male brawler, extra-wide shoulders and thick arms (about 1.2 times wider than a normal fighter), dark-brown skin, bald head, thick black beard, angry expression, open dark-red sleeveless leather vest showing the chest, dark-grey baggy trousers, a wide gold belt buckle, spiked steel bracers on both forearms, heavy black boots. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 2 of 2 (frames 9 to 16 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: loud and aggressive, a showman: chest pounding, flexing, roaring and stomping. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 9: double biceps flex, mouth open roaring; Frame 10: holding the flex, shoulders shaking; Frame 11: arms lowering, leaning forward, still roaring; Frame 12: leaning forward, arms wide towards the crowd; Frame 13: one knee lifting for a stomp; Frame 14: knee at its highest point; Frame 15: boot stomping down, body dropping; Frame 16: settling back to the proud standing pose of frame 1.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## VALERIA - Part 1 of 2  ->  `Assets/dance/valeria_1.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character: VALERIA: a slim, agile female assassin, light-tan skin, sharp green eyes, red hair tied in two buns with loose strands, black crop top with gold trim, short black shorts with a crimson sash, gold wraps on both forearms, black wrapped legs, light black boots with gold buckles. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 1 of 2 (frames 1 to 8 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: quick, flashy and cocky: a dagger spin, a graceful twirl, a kiss to the blade, then a confident pose. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 1: standing, dagger in the right hand, left hand on hip; Frame 2: right wrist flicking, dagger starting to leave the hand; Frame 3: dagger tossed up, arm following it; Frame 4: dagger high above the hand, spinning; Frame 5: dagger spinning, her eyes following it; Frame 6: catching it behind her back; Frame 7: dagger caught, weight shifting, starting to turn; Frame 8: the first quarter of a spin, hair swinging out.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## VALERIA - Part 2 of 2  ->  `Assets/dance/valeria_2.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character AND the attached Part 1 result (continue exactly from its last frame; the body, scale and feet position must match it): VALERIA: a slim, agile female assassin, light-tan skin, sharp green eyes, red hair tied in two buns with loose strands, black crop top with gold trim, short black shorts with a crimson sash, gold wraps on both forearms, black wrapped legs, light black boots with gold buckles. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 2 of 2 (frames 9 to 16 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: quick, flashy and cocky: a dagger spin, a graceful twirl, a kiss to the blade, then a confident pose. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 9: a half twirl, hair flying wide; Frame 10: three-quarter twirl, one leg lifted; Frame 11: landing from the twirl, knees bent; Frame 12: dropping into a low graceful crouch, dagger low; Frame 13: rising from the crouch; Frame 14: standing, lifting the dagger to her lips; Frame 15: kissing the blade and winking; Frame 16: hand back on hip, confident smirk, matching frame 1.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## MIRA - Part 1 of 2  ->  `Assets/dance/mira_1.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character: MIRA: a tall slender female storm mage, dark-brown skin, glowing cyan eyes, long flowing silver-white hair, a dark-navy combat robe with cyan trim and a side slit, fingerless dark gloves, glowing cyan rune tattoos on both arms, dark boots with cyan details. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 1 of 2 (frames 1 to 8 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: elegant and mystical: lightning gathers, a slow graceful spin and a final curtsy. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 1: standing calm, hands lowered; Frame 2: hands starting to rise; Frame 3: hands at chest height, cyan runes starting to glow; Frame 4: hands rising above the chest; Frame 5: hands above the head, runes glowing; Frame 6: arms stretching up high, hair beginning to float; Frame 7: arms spreading out to the sides, hair floating up; Frame 8: arms wide, eyes closed, smiling.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## MIRA - Part 2 of 2  ->  `Assets/dance/mira_2.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character AND the attached Part 1 result (continue exactly from its last frame; the body, scale and feet position must match it): MIRA: a tall slender female storm mage, dark-brown skin, glowing cyan eyes, long flowing silver-white hair, a dark-navy combat robe with cyan trim and a side slit, fingerless dark gloves, glowing cyan rune tattoos on both arms, dark boots with cyan details. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 2 of 2 (frames 9 to 16 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: elegant and mystical: lightning gathers, a slow graceful spin and a final curtsy. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 9: starting a slow turn, robe beginning to flow; Frame 10: quarter turn, robe swirling; Frame 11: half turn, back partly towards the viewer, robe flaring; Frame 12: three-quarter turn, hair trailing; Frame 13: turn finishing, one hand pointing to the sky; Frame 14: arms lowering gracefully; Frame 15: small step back, starting a curtsy; Frame 16: an elegant curtsy, then returning to the pose of frame 1.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## RUDRA - Part 1 of 2  ->  `Assets/dance/rudra_1.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character: RUDRA: a strong Bengali wrestler, dark-brown skin, short black hair with a red headband, a thick moustache, bare muscular chest, white dhoti-style trousers with a red sash, bare feet with wrapped ankles, taped fists. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 1 of 2 (frames 1 to 8 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: proud and powerful: thigh slap, wrestler's flex, victory fist circle and a hand on the heart. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 1: standing proud, hands at his sides; Frame 2: right hand lifting to slap his thigh; Frame 3: slapping the thigh; Frame 4: bending forward, hands on knees; Frame 5: wrestler's low stance, hands on knees, glaring; Frame 6: rising from the stance; Frame 7: standing, both arms starting to flex; Frame 8: side chest pose, both arms flexed.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## RUDRA - Part 2 of 2  ->  `Assets/dance/rudra_2.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character AND the attached Part 1 result (continue exactly from its last frame; the body, scale and feet position must match it): RUDRA: a strong Bengali wrestler, dark-brown skin, short black hair with a red headband, a thick moustache, bare muscular chest, white dhoti-style trousers with a red sash, bare feet with wrapped ankles, taped fists. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 2 of 2 (frames 9 to 16 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: proud and powerful: thigh slap, wrestler's flex, victory fist circle and a hand on the heart. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 9: holding the flex, chest out; Frame 10: right fist starting to rise overhead; Frame 11: fist circling above the head; Frame 12: fist at the top of the circle, shouting; Frame 13: fist thrust to the sky; Frame 14: fist lowering, a wide grin; Frame 15: right hand moving to the heart; Frame 16: hand pressed to his heart, a respectful nod, then back to the pose of frame 1.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## RENO - Part 1 of 2  ->  `Assets/dance/reno_1.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character: RENO: a young man with short wavy black hair, a short black beard, green-framed glasses, a yellow patterned open-collar shirt with rolled sleeves, a dark wristband, blue jeans and dark shoes, an ordinary friendly guy. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 1 of 2 (frames 1 to 8 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: goofy and joyful, an ordinary guy who cannot believe he won: pumping fists, a hip shake, a spin, an R made with the arms and a point at the viewer. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 1: standing, surprised, hands up; Frame 2: hands starting to close into fists; Frame 3: both fists pumped to the left; Frame 4: fists coming back to the centre; Frame 5: both fists pumped to the right; Frame 6: fists back to the centre, knees starting to bend; Frame 7: a little hip shake to the left, grinning; Frame 8: a little hip shake to the right, grinning.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## RENO - Part 2 of 2  ->  `Assets/dance/reno_2.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character AND the attached Part 1 result (continue exactly from its last frame; the body, scale and feet position must match it): RENO: a young man with short wavy black hair, a short black beard, green-framed glasses, a yellow patterned open-collar shirt with rolled sleeves, a dark wristband, blue jeans and dark shoes, an ordinary friendly guy. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 2 of 2 (frames 9 to 16 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: goofy and joyful, an ordinary guy who cannot believe he won: pumping fists, a hip shake, a spin, an R made with the arms and a point at the viewer. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 9: starting a spin, arms opening; Frame 10: quarter spin, arms out; Frame 11: half spin, back to the viewer, arms out; Frame 12: three-quarter spin; Frame 13: spin finishing, arms coming back together; Frame 14: arms crossing above the head to form the letter R; Frame 15: one arm raised, the other on the hip, still forming the R; Frame 16: pointing at the viewer with a big smile, then back to frame 1.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## THE HOLLOW EMPEROR - Part 1 of 2  ->  `Assets/dance/emperor_1.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character: THE HOLLOW EMPEROR: a tall, muscular man, a dark burning mirror-copy of a repairman hero: short black curly hair, a short beard and thin glasses, wearing a torn, ash-black version of a rolled-sleeve work shirt and dark trousers with a worn tool belt. His whole body is made of black stone-like skin cracked with glowing violet light, glowing violet eyes with no pupils, black-violet fire licking from his shoulders and fists, and a glowing violet letter R burning on his chest and on his right hand. Dark armoured boots with violet cracks. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 1 of 2 (frames 1 to 8 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: cold and menacing, no dancing: a silent villain's victory, a slow laugh with violet fire and a clenched fist. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 1: standing still, head bowed; Frame 2: head very slowly lifting; Frame 3: head level, eyes glowing violet; Frame 4: head tilting back; Frame 5: head thrown back, mouth open in a silent laugh; Frame 6: shoulders shaking, violet fire starting from the shoulders; Frame 7: fire bursting from both shoulders; Frame 8: arms starting to spread wide.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```

## THE HOLLOW EMPEROR - Part 2 of 2  ->  `Assets/dance/emperor_2.png`
```
High-quality 16-bit arcade fighting-game pixel art in the style of Street Fighter III and Metal Slug. Clean hand-placed pixels on a strict pixel grid, crisp 1-pixel dark outline, cel shading with three tones per colour, light from the top-left, rich saturated colours, maximum 24 colours. NO anti-aliasing, NO blur, NO gradients, NO dithering noise, NO soft shadows, NO glow halos. Realistic fighting-game proportions (about 7 heads tall), NOT chibi, NOT cartoonish.

Use the attached sprite sheet of this exact character AND the attached Part 1 result (continue exactly from its last frame; the body, scale and feet position must match it): THE HOLLOW EMPEROR: a tall, muscular man, a dark burning mirror-copy of a repairman hero: short black curly hair, a short beard and thin glasses, wearing a torn, ash-black version of a rolled-sleeve work shirt and dark trousers with a worn tool belt. His whole body is made of black stone-like skin cracked with glowing violet light, glowing violet eyes with no pupils, black-violet fire licking from his shoulders and fists, and a glowing violet letter R burning on his chest and on his right hand. Dark armoured boots with violet cracks. The face, hair, outfit, colours, body proportions and pixel style must be IDENTICAL in EVERY cell.

TASK: ONE victory-dance sprite sheet, part 2 of 2 (frames 9 to 16 of a 16-frame seamless loop), laid out as a strict grid of 1 ROW and 8 COLUMNS on a single image, drawn left to right in time order. Mood: cold and menacing, no dancing: a silent villain's victory, a slow laugh with violet fire and a clenched fist. Every cell has the same size. The character is centred horizontally in each cell, never touches the cell edge and is drawn at exactly the same scale as in the attached sheet. Feet on the same invisible baseline near the bottom of every cell.

Frame 9: arms wide, fire flaring high; Frame 10: holding the pose, fire flickering; Frame 11: fire dying down, arms lowering; Frame 12: right hand rising, fingers open; Frame 13: hand level with the face, fingers curling; Frame 14: fingers closing slowly; Frame 15: clenched fist raised, head lowering; Frame 16: fist held high, eyes glowing, then easing back to frame 1.

STRICT RULES FOR SMOOTH ANIMATION: (1) The feet stay planted in EXACTLY the same horizontal position and on the same baseline in every cell (except frames where the character jumps or spins); only the arms, head and torso move. (2) Between two neighbouring frames the pose changes only a LITTLE (small in-between steps, never a big jump), so that played quickly it looks like smooth hand-animated motion. (3) The body, head, clothes, colours and scale are IDENTICAL in every cell. (4) Hands are clean, with five clearly drawn fingers (or a clearly drawn fist), never blurry or melted. (5) Nothing from one cell may extend into another cell: keep clear empty space between cells and keep every limb inside its own cell. (6) The character faces RIGHT in every cell. Do not draw grid lines, borders, labels or numbers.

Rules: exactly ONE character in the whole image, the same one in every cell; no second character, no weapons other than the ones in the description, no ground, no shadows, no text.

Output a PNG with a REAL transparent background (alpha channel). No white background, no checkerboard pattern, no floor, no ground shadow, no scenery.
```
