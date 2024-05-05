import csv
from tkinter import END, Button, Entry, Frame, Label, PanedWindow, PhotoImage, Tk, messagebox, ttk
import pandas as pd
from datetime import date
from google.oauth2.service_account import Credentials
import gspread


def main():
    root.title(f"Affari Tuoi Manager - {today_str}")
    img = PhotoImage(file="amadeus.png")
    root.iconphoto(False, img)
    root.geometry("800x600")

    # Menu bottoni schermate
    paned_buttons = PanedWindow(root, orient="horizontal")

    btn_inserimento = Button(paned_buttons, text="Inserimento📥", command=(lambda: build_panel("ins")))
    btn_inserimento.pack(side="left")
    paned_buttons.add(btn_inserimento)

    btn_classifica = Button(paned_buttons, text="Classifica📊", command=(lambda: build_panel("clas")))
    btn_classifica.pack(side="left")
    paned_buttons.add(btn_classifica)

    btn_impostazioni = Button(paned_buttons, text="Impostazioni⚙️", command=(lambda: build_panel("imp")))
    btn_impostazioni.pack(side="left")
    paned_buttons.add(btn_impostazioni)

    # Label placeholder
    lbl_intro = Label(frame_panel, text="Scegli una schermata per cominciare...", font=("TkDefaultFont", 19), pady=30)
    lbl_intro.pack(side="top")

    paned_buttons.pack(side="top")
    frame_panel.pack(side="top")

    root.mainloop()

def build_panel(panel_id):
    # Pulisce il pannello per la prossima schermata
    for widget in frame_panel.winfo_children():
        widget.destroy()

    if panel_id == "ins":
        build_panel_inserimento()
    elif panel_id == "clas" :
        build_panel_classifica()
    elif panel_id == "imp":
        build_panel_impostazioni()
    else:
        messagebox.showerror("Errore", "Tipo di schermata non riconosciuto")

def build_panel_impostazioni():
    frm_impostazioni = Frame(frame_panel, pady=30)

    lbl_load = Label(frm_impostazioni, text="Carica da file", font=("TkDefaultFont", 19))
    lbl_load.pack(side="top")

    btn_load_csv = Button(frm_impostazioni, text="Carica partita da file CSV", command=(lambda: load_partita_from_file("csv")))
    btn_load_csv.pack(side="top")

    lbl_save = Label(frm_impostazioni, text="Salva su file", font=("TkDefaultFont", 19), pady=10)
    lbl_save.pack(side="top")

    btn_save_csv = Button(frm_impostazioni, text="Salva partita su file CSV", command=(lambda: save_partita_to_file("csv")))
    btn_save_csv.pack(side="top")

    frm_impostazioni.pack(side="top")

def build_panel_classifica():
    frm_classifica = Frame(frame_panel, pady=30)
    lbl_classifica = Label(frm_classifica, text="Classifica", font=("TkDefaultFont", 19))
    lbl_classifica.grid(row=0, column=0)

    frm_classifica.pack(side="top")

def build_panel_inserimento():
    global list_cmb_pacchi
    list_cmb_pacchi = []

    frm_inserimento = Frame(frame_panel, pady=30)
    lbl_input_pacchi = Label(frm_inserimento, text="Inserimento pacchi", font=("TkDefaultFont", 19))
    lbl_input_pacchi.grid(row=0, column=0)

    count = 1
    for i in range(2):
        for j in range(10):
            frm_pacco = Frame(frm_inserimento)
            lbl_pacco = Label(frm_pacco, text=str(count))

            cmb_pacco = ttk.Combobox(frm_pacco, state="readonly", postcommand=update_available_pacchi) # postcommand: eseguito prima che si generi la lista di opzioni
            cmb_pacco.bind("<<ComboboxSelected>>", lambda event, num_pacco=str(count): update_tonight_partita(event, num_pacco))
            cmb_pacco["values"] = POSSIBLE_PRIZES
            list_cmb_pacchi.append(cmb_pacco)

            lbl_pacco.grid(row=0, column=0)
            cmb_pacco.grid(row=0, column=1)
            frm_pacco.grid(row=j+1, column=i, padx=10, pady=5)

            count += 1

    frm_vincita = Frame(frm_inserimento)
    frm_vincita.grid(row=12,column=0)
    lbl_vincita = Label(frm_vincita, text="Vincita")
    lbl_vincita.grid(row=0, column=0)
    global entry_vincita
    entry_vincita = Entry(frm_vincita)
    entry_vincita.grid(row=0, column=1)
    btn_update_vincita = Button(frm_vincita, text="Conferma", command=lambda key="Vincita": update_tonight_partita(None, key))
    btn_update_vincita.grid(row=0, column=2)

    frm_tipo_vincita = Frame(frm_inserimento)
    frm_tipo_vincita.grid(row=13, column=0)
    lbl_tipo_vincita = Label(frm_tipo_vincita, text="Tipo vincita")
    lbl_tipo_vincita.grid(row=0, column=0)
    global cmb_tipo_vincita
    cmb_tipo_vincita = ttk.Combobox(frm_tipo_vincita, values=["Regione fortunata", "Offerta", "Pacco"], state="readonly")
    cmb_tipo_vincita.bind("<<ComboboxSelected>>", lambda event, key="Tipo vincita": update_tonight_partita(event, key))
    cmb_tipo_vincita.grid(row=0, column=1)

    btn_confirm_pacchi = Button(frm_inserimento, text="Salva in Parquet e Google Sheets💾", command=confirm_pacchi)
    btn_confirm_pacchi.grid(row=14, column=1, pady=5)
    btn_inserisci_caricati = Button(frm_inserimento, text="Inserisci dati caricati", command=inserimento_loaded_data)
    btn_inserisci_caricati.grid(row=15, column=1)

    frm_inserimento.pack(side="top")

