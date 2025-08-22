MORSE_CODE_DIGITS_ONLY = {
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'
}

MORSE_CODE_INTERNATIONAL = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',

    '.': '.-.-.-', ',': '--..--', '?': '..--..', '!': '-.-.--',
    ' ': '',

    **MORSE_CODE_DIGITS_ONLY
}

MORSE_CODE_JAPANESE = {
    'あ': '--.--', 'い': '.-', 'う': '..-', 'え': '-.---', 'お': '.-...',
    'か': '.-..', 'き': '-.-..', 'く': '...-', 'け': '-.--', 'こ': '----',
    'さ': '-.-.-', 'し': '--.-.', 'す': '---.-', 'せ': '.---.', 'そ': '---.',
    'た': '-.', 'ち': '..-.', 'つ': '.--.', 'て': '.-.--', 'と': '..-..',
    'な': '.-.', 'に': '-.-.', 'ぬ': '....', 'ね': '--.-', 'の': '..--',
    'は': '-...', 'ひ': '--..-', 'ふ': '--..', 'へ': '.', 'ほ': '-..',
    'ま': '-..-', 'み': '..-.-', 'む': '-', 'め': '-...-', 'も': '-..-.',
    'や': '.--', 'ゆ': '-..--', 'よ': '--',
    'ら': '...', 'り': '--.', 'る': '-.--.', 'れ': '---', 'ろ': '.-.-',
    'わ': '-.-', 'を': '.---', 'ん': '.-.-.',

    'が': '.-.. ..', 'ぎ': '-.-.. ..', 'ぐ': '...- ..', 'げ': '-.-- ..', 'ご': '---- ..',
    'ざ': '-.-.- ..', 'じ': '--.-. ..', 'ず': '---.- ..', 'ぜ': '.---. ..', 'ぞ': '---. ..',
    'だ': '-. ..', 'ぢ': '..-. ..', 'づ': '.--. ..', 'で': '.-.-- ..', 'ど': '..-.. ..',
    'ば': '-... ..', 'び': '--..- ..', 'ぶ': '--.. ..', 'べ': '. ..', 'ぼ': '-.. ..',
    'ぱ': '-... ..--.', 'ぴ': '--..- ..--.', 'ぷ': '--.. ..--.', 'ぺ': '. ..--.', 'ぽ': '-.. ..--.',
    'ゔ': '..- ..',

    '、': '.-.-.-', 'ー': '.--.-', '？': '..--..', '！': '-.-.--',
    '　': '',

    **MORSE_CODE_DIGITS_ONLY
}

SMALL_TO_LARGE = {
    'ゃ':'や', 'ゅ':'ゆ', 'ょ':'よ',
    'ぁ':'あ', 'ぃ':'い', 'ぅ':'う', 'ぇ':'え', 'ぉ':'お',
    'っ': 'つ', 'ゎ':'わ'
}

def normalize_char(char):
    # カタカナを正規化
    if 'ァ' <= char <= 'ヴ':
        char = chr(ord(char) - ord('ァ') + ord('ぁ'))

    # 小書き文字を正規化
    char = SMALL_TO_LARGE.get(char, char)

    return char



# 入力からモール信号の国際規格, 和文規格を判定する関数（数字のみはdigits_onlyとして判定）
def get_morse_mode(text):
    if all(char in MORSE_CODE_DIGITS_ONLY for char in text):
        return 'digits_only'
    elif all(char.upper() in MORSE_CODE_INTERNATIONAL for char in text):
        return 'international'
    elif all(char in MORSE_CODE_JAPANESE for char in text):
        return 'japanese'
    else:
        raise ValueError('英語と日本語が混在、あるいは未対応文字が含まれています。')

    
def text_to_morse(text):
    normalized_text = ''.join(normalize_char(char) for char in text)
    mode = get_morse_mode(normalized_text)

    if mode == 'international':
        morse_list = [MORSE_CODE_INTERNATIONAL[char.upper()] for char in normalized_text]
    elif mode == 'japanese':
        morse_list = [MORSE_CODE_JAPANESE[char] for char in normalized_text]
    else:
        morse_list = [MORSE_CODE_DIGITS_ONLY[char] for char in normalized_text]

    morse_str = '　'.join(morse_list).replace('.', '・').replace('-', 'ー').replace(' ', '　')
    
    return morse_list, morse_str