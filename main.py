from tkinter import Button, Entry, Frame, Label, PanedWindow, Tk, messagebox, ttk

POSSIBLE_PRIZES = ["0", "1", "5", "10", "20", "50", "75", "100", "200", "500", "5.000", "10.000", "15.000", "20.000", "30.000", 
                    "50.000", "75.000", "100.000", "200.000", "300.000"]
root = Tk()
frame_panel = Frame(root)

def main():
    root.title("Affari Tuoi Manager")
    root.geometry("800x600")

    # Menu bottoni schermate
    paned_buttons = PanedWindow(root, orient="horizontal")

    btn_inserimento = Button(paned_buttons, text="Inserimento", command=(lambda: build_panel("ins")))
    btn_inserimento.pack(side="left")
    paned_buttons.add(btn_inserimento)

    btn_classifica = Button(paned_buttons, text="Classifica", command=(lambda: build_panel("clas")))
    btn_classifica.pack(side="left")
    paned_buttons.add(btn_classifica)

    btn_impostazioni = Button(paned_buttons, text="Impostazioni", command=(lambda: build_panel("imp")))
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

def build_panel_impostazioni(): # TODO riabilitare i command con funzione/lettura e scrittura da/su file .parquet
    frm_impostazioni = Frame(frame_panel, pady=30)
    lbl_impostazioni = Label(frm_impostazioni, text="Impostazioni", font=("TkDefaultFont", 19))
    lbl_impostazioni.pack(side="top")

    btn_load = Button(frm_impostazioni, text="Carica da file Parquet") # , command=load_from_file
    btn_load.pack(side="top")

    btn_save = Button(frm_impostazioni, text="Salva su file Parquet") # , command=save_to_file
    btn_save.pack(side="top")

    frm_impostazioni.pack(side="top")

def build_panel_classifica():
    frm_classifica = Frame(frame_panel, pady=30)
    lbl_classifica = Label(frm_classifica, text="Classifica", font=("TkDefaultFont", 19))
    lbl_classifica.grid(row=0, column=0)

    frm_classifica.pack(side="top")

def build_panel_inserimento(): # TODO riabilitare i command e postcommand di button e combobox
    frm_inserimento = Frame(frame_panel, pady=30)
    lbl_input_pacchi = Label(frm_inserimento, text="Inserimento pacchi", font=("TkDefaultFont", 19))
    lbl_input_pacchi.grid(row=0, column=0)

    count = 1
    for i in range(2):
        for j in range(10):
            frm_pacco = Frame(frm_inserimento)
            lbl_pacco = Label(frm_pacco, text=str(count))

            cmb_pacco = ttk.Combobox(frm_pacco, state='readonly') # , postcommand=update_available_pacchi
            cmb_pacco['values'] = POSSIBLE_PRIZES
            # list_cmb_pacchi.append(cmb_pacco)

            lbl_pacco.grid(row=0, column=0)
            cmb_pacco.grid(row=0, column=1)
            frm_pacco.grid(row=j+1, column=i, padx=10, pady=5)

            count += 1

    frm_vincita = Frame(frm_inserimento)
    frm_vincita.grid(row=12,column=0)
    lbl_vincita = Label(frm_vincita, text="Vincita")
    lbl_vincita.grid(row=0, column=0)
    entry_vincita = Entry(frm_vincita)
    entry_vincita.grid(row=0, column=1)

    frm_tipo_vincita = Frame(frm_inserimento)
    frm_tipo_vincita.grid(row=13, column=0)
    lbl_tipo_vincita = Label(frm_tipo_vincita, text="Tipo vincita")
    lbl_tipo_vincita.grid(row=0, column=0)
    cmb_tipo_vincita = ttk.Combobox(frm_tipo_vincita, values=["Regione fortunata", "Offerta", "Pacco"], state='readonly')
    cmb_tipo_vincita.grid(row=0, column=1)

    btn_confirm_pacchi = Button(frm_inserimento, text="Salva su Google Sheets") # , command=(lambda: confirmPacchi(entry_vincita, cmb_tipo_vincita))
    btn_confirm_pacchi.grid(row=14, column=1, pady=10)

    frm_inserimento.pack(side="top")

if __name__ == "__main__":
    main()