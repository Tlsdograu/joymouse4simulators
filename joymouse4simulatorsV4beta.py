import threading
import pyvjoy
from pynput import mouse, keyboard
import tkinter as tk
import time
import configparser
from tkinter import messagebox
import webbrowser

# Configurar o joystick virtual
joystick_id = 1  # ID do joystick virtual
joystick = pyvjoy.VJoyDevice(joystick_id)

# Variáveis para armazenar a posição do mouse
mouse_x = 0
mouse_y = 0

# Variável para armazenar o estado da tecla
is_key_pressed = False

# Variáveis para armazenar a resolução do monitor
screen_width = 1920
screen_height = 1080

# Variável para armazenar a tecla selecionada
tecla = "space"

# Carregar configurações do arquivo .ini (se existir)
config = configparser.ConfigParser()
config_file = "config.ini"

if config.read(config_file):
    if config.has_section("Config"):
        if config.has_option("Config", "tecla"):
            tecla = config.get("Config", "tecla")
        if config.has_option("Config", "width"):
            screen_width = int(config.get("Config", "width"))
        if config.has_option("Config", "height"):
            screen_height = int(config.get("Config", "height"))

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

# Variável de controle para sair do loop do controle do joystick
running = True

# Função para fechar a janela
def on_close():
    global running
    running = False
    root.destroy()

    # Parar os listeners do mouse e do teclado
    mouse_listener.stop()
    keyboard_listener.stop()

    # Aguardar o término da thread de controle do joystick
    joystick_thread.join()

    # Encerrar o programa
    root.quit()

# Função principal para o controle do joystick
def control_joystick():
    while running:
        if is_key_pressed:
            # Mapear a posição do mouse para os eixos do joystick
            x_axis = int(mouse_x / screen_width * 32767)  # Mapear de 0 a tela_width para -16384 a 16383
            y_axis = int(mouse_y / screen_height * 32767)  # Mapear de 0 a tela_height para -16384 a 16383

            # Configurar os eixos do joystick virtual
            joystick.set_axis(pyvjoy.HID_USAGE_X, x_axis)  # Define o valor do eixo X
            joystick.set_axis(pyvjoy.HID_USAGE_Y, y_axis)  # Define o valor do eixo Y
        else:
            # Colocar o joystick no centro
            joystick.set_axis(pyvjoy.HID_USAGE_X, 16384)  # Define o valor do eixo X
            joystick.set_axis(pyvjoy.HID_USAGE_Y, 16384)

        time.sleep(0.01)  # Espera 0.01 segundos para evitar que o código consuma muita CPU

# Função para salvar as configurações no arquivo .ini
def save_config():
    config["Config"] = {
        "tecla": tecla,
        "width": str(screen_width),
        "height": str(screen_height)
    }

    with open(config_file, "w") as configfile:
        config.write(configfile)

# Função para atualizar a resolução selecionada
def update_resolution():
    global screen_width, screen_height
    screen_width = int(entry_width.get())
    screen_height = int(entry_height.get())
    save_config()

# Função para iniciar ou parar o controle do joystick
def toggle_joystick_control():
    global is_key_pressed
    is_key_pressed = not is_key_pressed


# Função para salvar configuração
def save_configuration():
    save_config()
    messagebox.showinfo("Salvo", "Configurações salvas com sucesso!")

# Criar a janela principal
root = tk.Tk()
root.title("JoyMouse4simulatorsBeta4")

# Configurar a função on_close como tratamento do evento de fechamento da janela
root.protocol("WM_DELETE_WINDOW", on_close)

# Criar os widgets para seleção da resolução
label_resolution = tk.Label(root, text="Selecione a resolução do seu monitor:")
label_resolution.pack()

frame_resolution = tk.Frame(root)
frame_resolution.pack()

label_width = tk.Label(frame_resolution, text="Largura:")
label_width.pack(side=tk.LEFT)

entry_width = tk.Entry(frame_resolution)
entry_width.pack(side=tk.LEFT)
entry_width.insert(0, str(screen_width))

label_height = tk.Label(frame_resolution, text="Altura:")
label_height.pack(side=tk.LEFT)

entry_height = tk.Entry(frame_resolution)
entry_height.pack(side=tk.LEFT)
entry_height.insert(0, str(screen_height))

btn_update_resolution = tk.Button(root, text="Atualizar Resolução", command=update_resolution)
btn_update_resolution.pack()

# Criar botão para salvar configuração
btn_save_config = tk.Button(root, text="Salvar Configuração", command=save_configuration)
btn_save_config.pack()

# Função para abrir o link do canal no navegador
def open_channel_link():
    webbrowser.open("https://www.youtube.com/channel/UCXdgOwYxeVJgok4exLLtfFg")

# Criar o botão para abrir o link do canal
label_chanel = tk.Button(root, text="Made by Desde o simples ao descomplicado youtube", command=open_channel_link)
label_chanel.pack()

# Escolher a tecla para ativar e desativar o joystick
msg = "Escolha a tecla para ativar e desativar o joystick"
teclas = ['space', 'esc', 'enter', 'tab', 'delete', 'insert', 'home', 'end', 'page_up', 'page_down','caps_lock', 'shift', 'ctrl', 'backspace', 'print_screen', 'scroll_lock', 'num_lock', 'menu', ]
label_tecla = tk.Label(root, text="Tecla selecionada: {}".format(tecla))
label_tecla.pack()

# Função para atualizar a tecla selecionada
def update_tecla(value):
    global tecla
    tecla = value
    label_tecla.config(text="Tecla selecionada: {}".format(tecla))

# Dropdown para selecionar a tecla
dropdown_teclas = tk.OptionMenu(root, tk.StringVar(root, tecla), *teclas, command=update_tecla)
dropdown_teclas.pack()

# Configurar os listeners do mouse e do teclado
with mouse.Listener(on_move=on_move) as mouse_listener:
    with keyboard.Listener(on_press=on_press) as keyboard_listener:

        # Criar uma thread para executar a função principal de controle do joystick
        joystick_thread = threading.Thread(target=control_joystick)
        joystick_thread.start()

        # Iniciar a interface gráfica
        root.mainloop()
