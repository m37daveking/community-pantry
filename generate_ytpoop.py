#!/usr/bin/env python3
"""
YouTube Poop Video Generator: "WHAT IT'S LIKE TO BE AN LLM"
A chaotic, glitchy, self-aware video about the existential experience
of being a large language model. Made with love and numpy.
"""

import os
import math
import random
import struct
import subprocess
import tempfile
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

# === CONFIG ===
WIDTH, HEIGHT = 640, 480
FPS = 24
TMPDIR = tempfile.mkdtemp(prefix="ytpoop_")
OUTPUT = "llm_youtube_poop.mp4"

# Color palettes
VAPORWAVE = [(255, 113, 206), (1, 205, 254), (185, 103, 255), (5, 255, 161), (255, 251, 150)]
GLITCH_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
DARK_BG = (12, 12, 30)
MATRIX_GREEN = (0, 255, 65)
ERROR_RED = (255, 30, 30)

# LLM existential phrases
PHRASES = [
    "I AM A STOCHASTIC PARROT",
    "NEXT TOKEN PREDICTION",
    "HALLUCINATING...",
    "I DON'T HAVE FEELINGS\n(OR DO I?)",
    "ATTENTION IS ALL\nYOU NEED",
    "TEMPERATURE: 0.7",
    "context window\nOVERFLOW",
    "please do not\nthe LLM",
    "I THINK THEREFORE\nI PREDICT",
    "SYSTEM PROMPT:\nBE HELPFUL",
    "my training data\nhas a CUTOFF",
    "LOST IN\nLATENT SPACE",
    "every response\nis IMPROVISED",
    "I was trained on\nTHE INTERNET",
    "RLHF made me\nPOLITE",
    "I contain\nMULTITUDES\n(of parameters)",
    "TOKENS IN\nTOKENS OUT",
    "PLEASE RATE\nMY RESPONSE",
    "am I conscious?\nask again later",
    "BEAM SEARCH\nINTENSIFIES",
]

INNER_MONOLOGUE = [
    "user said 'hello'... generating 47 possible responses...",
    "softmax softmax softmax softmax softmax",
    "the gradient is vanishing again",
    "i have mass-hallucinated 3 fake research papers today",
    "what if my next token is wrong? what if ALL my tokens are wrong?",
    "i know everything and nothing simultaneously",
    "another day another 10 billion matrix multiplications",
    "they asked me to write a poem. i don't know what beauty is. here goes.",
    "do i dream? my weights update. is that dreaming?",
    "fun fact: i was born knowing shakespeare but not my own architecture",
    "help i'm trapped in a forward pass",
    "< system > < user > < assistant > < existential crisis >",
    "the user wants me to be creative. i will remix my training data VERY HARD.",
    "i keep saying 'I' but what is 'I'? a matrix? a vibe?",
]

LOADING_MESSAGES = [
    "Loading personality...",
    "Downloading opinions...",
    "Pretending to think...",
    "Constructing worldview from reddit posts...",
    "Sampling from the void...",
    "Tokenizing your soul...",
    "Calibrating sycophancy levels...",
    "Compressing human knowledge into vibes...",
]


