import sys
import io

# Re-encode stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Map of homoglyph Unicode characters to their Latin lookalikes
homoglyph_map = {
    'ɵ': 'o',
    'ο': 'o',
    'о': 'o',
    '૦': 'o',
    'ɡ': 'g',
    'ġ': 'g',
    'ģ': 'g',
    'ӏ': 'l',
    'ⅼ': 'l',
    'ا': 'l',
    'е': 'e',
    '℮': 'e',
    'ϲ': 'c',
    'с': 'c',
    'ṁ': 'm',
    'а': 'a',
    'і': 'i',
    '۱': 'i',
    'Ь': 'b',
    'ԁ': 'd',
    
}

def get_homoglyph_reasons(line):
    reasons = []
    for idx, char in enumerate(line):
        if char in homoglyph_map:
            ascii_equiv = homoglyph_map[char]
            reasons.append((char, ascii_equiv, idx))
    return reasons

def detect_homoglyphs_verbose(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            reasons = get_homoglyph_reasons(line)
            if reasons:
                print(f"Line {lineno}: {line} is homoglyph")
                for char, mimic, pos in reasons:
                    print(f"  -> Character '{char}' at position {pos} mimics '{mimic}'")


if __name__ == "__main__":
    detect_homoglyphs_verbose("input.txt")
