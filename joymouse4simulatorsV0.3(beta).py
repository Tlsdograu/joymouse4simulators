import pyvjoy
from pynput import mouse, keyboard
import time
import easygui
import math

# Configurar o joystick virtual
joystick_id = 1  # ID do joystick virtual
joystick = pyvjoy.VJoyDevice(joystick_id)

# Variáveis para armazenar a posição do mouse
mouse_x = 0
mouse_y = 0

# Variável para armazenar o estado da tecla
is_key_pressed = False

# Função para atualizar a posição do mouse
def on_move(x, y):
    global mouse_x, mouse_y
    mouse_x = x
    mouse_y = y

# Função para atualizar o estado da tecla
def on_press(key):
    global is_key_pressed
    if key == keyboard.Key[tecla]:
        is_key_pressed = not is_key_pressed

# Escolher a tecla para ativar e desativar o joystick
msg = "Escolha a tecla para ativar e desativar o joystick"
teclas = ['space', 'esc', 'enter', 'tab', 'delete', 'insert', 'home', 'end', 'page_up', 'page_down','caps_lock', 'shift', 'ctrl', 'backspace', 'print_screen', 'scroll_lock', 'num_lock', 'menu', ]
tecla = easygui.choicebox(msg, choices=teclas)
print('Feito por/made by: Desde O Simples ao Descomplicado(youtube)\n ------funcionando------\n--------working---------')

# Configurar os listeners do mouse e do teclado
with mouse.Listener(on_move=on_move) as mouse_listener:
    with keyboard.Listener(on_press=on_press) as keyboard_listener:

        # Loop principal do programa
        while True:

            # Se a tecla estiver pressionada
            if is_key_pressed:

                # Mapear a posição do mouse para os eixos do joystick
                x_axis = int(mouse_x / 1920 * 32767)  # Mapear de 0 a tela_width para -16384 a 16383
                y_axis =  int(mouse_y / 1080 * 32767)  # Mapear de 0 a tela_height para -16384 a 16383

                # Configurar os eixos do joystick virtual
                joystick.set_axis(pyvjoy.HID_USAGE_X, x_axis)  # Define o valor do eixo X
                joystick.set_axis(pyvjoy.HID_USAGE_Y, y_axis)  # Define o valor do eixo Y

            # Se a tecla não estiver pressionada
            else:
                # Colocar o joystick no centro
                joystick.set_axis(pyvjoy.HID_USAGE_X, 16384)  # Define o valor do eixo X
                joystick.set_axis(pyvjoy.HID_USAGE_Y, 16384)

            time.sleep(0.01)  # Espera 0.01 segundos para evitar que o código consuma muita CPU

        # Parar os listeners do mouse e do teclado
        mouse_listener.stop()
        keyboard_listener.stop()