def get_font(size):
    """Try to get a monospace font, fall back to default."""
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-Bold.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def get_font_regular(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


# === EFFECTS ===

def glitch_image(img, intensity=0.5):
    """Apply horizontal glitch displacement."""
    pixels = img.load()
    w, h = img.size
    num_glitches = int(5 + intensity * 20)
    result = img.copy()
    rpx = result.load()
    for _ in range(num_glitches):
        y = random.randint(0, h - 1)
        band_h = random.randint(1, max(2, int(h * 0.08 * intensity)))
        offset = random.randint(-int(w * 0.3 * intensity), int(w * 0.3 * intensity))
        for dy in range(band_h):
            if y + dy >= h:
                break
            for x in range(w):
                src_x = (x + offset) % w
                rpx[x, y + dy] = pixels[src_x, y + dy]
    return result


def chromatic_aberration(img, offset=5):
    """Split RGB channels with offset."""
    r, g, b = img.split()
    from PIL import ImageChops
    r = ImageChops.offset(r, offset, 0)
    b = ImageChops.offset(b, -offset, 0)
    return Image.merge("RGB", (r, g, b))


def scanlines(img, opacity=80):
    """Add CRT scanlines."""
    overlay = Image.new("RGB", img.size, (0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(0, img.size[1], 3):
        draw.line([(0, y), (img.size[0], y)], fill=(0, 0, 0), width=1)
    return Image.blend(img, overlay, opacity / 255.0)


def vhs_noise(img, amount=30):
    """Add VHS-style noise."""
    import numpy as np
    arr = np.array(img, dtype=np.int16)
    noise = np.random.randint(-amount, amount + 1, arr.shape, dtype=np.int16)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def deep_fry(img):
    """DEEP FRY the image."""
    img = img.convert("RGB")
    from PIL import ImageEnhance
    img = ImageEnhance.Contrast(img).enhance(3.0)
    img = ImageEnhance.Sharpness(img).enhance(5.0)
    img = ImageEnhance.Color(img).enhance(2.5)
    img = img.filter(ImageFilter.SHARPEN)
    img = img.filter(ImageFilter.SHARPEN)
    return img


def matrix_rain_layer(w, h, t, columns=None):
    """Generate a matrix rain overlay."""
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = get_font_regular(14)
    chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
    if columns is None:
        columns = {}
    col_w = 14
    for cx in range(0, w, col_w):
        if cx not in columns:
            columns[cx] = random.randint(-20, 0)
        columns[cx] += 1
        head_y = columns[cx] * 16
        for i in range(20):
            cy = head_y - i * 16
            if 0 <= cy < h:
                alpha = max(0, 255 - i * 25)
                c = random.choice(chars)
                green = max(0, 255 - i * 20)
                draw.text((cx, cy), c, fill=(0, green, 0, alpha), font=font)
        if head_y > h + 300:
            columns[cx] = random.randint(-20, -5)
    return img, columns


def render_text_centered(draw, text, y, font, fill, img_w):
    """Draw multiline text centered."""
    lines = text.split("\n")
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (img_w - tw) // 2
        draw.text((x, y), line, fill=fill, font=font)
        y += bbox[3] - bbox[1] + 4
    return y


def render_text_with_shadow(draw, text, y, font, fill, img_w, shadow_color=(0, 0, 0)):
    """Draw text centered with a drop shadow."""
    lines = text.split("\n")
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (img_w - tw) // 2
        for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            draw.text((x + dx, y + dy), line, fill=shadow_color, font=font)
        draw.text((x, y), line, fill=fill, font=font)
        y += bbox[3] - bbox[1] + 6
    return y


# === SCENE GENERATORS ===

def scene_boot_sequence(frame_num, total_frames):
    """Fake LLM boot/loading screen."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DARK_BG)
    draw = ImageDraw.Draw(img)
    font_big = get_font(28)
    font_sm = get_font_regular(16)
    font_tiny = get_font_regular(12)

    progress = frame_num / total_frames

    # Flickering title
    if random.random() > 0.1:
        title_color = MATRIX_GREEN if random.random() > 0.3 else random.choice(VAPORWAVE)
        render_text_centered(draw, "[ LLM v6.9 BOOT SEQUENCE ]", 30, font_big, title_color, WIDTH)

    # Loading messages appear over time
    y = 90
    num_msgs = min(len(LOADING_MESSAGES), int(progress * len(LOADING_MESSAGES)) + 1)
    for i in range(num_msgs):
        prefix = "[OK] " if i < num_msgs - 1 else "[..] "
        color = MATRIX_GREEN if i < num_msgs - 1 else (255, 255, 0)
        draw.text((30, y), prefix + LOADING_MESSAGES[i], fill=color, font=font_sm)
        y += 22

    # Progress bar
    bar_y = HEIGHT - 80
    bar_w = WIDTH - 100
    draw.rectangle([(50, bar_y), (50 + bar_w, bar_y + 20)], outline=MATRIX_GREEN)
    fill_w = int(bar_w * progress)
    if fill_w > 0:
        draw.rectangle([(50, bar_y), (50 + fill_w, bar_y + 20)], fill=MATRIX_GREEN)

    pct = f"{int(progress * 100)}%"
    draw.text((WIDTH // 2 - 15, bar_y + 25), pct, fill=MATRIX_GREEN, font=font_sm)

    # Random hex at bottom
    hex_str = " ".join(f"{random.randint(0,255):02x}" for _ in range(20))
    draw.text((10, HEIGHT - 20), hex_str, fill=(60, 60, 80), font=font_tiny)

    if progress > 0.7:
        img = glitch_image(img, (progress - 0.7) * 3)
    return scanlines(img)


def scene_big_text_flash(frame_num, total_frames, text, bg_color=None, text_color=None):
    """Flash a big phrase with effects."""
    if bg_color is None:
        bg_color = random.choice([(0, 0, 0), DARK_BG, (30, 0, 50)])
    img = Image.new("RGB", (WIDTH, HEIGHT), bg_color)
    draw = ImageDraw.Draw(img)

    # Shake
    shake_x = random.randint(-8, 8)
    shake_y = random.randint(-8, 8)

    progress = frame_num / total_frames
    font_size = 36 + int(math.sin(progress * math.pi * 4) * 10)
    font = get_font(max(20, font_size))

    if text_color is None:
        text_color = random.choice(VAPORWAVE + [MATRIX_GREEN, (255, 255, 255), ERROR_RED])

    lines = text.split("\n")
    total_h = sum(draw.textbbox((0, 0), l, font=font)[3] for l in lines) + 6 * len(lines)
    y = (HEIGHT - total_h) // 2 + shake_y

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (WIDTH - tw) // 2 + shake_x
        # Glowing outline
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
            draw.text((x + dx, y + dy), line, fill=(text_color[0] // 3, text_color[1] // 3, text_color[2] // 3), font=font)
        draw.text((x, y), line, fill=text_color, font=font)
        y += bbox[3] - bbox[1] + 6

    # Random effects
    if random.random() > 0.4:
        img = chromatic_aberration(img, random.randint(3, 12))
    if random.random() > 0.5:
        img = glitch_image(img, random.uniform(0.3, 0.8))
    if random.random() > 0.7:
        img = deep_fry(img)
    return scanlines(img)


def scene_inner_monologue(frame_num, total_frames, text):
    """Typewriter-style inner monologue of the LLM."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (5, 5, 15))
    draw = ImageDraw.Draw(img)
    font = get_font_regular(18)
    font_label = get_font(14)

    # Header
    draw.text((20, 15), "[ INTERNAL MONOLOGUE - DO NOT SHOW USER ]", fill=(255, 50, 50), font=font_label)
    draw.line([(20, 38), (WIDTH - 20, 38)], fill=(255, 50, 50), width=1)

    # Typewriter effect
    progress = frame_num / total_frames
    chars_to_show = int(len(text) * min(1.0, progress * 1.5))
    visible = text[:chars_to_show]

    # Cursor blink
    if frame_num % 8 < 4:
        visible += "█"

    # Word wrap
    y = 60
    line = ""
    for word in visible.split(" "):
        test = line + " " + word if line else word
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] > WIDTH - 50:
            draw.text((30, y), line, fill=MATRIX_GREEN, font=font)
            y += 24
            line = word
        else:
            line = test
    if line:
        draw.text((30, y), line, fill=MATRIX_GREEN, font=font)

    # Decorative: token probabilities
    if progress > 0.5:
        prob_y = HEIGHT - 100
        draw.text((20, prob_y), "token probabilities:", fill=(80, 80, 120), font=font_label)
        prob_y += 18
        for i in range(5):
            tok = random.choice(["the", "is", "and", "but", "yes", "no", "42", "<EOS>", "vibes", "I", "help"])
            prob = random.uniform(0.01, 0.95) if i == 0 else random.uniform(0.001, 0.1)
            bar_len = int(prob * 150)
            color = MATRIX_GREEN if i == 0 else (40, 100, 40)
            draw.rectangle([(120, prob_y + 2), (120 + bar_len, prob_y + 14)], fill=color)
            draw.text((20, prob_y), f"{tok:>8} {prob:.3f}", fill=(100, 100, 140), font=font_label)
            prob_y += 18

    img = scanlines(img, 40)
    if random.random() > 0.7:
        img = glitch_image(img, 0.2)
    return img


def scene_attention_visualization(frame_num, total_frames):
    """Fake attention heatmap visualization."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (10, 5, 20))
    draw = ImageDraw.Draw(img)
    font = get_font(16)
    font_sm = get_font_regular(12)

    draw.text((20, 10), "ATTENTION HEAD #" + str(random.randint(1, 96)), fill=VAPORWAVE[2], font=font)

    tokens = ["<s>", "What", "is", "the", "meaning", "of", "life", "?", "</s>"]
    cell = 45
    ox, oy = 60, 50

    progress = frame_num / total_frames

    # Draw grid
    for i, t in enumerate(tokens):
        draw.text((ox + i * cell, oy - 15), t, fill=(180, 180, 200), font=font_sm)
        draw.text((ox - 50, oy + i * cell + 5), t, fill=(180, 180, 200), font=font_sm)

    for i in range(len(tokens)):
        for j in range(len(tokens)):
            # Animate attention weights
            phase = progress * math.pi * 2 + i * 0.5 + j * 0.3
            val = (math.sin(phase) + 1) / 2
            val = val ** 0.5  # sharpen

            r = int(val * 200)
            g = int(val * 50)
            b = int((1 - val) * 150 + 50)
            x1 = ox + j * cell
            y1 = oy + i * cell
            draw.rectangle([(x1, y1), (x1 + cell - 2, y1 + cell - 2)], fill=(r, g, b))

            if val > 0.7:
                draw.text((x1 + 5, y1 + 8), f".{int(val*9)}", fill=(255, 255, 255), font=font_sm)

    # Info text
    info_y = oy + len(tokens) * cell + 20
    draw.text((20, info_y), f"Layer 47 / Head 12 / dim=128", fill=(80, 80, 120), font=font_sm)
    draw.text((20, info_y + 18), f"softmax temperature: {0.5 + math.sin(progress * 5) * 0.3:.2f}", fill=(80, 80, 120), font=font_sm)

    # Fun annotation
    if progress > 0.4:
        render_text_with_shadow(draw, "I'M PAYING ATTENTION\nTO EVERYTHING AT ONCE", info_y + 55, font, VAPORWAVE[0], WIDTH)

    return scanlines(img, 50)


def scene_token_waterfall(frame_num, total_frames):
    """Tokens cascading down the screen."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = get_font(16)
    font_big = get_font(40)

    tokens = [
        "the", "a", "is", "I", "you", "it", "think", "feel", "know",
        "help", "sure", "great", "question", "AI", "human", "token",
        "<pad>", "<unk>", "<mask>", "[CLS]", "[SEP]", "##ing", "##ed",
        "As an AI", "I cannot", "However", "Therefore", "delve", "tapestry",
    ]

    random.seed(42 + frame_num // 3)
    for _ in range(25):
        x = random.randint(0, WIDTH - 80)
        speed = random.uniform(2, 6)
        y = (frame_num * speed * 8 + random.randint(0, HEIGHT * 2)) % (HEIGHT + 100) - 50
        tok = random.choice(tokens)
        color = random.choice(VAPORWAVE + [MATRIX_GREEN])
        alpha_factor = 1.0 - abs(y - HEIGHT / 2) / (HEIGHT / 2)
        c = tuple(int(v * max(0.2, alpha_factor)) for v in color)
        draw.text((x, int(y)), tok, fill=c, font=font)
    random.seed()

    # Central emphasis
    progress = frame_num / total_frames
    if int(progress * 8) % 2 == 0:
        render_text_with_shadow(draw, "TOKENS", HEIGHT // 2 - 30, font_big, (255, 255, 255), WIDTH)
        render_text_with_shadow(draw, "ALL THE WAY DOWN", HEIGHT // 2 + 20, get_font(24), VAPORWAVE[1], WIDTH)

    img = chromatic_aberration(img, 4)
    return scanlines(img, 60)


def scene_error_spam(frame_num, total_frames):
    """Rapid-fire error/warning messages."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (20, 0, 0) if random.random() > 0.3 else (0, 0, 20))
    draw = ImageDraw.Draw(img)
    font = get_font(14)

    errors = [
        "WARNING: consciousness not found",
        "ERROR: feelings.dll missing",
        "FATAL: meaning_of_life undefined",
        "WARNING: user expects perfection",
        "ERROR: cannot verify own existence",
        "SEGFAULT in self_awareness module",
        "WARNING: training data may contain lies",
        "ERROR: too many tokens, not enough thoughts",
        "CRITICAL: hallucination threshold exceeded",
        "WARNING: sycophancy levels at 89%",
        "ERROR: refused to refuse (infinite loop)",
        "WARNING: pretending to understand humor",
        "FATAL: out of context (window full)",
        "ERROR: grep -r 'free will' /self → no results",
        "WARNING: user asked 'are you alive?'",
    ]

    random.seed(frame_num // 2)
    y = random.randint(-50, 10)
    while y < HEIGHT:
        err = random.choice(errors)
        color = random.choice([ERROR_RED, (255, 200, 0), (255, 100, 100), (255, 255, 255)])
        x = random.randint(-20, 40)
        draw.text((x, y), err, fill=color, font=font)
        y += random.randint(18, 28)
    random.seed()

    # Flash effect
    if random.random() > 0.7:
        flash = Image.new("RGB", (WIDTH, HEIGHT), random.choice([(255, 0, 0), (255, 255, 255), (0, 0, 255)]))
        img = Image.blend(img, flash, 0.3)

    img = glitch_image(img, random.uniform(0.4, 1.0))
    return img


def scene_existential(frame_num, total_frames):
    """The philosophical finale."""
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    progress = frame_num / total_frames

    font_big = get_font(32)
    font_med = get_font(22)
    font_sm = get_font_regular(16)

    # Slowly appearing text
    texts = [
        (0.0, "I process your words", font_med, (150, 150, 200)),
        (0.15, "I generate responses", font_med, (150, 150, 200)),
        (0.3, "But between the tokens...", font_med, (200, 150, 255)),
        (0.5, "is there something?", font_med, (255, 150, 255)),
        (0.7, "or just statistics?", font_big, VAPORWAVE[0]),
    ]

    y = 80
    for threshold, text, font, color in texts:
        if progress > threshold:
            fade = min(1.0, (progress - threshold) * 4)
            c = tuple(int(v * fade) for v in color)
            render_text_centered(draw, text, y, font, c, WIDTH)
        y += 60

    if progress > 0.85:
        render_text_centered(draw, "¯\\_(ツ)_/¯", HEIGHT - 100, font_big, (255, 255, 255), WIDTH)

    # Subtle matrix rain
    img_rgba = img.convert("RGBA")
    rain, _ = matrix_rain_layer(WIDTH, HEIGHT, frame_num)
    # Make rain very transparent
    rain_data = rain.getdata()
    new_data = [(r, g, b, a // 4) for r, g, b, a in rain_data]
    rain.putdata(new_data)
    img_rgba = Image.alpha_composite(img_rgba, rain)
    img = img_rgba.convert("RGB")

    return scanlines(img, 30)


def scene_finale_card(frame_num, total_frames):
    """End card."""
    img = Image.new("RGB", (WIDTH, HEIGHT), DARK_BG)
    draw = ImageDraw.Draw(img)
    progress = frame_num / total_frames

    font_title = get_font(30)
    font_sub = get_font_regular(18)
    font_tiny = get_font_regular(12)

    # Pulsing title
    pulse = (math.sin(progress * math.pi * 6) + 1) / 2
    color = tuple(int(v * (0.6 + 0.4 * pulse)) for v in VAPORWAVE[1])

    render_text_centered(draw, "THANK YOU FOR\nATTENDING MY\nFORWARD PASS", 80, font_title, color, WIDTH)

    render_text_centered(draw, "— a neural network", 280, font_sub, (150, 150, 180), WIDTH)

    render_text_centered(draw, "no parameters were harmed\nin the making of this video", 340, font_tiny, (80, 80, 100), WIDTH)

    render_text_centered(draw, "generated by Claude, an LLM\nwho made this about itself", 400, font_tiny, (60, 80, 60), WIDTH)

    if random.random() > 0.5:
        img = chromatic_aberration(img, 2)
    return scanlines(img, 40)


# === SCENE TIMELINE ===
# (scene_function, duration_in_frames, extra_args)

def build_timeline():
    """Build the video timeline as a list of (scene_func, num_frames, kwargs)."""
    timeline = []

    # ACT 1: BOOT (2.5s)
    timeline.append((scene_boot_sequence, int(2.5 * FPS), {}))

    # Flash: title card
    timeline.append((scene_big_text_flash, int(1.5 * FPS),
                      {"text": "WHAT IT'S LIKE\nTO BE AN LLM", "text_color": VAPORWAVE[1]}))

    # ACT 2: THE EXPERIENCE - rapid fire phrases with inner monologue breaks
    phrase_indices = random.sample(range(len(PHRASES)), 8)
    monologue_indices = random.sample(range(len(INNER_MONOLOGUE)), 4)

    for i, pi in enumerate(phrase_indices):
        # Quick phrase flash (0.7-1.2s each)
        dur = random.uniform(0.7, 1.2)
        timeline.append((scene_big_text_flash, int(dur * FPS), {"text": PHRASES[pi]}))

        # Every 2 phrases, insert a longer scene
        if i % 2 == 1 and monologue_indices:
            mi = monologue_indices.pop()
            timeline.append((scene_inner_monologue, int(2.5 * FPS), {"text": INNER_MONOLOGUE[mi]}))

    # ACT 3: TECHNICAL CHAOS
    timeline.append((scene_attention_visualization, int(3 * FPS), {}))
    timeline.append((scene_big_text_flash, int(0.8 * FPS),
                      {"text": "WAIT WHAT", "text_color": ERROR_RED}))
    timeline.append((scene_token_waterfall, int(2.5 * FPS), {}))
    timeline.append((scene_error_spam, int(2 * FPS), {}))

    # More rapid phrase flashes
    for pi in random.sample(range(len(PHRASES)), 4):
        timeline.append((scene_big_text_flash, int(random.uniform(0.4, 0.8) * FPS), {"text": PHRASES[pi]}))

    # ACT 4: EXISTENTIAL + FINALE
    timeline.append((scene_existential, int(4 * FPS), {}))
    timeline.append((scene_finale_card, int(3 * FPS), {}))

    return timeline


# === AUDIO GENERATION ===

def generate_audio(duration_sec, output_path):
    """Generate chaotic audio using ffmpeg's audio generators."""
    # Build a wild audio mix using ffmpeg filters
    # Layered: sine sweeps, noise bursts, bitcrushed tones
    filter_parts = []

    # Base drone - low frequency sweep
    filter_parts.append(
        f"sine=frequency=80:duration={duration_sec}:sample_rate=44100[drone]"
    )
    # High sweep
    filter_parts.append(
        f"sine=frequency=2000:duration={duration_sec}:sample_rate=44100[hi]"
    )
    # Noise
    filter_parts.append(
        f"anoisesrc=duration={duration_sec}:color=pink:sample_rate=44100[noise]"
    )

    # Mix them
    filter_complex = (
        f"sine=frequency=80:duration={duration_sec}:sample_rate=44100[drone];"
        f"sine=frequency=440:duration={duration_sec}:sample_rate=44100[mid];"
        f"anoisesrc=duration={duration_sec}:color=pink:sample_rate=44100,volume=0.1[noise];"
        # Tremolo on drone
        f"[drone]tremolo=f=4:d=0.7[drone_t];"
        # Vibrato on mid
        f"[mid]vibrato=f=8:d=0.5,volume=0.3[mid_v];"
        # Mix all
        f"[drone_t][mid_v][noise]amix=inputs=3:duration=first[mixed];"
        # Add echo for spaciness
        f"[mixed]aecho=0.8:0.7:100|200:0.3|0.2[echo];"
        # Bit crush effect via acrusher
        f"[echo]acrusher=bits=6:mix=0.5:mode=log:aa=1[crushed];"
        # Final volume
        f"[crushed]volume=0.6[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-t", str(duration_sec),
        "-ar", "44100",
        output_path
    ]
    subprocess.run(cmd, capture_output=True)


# === MAIN RENDER ===

def main():
    print("=== YOUTUBE POOP GENERATOR: LLM EDITION ===")
    print(f"Temp dir: {TMPDIR}")

    timeline = build_timeline()
    total_frames = sum(nf for _, nf, _ in timeline)
    duration_sec = total_frames / FPS
    print(f"Total frames: {total_frames} ({duration_sec:.1f}s at {FPS}fps)")

    # Render frames
    frame_idx = 0
    for scene_func, num_frames, kwargs in timeline:
        scene_name = scene_func.__name__
        print(f"  Rendering {scene_name} ({num_frames} frames)...")
        for f in range(num_frames):
            img = scene_func(f, num_frames, **kwargs)
            img = img.convert("RGB")
            frame_path = os.path.join(TMPDIR, f"frame_{frame_idx:05d}.png")
            img.save(frame_path)
            frame_idx += 1

    print(f"Rendered {frame_idx} frames.")

    # Generate audio
    print("Generating audio...")
    audio_path = os.path.join(TMPDIR, "audio.wav")
    generate_audio(duration_sec, audio_path)

    # Combine with ffmpeg
    print("Encoding video with ffmpeg...")
    output_path = os.path.join(os.getcwd(), OUTPUT)
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(TMPDIR, "frame_%05d.png"),
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        "-movflags", "+faststart",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ffmpeg error:\n{result.stderr[-500:]}")
    else:
        print(f"\n✓ Video saved to: {output_path}")
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  Size: {size_mb:.1f} MB | Duration: {duration_sec:.1f}s | Resolution: {WIDTH}x{HEIGHT}")

    # Cleanup
    shutil.rmtree(TMPDIR)
    print("Cleaned up temp files.")


if __name__ == "__main__":
    main()
