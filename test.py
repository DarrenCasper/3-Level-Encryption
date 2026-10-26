import random
import string

# -------------------------------------------------------------
# 1. Setup & Key Tables
# -------------------------------------------------------------

# Level 1: Random substitution permutation
alphabet = list(string.ascii_uppercase)
shuffled_alpha = alphabet.copy()
random.shuffle(shuffled_alpha)

L1_ENCRYPT = {alphabet[i]: shuffled_alpha[i] for i in range(26)}
L1_DECRYPT = {v: k for k, v in L1_ENCRYPT.items()}

# Level 2: 6x6 Matrix (A-Z, 0-9)
MATRIX_CHARS = alphabet + [str(d) for d in range(10)]
L2_CHAR_TO_INDEX = {MATRIX_CHARS[i]: i for i in range(36)}
L2_INDEX_TO_CHAR = {i: MATRIX_CHARS[i] for i in range(36)}

# Level 3: 36 Distinct Complex Glyphs (Geometric, Greek, Math)
COMPLEX_GLYPHS = [
    "▲", "▼", "◆", "◇", "○", "●",
    "★", "☆", "♠", "♣", "♥", "♦",
    "←", "↑", "→", "↓", "↔", "↕",
    "§", "¶", "†", "‡", "¤", "¥",
    "α", "β", "γ", "δ", "ε", "θ",
    "λ", "μ", "π", "σ", "φ", "Ω",
]

GLYPH_TO_VAL = {COMPLEX_GLYPHS[i]: i for i in range(36)}
VAL_TO_GLYPH = {i: COMPLEX_GLYPHS[i] for i in range(36)}


# -------------------------------------------------------------
# 2. Encryption Pipeline
# -------------------------------------------------------------

def encrypt_pipeline(plaintext: str, secret_seed: int = 7) -> dict:
    clean_text = "".join([c for c in plaintext.upper() if c.isalnum()])

    # Level 1: Word substitution
    level_1 = "".join([L1_ENCRYPT.get(c, c) for c in clean_text])

    # Level 2 & 3: Matrix indexing + Positional offset -> Single complex glyph
    level_2_coords = []
    level_3_symbols = []

    for idx, char in enumerate(level_1):
        # Base matrix index (0 to 35) and coordinate format (row, col)
        base_val = L2_CHAR_TO_INDEX[char]
        row, col = divmod(base_val, 6)
        level_2_coords.append(f"({row},{col})")

        # Dynamic offset: shift by (index + secret_seed) modulo 36
        offset = (idx + secret_seed) % 36
        shifted_val = (base_val + offset) % 36

        # Convert to complex glyph
        level_3_symbols.append(VAL_TO_GLYPH[shifted_val])

    return {
        "plaintext": clean_text,
        "level_1_word": level_1,
        "level_2_coords": " ".join(level_2_coords),
        "level_3_symbol": "".join(level_3_symbols),
    }


# -------------------------------------------------------------
# 3. Decryption Pipeline
# -------------------------------------------------------------

def decrypt_pipeline(ciphertext: str, secret_seed: int = 7) -> str:
    level_1_chars = []

    # Reverse Level 3 & Level 2
    for idx, symbol in enumerate(ciphertext):
        shifted_val = GLYPH_TO_VAL[symbol]

        # Reverse offset shift
        offset = (idx + secret_seed) % 36
        base_val = (shifted_val - offset) % 36

        # Fetch character from matrix grid
        original_char = L2_INDEX_TO_CHAR[base_val]
        level_1_chars.append(original_char)

    level_1 = "".join(level_1_chars)

    # Reverse Level 1 substitution
    plaintext = "".join([L1_DECRYPT.get(c, c) for c in level_1])
    return plaintext


# -------------------------------------------------------------
# 4. Verification
# -------------------------------------------------------------

if __name__ == "__main__":
    message = "SECRET"
    seed = 11

    encrypted = encrypt_pipeline(message, secret_seed=seed)
    decrypted = decrypt_pipeline(encrypted["level_3_symbol"], secret_seed=seed)

    print("--- Encryption Trace ---")
    print(f"Original Text:       {encrypted['plaintext']}")
    print(f"Level 1 (Scramble):  {encrypted['level_1_word']}")
    print(f"Level 2 (Coords):    {encrypted['level_2_coords']}")
    print(f"Level 3 (Shifted):   {encrypted['level_3_symbol']}")
    print("\n--- Decryption Trace ---")
    print(f"Decrypted Result:    {decrypted}")
    print(f"Integrity Check:     {decrypted == encrypted['plaintext']}")