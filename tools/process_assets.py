#!/usr/bin/env python3
"""Cuts the AI-generated sprite sheets in Assets/ into clean, aligned game frames in data/.

For every character: slices each sheet into frames (by connected blobs, not a fixed grid), rescales all sheets to one
stance height, aligns feet to a common ground line and writes data/characters/<id>/<anim>/<n>.png + meta.json.
Also processes effects, stages, portraits and the logo.

Run:  .venv/bin/python tools/process_assets.py
"""
import colorsys
import json
import os
import shutil
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SRC = os.path.join(ROOT, "Assets")
OUT = os.path.join(ROOT, "data")
SCREEN_W, SCREEN_H = 1920, 1080

CHARS = {
    "kaito": dict(stance_h=396,
                  loco="Martial Artist Fighting Game Sprite Sheet", attacks="Martial Artist Fighting Sprite Sheet",
                  reactions="16-Bit Martial Artist Knockout Sprite Sheet", extras="Pixel Art Martial Artist Sprite Sheet"),
    "brutus": dict(stance_h=422,
                   loco="Pixel-Art Brawler Sprite Sheet", attacks="Pixel-Artsprüit-Sheet eines muskulösen Kämpfers",
                   reactions="Pixel Fighter Knockdown Sprite Sheet", extras="Brutus Brawler Sprite Sheet", recolor=True),
    "valeria": dict(stance_h=386,
                    loco="Red-Haired Fighter Animation Sprite Sheet",
                    attacks="Anime Fighter Sprite Sheet_ Punches, Kicks and Special Poses",
                    reactions="Pixel-Art Fighter Knockdown Sprite Sheet", extras="Pixel Fighter Knockdown to Victory Sprite Sheet"),
    "rudra": dict(stance_h=402,
                  loco="Indian Fighter Pixel Art Sprite Sheet", attacks="Indian Pixel Fighter Sprite Sheet",
                  reactions="Pixel Fighter Knockdown Sprite Atlas", extras="Pixel Fighter Knockdown to Victory Sprite Sheet copy"),
    "reno": dict(stance_h=396,
                 loco="Pixel Art Fighting Sprite Sheet", attacks="Pixel Fighter Animation Sprite Sheet",
                 reactions="Pixel Art Fighting Game Sprite Sheet", extras="Pixel Art Fighting Game Sprite Sheet-2"),
    "mira": dict(stance_h=406,
                 loco="Silver-Haired Mystic Fighter Sprite Sheet", attacks="Pixel-Art Fighter Animation Sprite Sheet",
                 reactions="Pixel Art Fighter Sprite Sheet", extras="Pixel Fighter Sprite Sheet_ Fall, Rise, Victory"),
}

# sheet kind -> rows (animation name, expected frames, indices that are grounded for the baseline)
ROWS = {
    "loco": [("idle", 6, None), ("walk_forward", 8, None), ("walk_back", 8, None), ("jump", 6, [0, 5])],
    "attacks": [("punch_light", 5, None), ("punch_heavy", 7, None), ("kick", 7, None), ("special", 8, None)],
    "reactions": [("block", 2, None), ("hit", 3, None), ("crouch", 2, None), ("ko", 6, [3, 4, 5])],
    "extras": [("knockdown", 6, [3, 4, 5]), ("getup", 5, None), ("win", 6, None)],
}
# which frame of each sheet is the standing "fighting stance" used to normalise the scale
STANCE_REF = {"loco": ("idle", 0), "attacks": ("punch_light", 0), "reactions": ("hit", -1), "extras": ("getup", 4)}


def load(name):
    return Image.open(os.path.join(SRC, name + ".png")).convert("RGBA")