def update_tonight_partita(event, key):
    if key != "Tipo vincita":
        if key == "Vincita":
            val = entry_vincita.get()
        else:
            val = event.widget.get()

        tonight_partita[key] = pacco_to_float(val)
    else:
        tonight_partita[key] = event.widget.get()

def update_available_pacchi():
    i = 0
    selected_prizes = []
    for cmb in list_cmb_pacchi:
        selected_prizes.insert(i, cmb.get())
        i += 1

    for cmb in list_cmb_pacchi:
        cmb["values"] = difference(POSSIBLE_PRIZES, selected_prizes)
    
def difference(l1, l2):
    tmp = []
    for element in l1:
        if element not in l2:
            tmp.append(element)
    return tmp

def confirm_pacchi():
    if messagebox.showwarning("Salvare la partita?", str_warning_salvataggio) == "ok":
        # Aggiorna il dataframe
        df_partite_affari_tuoi.loc[len(df_partite_affari_tuoi)] = tonight_partita
        
        try: # Salvataggio in locale
            df_partite_affari_tuoi.to_parquet("dataset_affari_tuoi.parquet")
        except:
            messagebox.showerror("Errore", "Errore nel salvataggio in Parquet.")

        
        index_tonight_partita = df_partite_affari_tuoi.shape[0] + 1

        try: # Salvataggio in cloud (Google Sheets)
            sheet.update(range_name=f"A{index_tonight_partita}:W{index_tonight_partita}", values=[tonight_partita])
        except:
            messagebox.showerror("Errore", "Errore nell'invio dei dati a Google Sheets")

def pacco_to_float(pacco: str):
    return float(pacco.replace(".", ""))

def float_to_pacco(premio):
    premio = float(premio)
    return f"{premio:,.0f}".replace(",", ".")

def load_partita_from_file(file_format):
    global tonight_partita
    if file_format == "csv":
        with open("saved_partita.csv", "r") as csv_data:
            reader = csv.reader(csv_data, delimiter=",")

            for key, loaded_val in zip(tonight_partita.keys(), next(reader)):
                tonight_partita[key] = loaded_val
    else:
        messagebox.showerror("Errore", "Tipo di file sconosciuto")

def inserimento_loaded_data():
    i = 0
    for data in tonight_partita.values():
        if i > 0 and i < 21:
            list_cmb_pacchi[i-1].set(float_to_pacco(data)) # Aggiorna combobox pacchi
        elif i == 21:
            entry_vincita.delete(0, END) # Aggiorna entry vincita
            entry_vincita.insert(0, data.split(".")[0])
        elif i == 22:
            cmb_tipo_vincita.set(data) # Aggiorna combobox tipo vincita
        i += 1

def save_partita_to_file(file_format):
    if file_format == "csv":
        with open("saved_partita.csv", "w", newline="") as csv_data:
            writer = csv.writer(csv_data, delimiter=",")
            writer.writerow(tonight_partita.values())
    else:
        messagebox.showerror("Errore", "Tipo di file sconosciuto")



if __name__ == "__main__":
    today = date.today()
    today_str = today.strftime("%d/%m/%y")

    str_warning_salvataggio = f"La partita del {today_str} verrà salvata in locale e su Google Sheets."

    df_partite_affari_tuoi = pd.read_parquet("dataset_affari_tuoi.parquet")
    tonight_partita = {"Data": today_str, "1": 0.0, "2": 0.0, "3": 0.0, "4": 0.0, "5": 0.0, "6": 0.0, "7": 0.0, 
                       "8": 0.0, "9": 0.0, "10": 0.0, "11": 0.0, "12": 0.0, "13": 0.0, "14": 0.0, "15": 0.0, "16": 0.0, 
                       "17": 0.0, "18": 0.0, "19": 0.0,"20": 0.0, "Vincita": "", "Tipo vincita": ""}
    list_cmb_pacchi = []

    POSSIBLE_PRIZES = ["0", "1", "5", "10", "20", "50", "75", "100", "200", "500", "5.000", "10.000", "15.000", "20.000", "30.000", 
                        "50.000", "75.000", "100.000", "200.000", "300.000"]

    # Spreadsheets API config
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    workbook = client.open_by_key("1kaKvRk6R95m9XySwtx_GQvxY2v3QQpTwTnWHPQveed8")
    sheet = workbook.worksheet("Dati")

    # Public widgets
    root = Tk()
    frame_panel = Frame(root)
    entry_vincita = None
    cmb_tipo_vincita = None

    main()