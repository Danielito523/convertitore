import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import sv_ttk


def mostra_schermata_iniziale():
    overlay_canvas = tk.Canvas(root, highlightthickness=0, bg='black')  # Sfondo nero per l'intro
    overlay_canvas.place(relwidth=1, relheight=1)  # Riempi l'intera finestra

    # Carica l'immagine del logo per l'intro
    global logo_img  # Dichiarare logo_img come globale
    logo_path_intro = os.path.join(os.getcwd(), 'logo.png')
    logo_img = Image.open(logo_path_intro)
    logo_img = logo_img.resize((80, 80), Image.Resampling.LANCZOS)  # Ridimensionato a 80x80
    logo_tk = ImageTk.PhotoImage(logo_img)

    center_x = root.winfo_width() // 2
    start_y = root.winfo_height() + 80  # Partenza dal basso

    global logo_item  # Dichiarare logo_item come globale
    logo_item = overlay_canvas.create_image(center_x, start_y, image=logo_tk)
    slide_and_fade_in(overlay_canvas, logo_item, logo_img, 0, 0)

def ease_out_quadratic(t, b, c, d):
    t /= d
    return -c * t * (t - 2) + b

def slide_and_fade_in(canvas, logo_item, logo_img, alpha, step):
    duration = 60
    total_steps = 60

    start_y = root.winfo_height() + 80  # Partenza dal basso
    target_y = (root.winfo_height() // 2) - 39  # Abbassato di un ulteriore 30% (circa 39 pixel)
    change_y = target_y - start_y

    new_y = ease_out_quadratic(step, start_y, change_y, total_steps)
    center_x = root.winfo_width() // 2
    canvas.coords(logo_item, center_x, new_y)

    if alpha < 255:
        alpha = min(alpha + 5, 255)

    logo_img_with_alpha = logo_img.copy()
    logo_img_with_alpha.putalpha(alpha)
    logo_tk_with_alpha = ImageTk.PhotoImage(logo_img_with_alpha)

    canvas.itemconfig(logo_item, image=logo_tk_with_alpha)
    canvas.image = logo_tk_with_alpha

    if step < total_steps:
        canvas.after(15, lambda: slide_and_fade_in(canvas, logo_item, logo_img, alpha, step + 1))
    else:
        canvas.after(300, lambda: mostra_scritte(canvas))  # No need to pass logo_img here

def mostra_scritte(canvas):
    # Aggiunge la scritta "CONVERTER" e "by DANIEL CAON & NAHUEL ROSATI" con fade-in
    text1 = canvas.create_text(root.winfo_width() // 2, (root.winfo_height() // 2) + 40,
                                text="CONVERTER", fill="white", font=("Rubik", 24, "bold"))
    text2 = canvas.create_text(root.winfo_width() // 2, (root.winfo_height() // 2) + 70,
                                text="by DANIEL CAON & NAHUEL ROSATI", fill="white", font=("Rubik", 14))

    fade_in_text(canvas, text1, 0)
    fade_in_text(canvas, text2, 0)

    # Fades out the logo and the text after displaying the text
    canvas.after(2000, lambda: fade_out(canvas, text1, text2, logo_item, 255))  # Pass logo_item to fade_out

def fade_in_text(canvas, text_item, alpha):
    fade_speed = 5

    if alpha < 255:
        alpha = min(alpha + fade_speed, 255)

        canvas.itemconfig(text_item, fill=f"#{alpha:02x}{alpha:02x}{alpha:02x}")  # Fading effect

        canvas.after(30, lambda: fade_in_text(canvas, text_item, alpha))

def fade_out(canvas, text1, text2, logo_item, alpha):  # Added logo_item to parameters
    fade_speed = 5

    if alpha > 0:
        alpha = max(alpha - fade_speed, 0)

        canvas.itemconfig(text1, fill=f"#{alpha:02x}{alpha:02x}{alpha:02x}")  # Fading effect
        canvas.itemconfig(text2, fill=f"#{alpha:02x}{alpha:02x}{alpha:02x}")  # Fading effect

        # Fade out the logo
        logo_alpha = alpha
        logo_img_with_alpha = logo_img.copy()
        logo_img_with_alpha.putalpha(logo_alpha)
        logo_tk_with_alpha = ImageTk.PhotoImage(logo_img_with_alpha)

        canvas.itemconfig(logo_item, image=logo_tk_with_alpha)

        if alpha > 0:
            canvas.after(30, lambda: fade_out(canvas, text1, text2, logo_item, alpha))  # Continue fading out
        else:
            canvas.delete(text1)
            canvas.delete(text2)
            canvas.itemconfig(logo_item, image='')  # Clear the logo image after fading out
            canvas.destroy()

            # Ripristina lo sfondo predefinito
            root.configure(bg='#1c1c1c')

            # Cambia il logo nella finestra principale
            change_logo()

def change_logo():
    # Carica il logo senza sfondo
    logo_path_main = os.path.join(os.getcwd(), 'logonobg.png')
    logo_img_main = Image.open(logo_path_main)
    logo_img_main = logo_img_main.resize((100, 100), Image.Resampling.LANCZOS)  # Ridimensionato a 100x100
    k_main = ImageTk.PhotoImage(logo_img_main)
    logo_label.config(image=k_main)
    logo_label.image = k_main

def converti(event=None):
    try:
        valore_input = entry_input.get("1.0", tk.END).strip()
        base_input = combo_input.get()
        base_output = combo_output.get()

        if not valore_input:
            entry_output.delete("1.0", tk.END)
            return

        # Conversione da binario a decimale
        def binario_a_decimale(binario):
            if ',' in binario:
                parte_intera, parte_frazionaria = binario.split(',')
                decimale = int(parte_intera, 2)
                parte_frazionaria = float('0.' + parte_frazionaria)
                while parte_frazionaria > 0 and len(str(parte_frazionaria)) < 10:
                    parte_frazionaria *= 2
                    decimale += int(parte_frazionaria)
                    parte_frazionaria -= int(parte_frazionaria)
            else:
                decimale = int(binario, 2)
            return decimale

        # Conversione da decimale a binario
        def decimale_a_binario(decimale):
            parte_intera = int(decimale)
            parte_frazionaria = decimale - parte_intera
            
            binario_intero = bin(parte_intera)[2:]
            binario_frazionario = ''
            
            while parte_frazionaria > 0 and len(binario_frazionario) < 10:
                parte_frazionaria *= 2
                if parte_frazionaria >= 1:
                    binario_frazionario += '1'
                    parte_frazionaria -= 1
                else:
                    binario_frazionario += '0'

            return f"{binario_intero}.{binario_frazionario}" if binario_frazionario else binario_intero

        if base_input == "Binario":
            decimale = binario_a_decimale(valore_input)
        elif base_input == "Decimale":
            if ',' in valore_input:
                parte_intera, parte_frazionaria = valore_input.split(',')
                parte_intera = int(parte_intera)
                parte_frazionaria = float('0.' + parte_frazionaria)
            else:
                parte_intera = int(valore_input)
                parte_frazionaria = 0
            
            decimale = parte_intera + parte_frazionaria
        else:
            raise ValueError("Base non valida.")

        if base_output == "Binario":
            risultato = decimale_a_binario(decimale)
        elif base_output == "Decimale":
            risultato = f"{decimale:.10g}"

        entry_output.delete("1.0", tk.END)
        entry_output.insert(tk.END, risultato)

    except ValueError as e:
        messagebox.showerror("Errore", str(e))
    except Exception as e:
        messagebox.showerror("Errore", "Si è verificato un errore imprevisto.")

def inverti():
    input_text = entry_input.get("1.0", tk.END).strip()
    entry_output.delete("1.0", tk.END)
    entry_output.insert(tk.END, input_text)

root = tk.Tk()
root.title("Converter")
root.geometry("600x400")

# Salva il colore di sfondo predefinito
root.default_bg = root.cget('bg')

# Imposta l'icona della finestra
root.iconbitmap('logo.ico')

# Imposta lo sfondo della finestra principale
root.configure(bg=root.default_bg)
# Aggiungi logo (con il logo senza sfondo)
logo_path_main = os.path.join(os.getcwd(), 'logonobg.png')
logo_img_main = Image.open(logo_path_main)
logo_img_main = logo_img_main.resize((100, 100), Image.Resampling.LANCZOS)  # Ridimensionato a 100x100
k_main = ImageTk.PhotoImage(logo_img_main)
logo_label = tk.Label(root, image=k_main)
logo_label.image = k_main
logo_label.pack()

main_frame = tk.Frame(root)
main_frame.pack(pady=20)

# Sezione di input
input_frame = tk.Frame(main_frame)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

label_base_input = tk.Label(input_frame, text="Base di input:", fg='white')
label_base_input.pack(pady=5)

combo_input = ttk.Combobox(input_frame, values=["Binario", "Decimale"], state="readonly")
combo_input.pack(pady=5)
combo_input.current(0)
combo_input.bind("<<ComboboxSelected>>", converti)

entry_input = tk.Text(input_frame, width=20, height=5, bd=1, relief="flat", highlightbackground="#2E2E2E", highlightcolor="#2E2E2E", highlightthickness=1)
entry_input.pack(pady=5)
entry_input.bind("<KeyRelease>", converti)

# Sezione di output
output_frame = tk.Frame(main_frame)
output_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

label_base_output = tk.Label(output_frame, text="Base di output:", fg='white')
label_base_output.pack(pady=5)

combo_output = ttk.Combobox(output_frame, values=["Binario", "Decimale"], state="readonly")
combo_output.pack(pady=5)
combo_output.current(1)
combo_output.bind("<<ComboboxSelected>>", converti)

entry_output = tk.Text(output_frame, width=20, height=5, bd=1, relief="flat", highlightbackground="#2E2E2E", highlightcolor="#2E2E2E", highlightthickness=1)
entry_output.pack(pady=5)

# Function to invert input and output bases and their values
def inverti():
    # Get current values from the combo boxes
    current_input_base = combo_input.get()
    current_output_base = combo_output.get()

    # Swap the bases
    combo_input.set(current_output_base)
    combo_output.set(current_input_base)

    # Get the current input and output text
    input_text = entry_input.get("1.0", tk.END).strip()
    output_text = entry_output.get("1.0", tk.END).strip()

    # Swap the contents of the input and output text boxes
    entry_input.delete("1.0", tk.END)
    entry_output.delete("1.0", tk.END)
    
    entry_input.insert(tk.END, output_text)  # Put output text in input box
    entry_output.insert(tk.END, input_text)   # Put input text in output box

    if output_text:
        converti()

button_invert = tk.Button(main_frame, text="⇄", command=inverti, font=("Arial", 14))
button_invert.grid(row=0, column=1, padx=10, pady=10)

sv_ttk.set_theme("dark")

main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

root.update_idletasks()
mostra_schermata_iniziale()

root.mainloop()