def recolor_brutus_skin(im, ref_im):
    """The orange skin in some of Brutus' sheets is shifted to the brown of his model sheet."""
    def skin_stats(img):
        a = np.asarray(img).astype(np.float32) / 255.0
        mask = a[..., 3] > 0.9
        rgb = a[..., :3]
        mx, mn = rgb.max(-1), rgb.min(-1)
        v = mx
        s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
        d = np.maximum(mx - mn, 1e-6)
        r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
        h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60.0
        skin = mask & (h > 8) & (h < 36) & (s > 0.4) & (v > 0.3)
        return h, s, v, skin

    h0, s0, v0, k0 = skin_stats(im)
    h1, s1, v1, k1 = skin_stats(ref_im)
    if k0.sum() < 100 or k1.sum() < 100:
        return im
    dh = h1[k1].mean() - h0[k0].mean()
    ks = s1[k1].mean() / s0[k0].mean()
    kv = v1[k1].mean() / v0[k0].mean()
    a = np.asarray(im).astype(np.float32) / 255.0
    out = a.copy()
    ys, xs = np.where(k0)
    for y, x in zip(ys, xs):  # only skin pixels (a few hundred thousand), fine for a one-off tool
        h = (h0[y, x] + dh) % 360
        s = min(1.0, s0[y, x] * ks)
        v = min(1.0, v0[y, x] * kv)
        out[y, x, :3] = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


class Frame:
    """One frame cut from a sheet: its bounding box and the exact pixels that belong to it."""

    def __init__(self, box, owner_mask):
        self.box = box
        self.mask = owner_mask  # boolean array, same size as the sheet


def _split_vertical(owner, label, cut_candidates, window=45):
    """Splits one label into an upper and a lower part at the weakest horizontal line near a grid boundary."""
    ys, xs = np.where(owner == label)
    top, bottom = ys.min(), ys.max()
    for yb in cut_candidates:
        if top + 30 < yb < bottom - 30:
            lo, hi = max(top + 20, yb - window), min(bottom - 20, yb + window)
            proj = [(owner[y] == label).sum() for y in range(lo, hi)]
            cut = lo + int(np.argmin(proj))
            new = owner.max() + 1
            lower = np.zeros_like(owner, dtype=bool)
            lower[cut:] = True
            owner[(owner == label) & lower] = new
            return [label, new]
    return [label]


def _split_horizontal(owner, label):
    ys, xs = np.where(owner == label)
    x0, x1 = xs.min(), xs.max()
    w = x1 - x0 + 1
    cols = np.array([(owner[:, x] == label).sum() for x in range(x0, x1 + 1)], dtype=float)
    lo, hi = int(w * 0.28), int(w * 0.72)
    if hi <= lo:
        return None
    k = lo + int(np.argmin(cols[lo:hi]))
    depth = cols[k] / max(cols.max(), 1)
    return x0 + k, depth


