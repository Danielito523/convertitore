import tkinter as tk
from tkinter import ttk, messagebox

def converti():
    try:
        valore_input = entry_input.get()
        base_input = combo_input.get()
        base_output = combo_output.get()

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
        elif base_input == "Ottale":
            decimale = int(valore_input, 8)
        elif base_input == "Esadecimale":
            decimale = int(valore_input, 16)
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
        elif base_output == "Ottale":
            risultato = oct(int(decimale))[2:]  
        elif base_output == "Esadecimale":
            risultato = hex(int(decimale))[2:]  
        elif base_output == "Decimale":
            risultato = f"{decimale:.10g}"

        label_output.config(text=f"Risultato: {risultato}", bg="#1e1e1e", fg="#00ff00", font=("Arial", 12, "bold"))

    except ValueError as e:
        messagebox.showerror("Errore", str(e))
    except Exception as e:
        messagebox.showerror("Errore", "Input non valido.")

# Creazione della finestra principale
root = tk.Tk()
root.title("Convertitore di Numeri")
root.geometry("400x300")
root.configure(bg="#2e2e2e")

# Frame principale
main_frame = tk.Frame(root, bg="#3e3e3e")
main_frame.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

# Configurazione delle righe e colonne per il ridimensionamento
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2)  # La seconda colonna (input) avrà più spazio
main_frame.rowconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)
main_frame.rowconfigure(3, weight=1)
main_frame.rowconfigure(4, weight=1)

# Etichette e campi di input
label_input = tk.Label(main_frame, text="Inserisci il numero:", bg="#3e3e3e", fg="#ffffff", font=("Arial", 12))
label_input.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

entry_input = tk.Entry(main_frame, font=("Arial", 12), width=20, bd=0, relief="flat", fg="#000000", bg="#ffffff")
entry_input.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

label_base_input = tk.Label(main_frame, text="Base di input:", bg="#3e3e3e", fg="#ffffff", font=("Arial", 12))
label_base_input.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

combo_input = ttk.Combobox(main_frame, values=["Binario", "Ottale", "Decimale", "Esadecimale"], font=("Arial", 10), state="readonly")
combo_input.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
combo_input.current(0)

label_base_output = tk.Label(main_frame, text="Base di output:", bg="#3e3e3e", fg="#ffffff", font=("Arial", 12))
label_base_output.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

combo_output = ttk.Combobox(main_frame, values=["Binario", "Ottale", "Decimale", "Esadecimale"], font=("Arial", 10), state="readonly")
combo_output.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
combo_output.current(2)  # Imposta Decimale come default

# Pulsante di conversione
button_convert = tk.Button(main_frame, text="Converti", command=converti, font=("Arial", 10, "bold"), bg="#007bff", fg="white", bd=0, relief="flat")
button_convert.grid(row=3, columnspan=2, pady=10)

# Etichetta per il risultato
label_output = tk.Label(main_frame, text="Risultato: ", bg="#3e3e3e", fg="#ffffff", font=("Arial", 12))
label_output.grid(row=4, columnspan=2, pady=10, sticky='ew')

# Avvio dell'app
root.mainloop()
