import wiringpi as pi
import time
import sys
import oled
from PIL import ImageFont

LED1 = 'YOUR_LED_PIN_HERE'
BUZZER = 'YOUR_BUZZER_PIN_HERE'
pi.wiringPiSetupGpio()
pi.pinMode(LED1,1)
pi.pinMode(BUZZER, 1)

disp, image, draw = oled.oled_setup()

# フォント
line_height = 20
FONT_PATH = 'YOUR_FONT_PATH_HERE'
main_font = ImageFont.truetype(FONT_PATH, 16, encoding = 'unic')
morse_font = ImageFont.truetype(FONT_PATH, 12, encoding = 'unic')

def update_disp(current_char, current_morse):
    draw.text((0, 0), 'Now Outputting:', font = main_font, fill = 255)
    draw.text((0, line_height), current_char, font = main_font, fill = 255)
    draw.text((0, line_height * 2), current_morse, font = morse_font, fill = 255)
    
    disp.image(image)
    disp.show()
    oled.oled_clear(draw)

def morse_output(morse_list, text, unit=0.1):
    '''
    ドット = 1単位
    ダッシュ = 3単位
    符号間隔 = 1単位
    文字間隔 = 3単位
    単語間隔 = 7単位
    '''

    dot_duration = unit # ドットの間隔 1ユニット
    dash_duration = unit*3 # ダッシュの間隔 3ユニット
    signal_space_duration = unit # 1符号の間隔 1ユニット
    morse_code_space_duration = unit*2 # 1文字の間隔 3ユニット（1符号の間隔 + 2ユニット）
    word_space_duration = unit*4 # 単語の間隔 7ユニット（前の1文字の間隔 + 4ユニット）

    try:
        for char_index, morse_code in enumerate(morse_list):
            current_char = text[char_index]
            current_morse = morse_code.replace('.', '・').replace('-', 'ー').replace(' ', '　')
            update_disp(current_char, current_morse)
            
            if morse_code == '': # 空白を単語の終了とみなす
                time.sleep(word_space_duration)
                continue
            

            for sig_index, signal in enumerate(morse_code):
                if signal == '.':
                    pi.digitalWrite(LED1, 1)
                    pi.digitalWrite(BUZZER, 1)
                    time.sleep(dot_duration)
                    pi.digitalWrite(LED1, 0)
                    pi.digitalWrite(BUZZER, 0)
                elif signal == '-':
                    pi.digitalWrite(LED1, 1)
                    pi.digitalWrite(BUZZER, 1)
                    time.sleep(dash_duration)
                    pi.digitalWrite(LED1, 0)
                    pi.digitalWrite(BUZZER, 0)
                elif signal == ' ': # 濁点, 半濁点用の空白処理
                    time.sleep(signal_space_duration)
                    continue
                else:
                    continue
                
                # 最後の文字の場合のみスキップ
                if not (char_index == len(morse_list) - 1 and sig_index == len(morse_code) - 1):
                    time.sleep(signal_space_duration)
            
            # 最後の文字の場合のみスキップ
            if (char_index != len(morse_list) - 1):
                time.sleep(morse_code_space_duration)
    finally:
        # クリーンアップ処理
        oled.oled_clear(draw)
        disp.image(image)
        disp.show()
        pi.digitalWrite(LED1, 0)
        pi.digitalWrite(BUZZER, 0)