def find_frames(im, expected_rows, expected_counts=None, dilate=2, min_area=2500, join=45):
    """Returns rows (top to bottom) of Frame objects, left to right."""
    alpha = np.asarray(im)[..., 3]
    mask = alpha > 24
    H, W = mask.shape
    cell_h = H / expected_rows
    lab, n = ndimage.label(ndimage.binary_dilation(mask, iterations=dilate))
    owner = np.where(mask, lab, 0).astype(np.int32)
    # small pieces (stray hair, sparks) join the nearest big frame
    sizes = ndimage.sum(mask, lab, index=np.arange(1, n + 1))
    big = {i + 1 for i, sz in enumerate(sizes) if sz >= min_area}
    if not big:
        return []
    keep = np.isin(owner, list(big))
    dist, (iy, ix) = ndimage.distance_transform_edt(~keep, return_indices=True)
    nearest = owner[iy, ix]
    owner = np.where(mask & ~keep & (dist < join), nearest, np.where(keep, owner, 0))
    # split frames that span two grid rows (touching vertically)
    boundaries = [int(cell_h * r) for r in range(1, expected_rows)]
    for label in [l for l in np.unique(owner) if l]:
        ys, _ = np.where(owner == label)
        if ys.max() - ys.min() > cell_h * 1.2:
            _split_vertical(owner, label, boundaries)
    # assign to rows by the frame's vertical centre
    def row_of(label):
        ys, _ = np.where(owner == label)
        return min(expected_rows - 1, int(((ys.min() + ys.max()) / 2) / cell_h))
    rows = [[] for _ in range(expected_rows)]
    for label in [l for l in np.unique(owner) if l]:
        rows[row_of(label)].append(label)

    def xrange_of(label):
        _, xs = np.where(owner == label)
        return xs.min(), xs.max()
    # split frames that are merged horizontally when a row has too few frames
    for r in range(expected_rows):
        want = expected_counts[r] if expected_counts else None
        for _ in range(8):
            if want is None or len(rows[r]) >= want:
                break
            widths = {l: xrange_of(l)[1] - xrange_of(l)[0] + 1 for l in rows[r]}
            # compare to a typical frame of the WHOLE sheet, so a row with only a few frames can still be split
            all_w = [xrange_of(l)[1] - xrange_of(l)[0] + 1 for rr in rows for l in rr]
            med = float(min(np.median(list(widths.values())), np.median(all_w)))
            best = None
            for l, w in widths.items():
                if w > 1.55 * med:
                    res = _split_horizontal(owner, l)
                    if res and res[1] < 0.6 and (best is None or w > best[0]):
                        best = (w, l, res[0])
            if not best:
                break
            _, l, cutx = best
            new = owner.max() + 1
            right = np.zeros_like(owner, dtype=bool)
            right[:, cutx:] = True
            owner[(owner == l) & right] = new
            rows[r].append(new)
            # a cut through touching feet leaves a small detached piece on the wrong side: hand it to the other pose
            for lab_from, lab_to in ((l, new), (new, l)):
                part = owner == lab_from
                cl, ncl = ndimage.label(part)
                if ncl > 1:
                    sizes = ndimage.sum(part, cl, index=np.arange(1, ncl + 1))
                    big = int(np.argmax(sizes)) + 1
                    for k in range(1, ncl + 1):
                        if k != big and sizes[k - 1] < 0.12 * sizes[big - 1]:
                            owner[cl == k] = lab_to
    out = []
    for r in rows:
        frames = []
        for l in r:
            m = owner == l
            ys, xs = np.where(m)
            frames.append(Frame((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1), m))
        out.append(sorted(frames, key=lambda f: f.box[0]))
    return out


def drop_strays(img, gap=14):
    """Removes pieces that are not connected to the main figure (bits of neighbouring poses caught in the crop)."""
    a = np.asarray(img)
    mask = a[..., 3] > 24
    lab, n = ndimage.label(ndimage.binary_dilation(mask, iterations=gap))
    if n <= 1:
        return img
    sizes = ndimage.sum(mask, lab, index=np.arange(1, n + 1))
    keep = lab == (int(np.argmax(sizes)) + 1)
    out = a.copy()
    out[..., 3] = np.where(keep & mask, out[..., 3], 0)
    return Image.fromarray(out, "RGBA")


def scale_img(img, s):
    w, h = img.size
    nw, nh = max(1, round(w * s)), max(1, round(h * s))
    pm = img.convert("RGBa")
    big = pm.resize((w * 4, h * 4), Image.NEAREST)
    return big.resize((nw, nh), Image.BOX).convert("RGBA")


def clean_alpha(img):
    a = np.asarray(img).copy()
    a[..., 3] = np.where(a[..., 3] < 30, 0, a[..., 3])
    return Image.fromarray(a, "RGBA")


def _foot_w(fr):
    """Width (source px) of the widest foot in the lowest 7% of a frame."""
    m = fr.mask[fr.box[1]:fr.box[3], fr.box[0]:fr.box[2]]
    h = m.shape[0]
    band = m[max(0, h - 1 - int(0.07 * h)):]
    cols = band.any(0)
    runs, run = [], 0
    for c in cols:
        if c:
            run += 1
        elif run:
            runs.append(run)
            run = 0
    if run:
        runs.append(run)
    return max(runs) if runs else 0


def row_foot(name, frames):
    """Robust foot size of a row (None for rows where the character is airborne or lying down)."""
    if name in ("ko", "knockdown", "win") or not frames:
        return None
    sel = frames
    if name == "jump":
        sel = [frames[0], frames[-1]]
    elif name == "getup":
        sel = frames[-2:]
    ws = sorted(_foot_w(f) for f in sel)
    ws = [w for w in ws if w >= 0.82 * ws[-1]]      # drop frames where a leg is lifted
    return float(np.median(ws))


def derive_extras(outdir, meta):
    """No extras sheet: knockdown = KO fall, getup = the KO fall played backwards, win = a hands-up pose from idle."""
    A = meta["anims"]
    def copy(src, dst, order):
        os.makedirs(os.path.join(outdir, dst), exist_ok=True)
        lst = []
        for n, i in enumerate(order):
            shutil.copy(os.path.join(outdir, src, f"{i}.png"), os.path.join(outdir, dst, f"{n}.png"))
            lst.append(dict(A[src][i]))
        A[dst] = lst
    n = len(A["ko"])
    copy("ko", "knockdown", list(range(n)))
    copy("ko", "getup", list(range(n - 1, -1, -1)))
    copy("idle", "win", [0, 1, 2, 3, 2, 1])


def process_character(cid, cfg, report):
    outdir = os.path.join(OUT, "characters", cid)
    shutil.rmtree(outdir, ignore_errors=True)
    meta = {"stance_h": cfg["stance_h"], "anims": {}}
    target = cfg["stance_h"]
    ref_extras = load(cfg["extras"]) if cfg.get("extras") else None
    for kind, rows in ROWS.items():
        if cfg.get(kind) is None:
            continue
        im = load(cfg[kind])
        if cfg.get("recolor") and kind != "extras":
            im = recolor_brutus_skin(im, ref_extras)
        found = find_frames(im, len(rows), [r[1] for r in rows])
        if len(found) != len(rows):
            report.append(f"!! {cid}/{kind}: found {len(found)} rows, expected {len(rows)}")
            continue
        # scale from the stance reference frame. The first sheet (movement) is matched by height; every other
        # sheet is matched by body AREA of its stance-like frame, because the sheets were drawn at slightly
        # different sizes and the poses differ, so height alone makes some sheets come out too big.
        rname, ridx = STANCE_REF[kind]
        rrow = [r for r in rows if r[0] == rname][0]
        rrow_frames = found[rows.index(rrow)]
        rfr = rrow_frames[ridx if ridx >= 0 else len(rrow_frames) - 1]
        rbox = rfr.box
        area_src = float(rfr.mask.sum())
        if kind == "loco":
            scale = target / (rbox[3] - rbox[1])
            target_area = area_src * scale * scale
        else:
            scale = (target_area / area_src) ** 0.5
        # per-row scale. The AI drew every row (even in one sheet) at a slightly different size, and the hit/block
        # rows are up to 30% bigger than idle. Foot width is the one thing that stays the same size in every pose and
        # is very stable inside a row, so every row is scaled until its feet match the idle pose's feet.
        feet, areas = {}, {}
        ref_idx = {"punch_light": 0, "punch_heavy": 0, "kick": 0, "special": 0, "block": 0, "hit": -1, "getup": -1,
                   "crouch": None, "idle": 0, "walk_forward": 0, "walk_back": 0, "jump": 0}
        for (rn, _e, _g), rframes in zip(rows, found):
            feet[rn] = row_foot(rn, rframes)
            ri = ref_idx.get(rn)
            if rframes and ri is not None:
                areas[rn] = float(rframes[ri if ri >= 0 else len(rframes) - 1].mask.sum())
        fallback = {"ko": "hit", "knockdown": "getup", "win": "getup", "crouch": "hit"}
        row_scale = {}
        if kind == "loco":
            idle_foot_target = feet["idle"] * scale
        for (rn, _e, _g) in rows:
            key = rn if rn in areas else fallback.get(rn)
            if kind == "loco" and rn == "idle":
                row_scale[rn] = scale
                continue
            by_area = (target_area / areas[key]) ** 0.5 if key in areas else scale
            f = feet.get(rn) or feet.get(fallback.get(rn))
            by_foot = idle_foot_target / f if f else by_area
            # area is reliable for stance-like poses (hit/block/getup rows); attack rows blend in foot width
            row_scale[rn] = by_area ** 0.6 * by_foot ** 0.4 if rn in ("punch_light", "punch_heavy", "kick", "special", "walk_forward", "walk_back", "jump") else by_area
        for (name, expect, grounded), boxes in zip(rows, found):
            scale = row_scale[name]
            if len(boxes) != expect:
                report.append(f"   {cid}/{name}: {len(boxes)} frames (asked {expect})")
            frames = []
            for fr in boxes:
                b = fr.box
                piece = np.asarray(im).copy()
                piece[..., 3] = np.where(fr.mask, piece[..., 3], 0)
                crop = clean_alpha(Image.fromarray(piece, "RGBA").crop(b))
                crop = drop_strays(crop)
                sc = scale_img(crop, scale)
                arr = np.asarray(sc)[..., 3] > 24
                ys, xs = np.where(arr)
                tight = sc.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
                arr = arr[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
                frames.append((tight, arr, b))
            # baseline for the row: median of frame bottoms (in the source sheet) of grounded frames, scaled
            idx = grounded if grounded else list(range(len(frames)))
            idx = [i for i in idx if i < len(frames)]
            bottoms = [boxes[i].box[3] * scale for i in idx]
            baseline = float(np.median(bottoms))
            anim = []
            adir = os.path.join(outdir, name)
            os.makedirs(adir, exist_ok=True)
            for i, (tight, arr, b) in enumerate(frames):
                w, h = tight.size
                aspect = h / w
                if aspect > 0.9 and name not in ("knockdown", "ko"):
                    rows_n = max(2, int(h * 0.12))
                    ys, xs = np.where(arr[-rows_n:])
                    ax = float(xs.mean())
                else:
                    ax = w / 2.0
                bottom = b[3] * scale
                oy = -(h) + (baseline - baseline) + (bottom - baseline) * -1  # top relative to ground
                oy = (bottom - baseline) - h  # y of frame top relative to ground (negative = above ground)
                # tip: right-most opaque pixels (used to size hit boxes)
                xr = arr.shape[1] - 1
                cols = arr[:, max(0, xr - 8): xr + 1]
                ty = np.where(cols.any(1))[0].mean()
                anim.append({"w": w, "h": h, "ox": round(-ax, 1), "oy": round(oy, 1),
                             "tip": [round(xr - ax, 1), round(oy + ty, 1)]})
                tight.save(os.path.join(adir, f"{i}.png"))
            meta["anims"][name] = anim
    if cfg.get("extras") is None:
        derive_extras(outdir, meta)
    with open(os.path.join(outdir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=1)


def process_fx(report):
    outdir = os.path.join(OUT, "fx")
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir)
    meta = {}
    sheets = [
        ("Pixel Art Impact Effects Sprite Sheet", [("hit_spark", "center"), ("block_spark", "center"), ("fireball_orange", "front"), ("fireball_hit_orange", "center")]),
        ("Pixel Art VFX Sprite Sheet", [("dust", "bottom"), ("fireball_red", "front"), ("fireball_crimson", "front"), ("fireball_cyan", "front")]),
        ("Neon Pixel R Energy Sprite Sheet", [("fireball_reno", "front"), ("fireball_hit_reno", "center")]),
    ]
    for sheet, rows in sheets:
        im = load(sheet)
        expected = {"Pixel Art Impact": [6, 5, 4, 6], "Neon Pixel R": [4, 6]}.get(sheet[:16].strip() if False else ("Pixel Art Impact" if sheet.startswith("Pixel Art Impact") else ("Neon Pixel R" if sheet.startswith("Neon Pixel R") else "")), [6, 4, 4, 4])
        alpha = np.asarray(im)[..., 3] > 24
        H = alpha.shape[0]
        proj = alpha.sum(1)
        bounds = [0]
        for r in range(1, len(rows)):
            g = int(H * r / len(rows))
            lo, hi = g - 45, g + 45
            bounds.append(lo + int(np.argmin(proj[lo:hi])))
        bounds.append(H)
        found = []
        for r in range(len(rows)):
            band = im.crop((0, bounds[r], im.size[0], bounds[r + 1]))
            best = None
            for dil in (3, 5, 8, 11, 14, 18, 22, 27, 33, 40):
                cand = find_frames(band, 1, None, dilate=dil, min_area=40, join=60)
                cand = cand[0] if cand else []
                if len(cand) == expected[r]:
                    best = (cand, band)
                    break
                if best is None or abs(len(cand) - expected[r]) < abs(len(best[0]) - expected[r]):
                    best = (cand, band)
            if len(best[0]) != expected[r]:
                # fall back to the 6-column grid the sheet was drawn on
                bm = np.asarray(band)[..., 3] > 24
                Wb = bm.shape[1]
                frames = []
                for k in range(expected[r]):
                    cm = np.zeros_like(bm)
                    cm[:, int(k * Wb / 6):int((k + 1) * Wb / 6)] = bm[:, int(k * Wb / 6):int((k + 1) * Wb / 6)]
                    ys, xs = np.where(cm)
                    if len(ys):
                        frames.append(Frame((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1), cm))
                report.append(f"   fx row {r} of {sheet}: used the column grid ({len(frames)} frames)")
                best = (frames, band)
            found.append(best)
        for (name, anchor), (boxes, band) in zip(rows, found):
            adir = os.path.join(outdir, name)
            os.makedirs(adir)
            lst = []
            for i, fr in enumerate(boxes):
                piece = np.asarray(band).copy()
                piece[..., 3] = np.where(fr.mask, piece[..., 3], 0)
                crop = clean_alpha(Image.fromarray(piece, "RGBA").crop(fr.box))
                w, h = crop.size
                if anchor == "center":
                    ax, ay = w / 2, h / 2
                elif anchor == "front":
                    ax, ay = w - h * 0.5, h / 2
                else:
                    ax, ay = w / 2, h
                crop.save(os.path.join(adir, f"{i}.png"))
                lst.append({"w": w, "h": h, "ox": -ax, "oy": -ay})
            meta[name] = lst
            report.append(f"   fx/{name}: {len(boxes)} frames")
    # explosion variants for other colours by hue rotation of the orange one
    def hue_shift(img, deg):
        hsv = np.asarray(img.convert("RGB").convert("HSV")).copy()
        hsv[..., 0] = (hsv[..., 0].astype(int) + int(deg / 360 * 255)) % 256
        out = Image.fromarray(hsv, "HSV").convert("RGBA")
        out.putalpha(img.getchannel("A"))
        return out
    for color, deg in [("red", -8), ("crimson", -4), ("cyan", 150)]:
        name = f"fireball_hit_{color}"
        os.makedirs(os.path.join(outdir, name))
        lst = []
        for i, fr in enumerate(meta["fireball_hit_orange"]):
            img = Image.open(os.path.join(outdir, "fireball_hit_orange", f"{i}.png"))
            hue_shift(img, deg).save(os.path.join(outdir, name, f"{i}.png"))
            lst.append(dict(fr))
        meta[name] = lst
    json.dump(meta, open(os.path.join(outdir, "meta.json"), "w"), indent=1)


def process_stages_ui(report):
    stages = [("neon", "Rainy Neon Cyberpunk City Stage", "NEON CITY"), ("temple", "Sunset Shrine Courtyard in Pixel Art", "SUNSET SHRINE"),
              ("volcano", "Volcanic Ruins Fighting Arena", "VOLCANIC RUINS")]
    os.makedirs(os.path.join(OUT, "stages"), exist_ok=True)
    for sid, name, _ in stages:
        im = load(name).convert("RGB").resize((SCREEN_W, SCREEN_H), Image.LANCZOS)
        im.save(os.path.join(OUT, "stages", f"{sid}.png"))
    os.makedirs(os.path.join(OUT, "ui"), exist_ok=True)
    for out, name in [("menu_bg", "Ember Dragon Coliseum at Dusk"), ("select_bg", "Fiery Gothic Throne Hall")]:
        load(name).convert("RGB").resize((SCREEN_W, SCREEN_H), Image.LANCZOS).save(os.path.join(OUT, "ui", f"{out}.png"))
    logo = load("Ember Tournament Pixel Logo")
    a = np.asarray(logo)[..., 3] > 24
    ys, xs = np.where(a)
    logo = logo.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    logo.save(os.path.join(OUT, "ui", "logo.png"))
    # portraits: four blobs left to right
    por = load("Four Fierce Pixel Fighters")
    found = find_frames(por, 1, [4])
    boxes = found[0] if found else []
    ids = ["kaito", "brutus", "valeria", "mira"]
    if len(boxes) != 4:
        report.append(f"!! portraits: found {len(boxes)} (expected 4)")
    for cid, fr in zip(ids, boxes):
        piece = np.asarray(por).copy()
        piece[..., 3] = np.where(fr.mask, piece[..., 3], 0)
        clean_alpha(Image.fromarray(piece, "RGBA").crop(fr.box)).save(os.path.join(OUT, "ui", f"portrait_{cid}.png"))
    # single-image portraits (one fighter per file)
    for cid, name in (("rudra", "Pixel Warrior with Red Headband"), ("reno", "Intense Pixel-Art Portrait in Yellow")):
        p = load(name)
        a = np.asarray(p)[..., 3] > 24
        ys, xs = np.where(a)
        p = p.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        side = max(p.size)
        sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        sq.alpha_composite(p, ((side - p.width) // 2, 0))
        sq.save(os.path.join(OUT, "ui", f"portrait_{cid}.png"))
    json.dump({"stages": [{"id": s[0], "name": s[2]} for s in stages]}, open(os.path.join(OUT, "stages", "meta.json"), "w"))


def main():
    report = []
    only = sys.argv[1:]
    if not only or "chars" in only:
        for cid, cfg in CHARS.items():
            print("processing", cid)
            process_character(cid, cfg, report)
    if not only or "fx" in only:
        process_fx(report)
    if not only or "supers" in only:
        process_supers(report)
    if not only or "ui" in only:
        process_stages_ui(report)
    print("\n".join(report) or "all good")




SUPER_SHEETS = {
    "kaito": "16-Bit Dragon Fire Projectile Sprite Sheet", "brutus": "Molten Fist Impact Sprite Sheet",
    "valeria": "Fiery Tornado Sprite Sheet", "mira": "Electric Blue Lightning Sprite Sheet",
    "rudra": "Fiery Tiger Attack Sprite Sheet", "reno": "Neon R Energy Sprite Sheet",
}
AURA_SHEET = "Golden Aura and Shockwave Sprite Sheet"


class _Slice:
    def __init__(self, box, mask):
        self.box, self.mask = box, mask


def _rows_of(im, nrows):
    """First `nrows` rows of a 6-column effect sheet -> [([_Slice]*6, band_image), ...].
    Cuts along the emptiest vertical line near each 1/6 column boundary, so trails and debris cannot merge frames."""
    alpha = np.asarray(im)[..., 3] > 24
    proj = alpha.sum(1)
    rows, start = [], None
    for y, v in enumerate(proj > 3):
        if v and start is None:
            start = y
        elif not v and start is not None:
            if y - start > 25:
                rows.append((start, y))
            start = None
    if start is not None:
        rows.append((start, len(proj)))
    W_ = im.size[0]
    cw = W_ / 6
    out = []
    for (y0, y1) in rows[:nrows]:
        y0, y1 = max(0, y0 - 4), min(im.size[1], y1 + 4)
        band = im.crop((0, y0, W_, y1))
        m = alpha[y0:y1]
        col = m.sum(0).astype(float)
        # 1) natural gaps: runs of empty columns; tiny leftovers are merged into their neighbour
        occupied = col > 0
        segs, st = [], None
        for x, v in enumerate(occupied):
            if v and st is None:
                st = x
            elif not v and st is not None:
                segs.append([st, x])
                st = None
        if st is not None:
            segs.append([st, len(occupied)])
        merged = []
        for sg in segs:
            small = sg[1] - sg[0] < 30
            if merged and (sg[0] - merged[-1][1] < 6 or (small and sg[0] - merged[-1][1] < 90)):
                merged[-1][1] = sg[1]                                 # touching, or a few stray embers: same frame
            elif small:
                continue                                              # a lone speck is not a frame
            else:
                merged.append(sg)
        if 0 < len(merged) < 6:                                       # frames whose trails touch: split by expected width
            span = merged[-1][1] - merged[0][0]
            counts = [max(1, round((sg[1] - sg[0]) / (span / 6))) for sg in merged]
            if sum(counts) == 6:
                split = []
                for sg, n in zip(merged, counts):
                    if n == 1:
                        split.append(sg)
                        continue
                    w_ = (sg[1] - sg[0]) / n
                    edges = [sg[0]]
                    for j in range(1, n):
                        lo, hi = int(sg[0] + j * w_ - 0.3 * w_), int(sg[0] + j * w_ + 0.3 * w_)
                        edges.append(lo + int(np.argmin(col[lo:hi])))
                    edges.append(sg[1])
                    split += [[edges[j], edges[j + 1]] for j in range(n)]
                merged = split
        if len(merged) == 6:
            cuts = [0] + [(merged[i][1] + merged[i + 1][0]) // 2 for i in range(5)] + [W_]
        else:                       # 2) fall back to the emptiest line near each 1/6 boundary
            cuts = [0]
            for k in range(1, 6):
                lo, hi = int(k * cw - 0.3 * cw), int(k * cw + 0.3 * cw)
                cuts.append(lo + int(np.argmin(col[lo:hi])))
            cuts.append(W_)
        frames = []
        for i in range(6):
            sm = np.zeros_like(m)
            sm[:, cuts[i]:cuts[i + 1]] = m[:, cuts[i]:cuts[i + 1]]
            ys, xs = np.where(sm)
            if len(ys):
                frames.append(_Slice((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1), sm))
        out.append((frames, band))
    return out


def _save_anim(outdir, name, frames, band, report):
    adir = os.path.join(outdir, name)
    shutil.rmtree(adir, ignore_errors=True)
    os.makedirs(adir)
    lst = []
    for i, fr in enumerate(frames):
        piece = np.asarray(band).copy()
        piece[..., 3] = np.where(fr.mask, piece[..., 3], 0)
        crop = drop_strays(clean_alpha(Image.fromarray(piece, "RGBA").crop(fr.box)), gap=30)
        arr = np.asarray(crop).copy()
        lab, n = ndimage.label(arr[..., 3] > 24)
        for k, sl in enumerate(ndimage.find_objects(lab), 1):          # thin horizontal rule left over from a neighbouring row
            hh, ww = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
            if hh <= 3 and ww >= 18:
                arr[..., 3][lab == k] = 0
        crop = Image.fromarray(arr, "RGBA")
        bb = crop.getbbox()
        crop = crop.crop(bb) if bb else crop
        crop.save(os.path.join(adir, f"{i}.png"))
        lst.append({"w": crop.width, "h": crop.height, "ox": -crop.width / 2, "oy": -crop.height / 2})
    if len(frames) != 6:
        report.append(f"!! {name}: {len(frames)} frames")
    return lst


def process_supers(report):
    outdir = os.path.join(OUT, "fx")
    meta_path = os.path.join(outdir, "meta.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    for cid, sheet in SUPER_SHEETS.items():
        rows = _rows_of(load(sheet), 2)
        for kind, (frames, band) in zip(("proj", "hit"), rows):
            meta[f"super_{cid}_{kind}"] = _save_anim(outdir, f"super_{cid}_{kind}", frames, band, report)
    rows = _rows_of(load(AURA_SHEET), 2)
    for kind, (frames, band) in zip(("aura", "burst"), rows):
        lst = _save_anim(outdir, f"super_{kind}", frames, band, report)
        if kind == "aura":                       # aura: anchor at the bottom centre so it stands on the floor
            for m in lst:
                m["oy"] = -m["h"]
        meta[f"super_{kind}"] = lst
    json.dump(meta, open(meta_path, "w"), indent=1)
    report.append("   super effects: done")


if __name__ == "__main__":
    main()
