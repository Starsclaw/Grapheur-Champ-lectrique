import tkinter as tk
from tkinter import messagebox, filedialog
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.signal import savgol_filter
import numpy as np
import seaborn as sns

class App:
    def __init__(self, master):
        self.master = master
        master.title("Mon Application")

        # Création des variables pour stocker les données d'entrée
        self.input_data1 = tk.StringVar(value="")
        self.input_dataentrytemps2 = tk.StringVar(value="")
        self.input_data2 = tk.StringVar(value="")
        self.input_synchrocam_temps=tk.StringVar(value="")
        self.polynome = tk.StringVar(value="")
        self.file_path1 = tk.StringVar(value="")
        self.file_path2 = tk.StringVar(value="")
        self.file_path3= tk.StringVar(value="")
        self.file_checkbox_var = tk.BooleanVar(value=False)
        self.lissage_checkbox_var = tk.BooleanVar(value=False)
        self.camera_checkbox_var = tk.BooleanVar(value=False)

        # Création des variables pour stocker l'état des cases cochées
        self.checkbox_var1 = tk.BooleanVar(value=False)
        self.checkbox_var2 = tk.BooleanVar(value=False)
        self.checkbox_var3 = tk.BooleanVar(value=False)
        self.checkbox_var4 = tk.BooleanVar(value=False)
        self.checkbox_var5 = tk.BooleanVar(value=False)

        # Variables pour les données supplémentaires
        self.lissage= tk.StringVar(value="")
        self.antenna_factor = tk.StringVar(value="")
        self.resistance_value = tk.StringVar(value="")
        self.capacitance_value = tk.StringVar(value="")
        self.fenetreTension_value = tk.StringVar(value="")
        self.fenetreTension_value2 = tk.StringVar(value="")
        self.fenetrecourant_value = tk.StringVar(value="")
        self.fenetrecourant_value2 = tk.StringVar(value="")
        self.fenetrecharge_value = tk.StringVar(value="")
        self.fenetrecharge_value2 = tk.StringVar(value="")
        self.fenetrePMT_value = tk.StringVar(value="")
        self.fenetrePMT_value2 = tk.StringVar(value="")
        self.fenetreCE_value = tk.StringVar(value="")
        self.fenetreCE_value2 = tk.StringVar(value="")
        self.fenetretemps_value = tk.StringVar(value="")
        self.fenetretemps_value2 = tk.StringVar(value="")


        # Chargement des données sauvegardées
        self.load_saved_data()

        # Création des widgets
        self.create_widgets()

    def create_widgets(self):
        # Étiquettes et champs de saisie pour les données numériques
        self.label1 = tk.Label(self.master, text="Plage de temps enregistré [*,*]")
        self.label1.grid(row=0, column=0)
        self.entry1 = tk.Entry(self.master, textvariable=self.input_data1)
        self.entry1.grid(row=0, column=1)

        self.entrytemps2 = tk.Entry(self.master, textvariable=self.input_dataentrytemps2)
        self.entrytemps2.grid(row=0, column=2)

        self.label2 = tk.Label(self.master, text="Nom fichier")
        self.label2.grid(row=1, column=0)
        self.entry2 = tk.Entry(self.master, textvariable=self.input_data2)
        self.entry2.grid(row=1, column=1)

        # Étiquettes pour les chemins d'accès aux fichiers
        self.label3 = tk.Label(self.master, text="Chemin d'accès au fichier avec plasma:")
        self.label3.grid(row=2, column=0)
        self.entry3 = tk.Entry(self.master, textvariable=self.file_path1)
        self.entry3.grid(row=2, column=1)
        self.browse_button1 = tk.Button(self.master, text="Parcourir", command=self.browse_file1)
        self.browse_button1.grid(row=2, column=2)

        self.label4 = tk.Label(self.master, text="Chemin d'accès au fichier sans plasma:")
        self.label4.grid(row=3, column=0)
        self.entry4 = tk.Entry(self.master, textvariable=self.file_path2, state="readonly")
        self.entry4.grid(row=3, column=1)
        self.browse_button2 = tk.Button(self.master, text="Parcourir", command=self.browse_file2, state="disabled")
        self.browse_button2.grid(row=3, column=2)

        # Case à cocher pour activer la sélection de fichier
        self.file_checkbox = tk.Checkbutton(self.master, text="Avez-vous les fichiers de données sans plasma", variable=self.file_checkbox_var, command=self.toggle_file_entry)
        self.file_checkbox.grid(row=3, column=3, columnspan=2)

        self.label_graphesave_4 = tk.Label(self.master, text="Chemin d'accès figures:")
        self.label_graphesave_4.grid(row=4, column=0)
        self.entry_graphesave_4 = tk.Entry(self.master, textvariable=self.file_path3 , state="readonly")
        self.entry_graphesave_4.grid(row=4, column=1)
        self.browse_button3 = tk.Button(self.master, text="Parcourir", command=self.browse_file3)
        self.browse_button3.grid(row=4, column=2)

        # Cases à cocher pour les options
        self.checkbox1 = tk.Checkbutton(self.master, text="Haute tension", variable=self.checkbox_var1, command=self.show_fenetre_Tension)
        self.checkbox1.grid(row=5, column=0)

        self.checkbox2 = tk.Checkbutton(self.master, text="Courant", variable=self.checkbox_var2, command=self.show_fenetre_courant)
        self.checkbox2.grid(row=5, column=1)

        self.checkbox3 = tk.Checkbutton(self.master, text="Charge", variable=self.checkbox_var3, command=self.show_fenetre_charge)
        self.checkbox3.grid(row=5, column=2)

        self.checkbox4 = tk.Checkbutton(self.master, text="PMT", variable=self.checkbox_var4, command=self.show_fenetre_PMT)
        self.checkbox4.grid(row=5, column=3)

        self.checkbox5 = tk.Checkbutton(self.master, text="Champ électrique", variable=self.checkbox_var5, command=self.show_fenetre_CE)
        self.checkbox5.grid(row=5, column=4)

        # Champs de saisie pour les données supplémentaires
        self.antenna_factor_label = tk.Label(self.master, text="Facteur d'antenne:")
        self.antenna_factor_label.grid(row=6, column=0)
        self.antenna_factor_entry = tk.Entry(self.master, textvariable=self.antenna_factor, state="disabled")
        self.antenna_factor_entry.grid(row=6, column=1)

        self.resistance_label = tk.Label(self.master, text="Résistance:")
        self.resistance_label.grid(row=7, column=0)
        self.resistance_entry = tk.Entry(self.master, textvariable=self.resistance_value, state="disabled")
        self.resistance_entry.grid(row=7, column=1)

        self.capacitance_label = tk.Label(self.master, text="Capacité:")
        self.capacitance_label.grid(row=8, column=0)
        self.capacitance_entry = tk.Entry(self.master, textvariable=self.capacitance_value, state="disabled")
        self.capacitance_entry.grid(row=8, column=1)

        self.fenetreTension_label = tk.Label(self.master, text="Fenêtre tension appliquée")
        self.fenetreTension_label.grid(row=10, column=0)
        self.fenetreTension_entry = tk.Entry(self.master, textvariable=self.fenetreTension_value, state="disabled")
        self.fenetreTension_entry.grid(row=10, column=1)
        self.fenetreTension_entry2 = tk.Entry(self.master, textvariable=self.fenetreTension_value2, state="disabled")
        self.fenetreTension_entry2.grid(row=10, column=2)

        self.fenetrecourant_label = tk.Label(self.master, text="Fenêtre Courant")
        self.fenetrecourant_label.grid(row=10, column=3)
        self.fenetrecourant_entry = tk.Entry(self.master, textvariable=self.fenetrecourant_value, state="disabled")
        self.fenetrecourant_entry.grid(row=10, column=4)
        self.fenetrecourant_entry2 = tk.Entry(self.master, textvariable=self.fenetrecourant_value2, state="disabled")
        self.fenetrecourant_entry2.grid(row=10, column=5)

        self.fenetrecharge_label = tk.Label(self.master, text="Fenêtre Charge")
        self.fenetrecharge_label.grid(row=10, column=6)
        self.fenetrecharge_entry = tk.Entry(self.master, textvariable=self.fenetrecharge_value, state="disabled")
        self.fenetrecharge_entry.grid(row=10, column=7)
        self.fenetrecharge_entry2 = tk.Entry(self.master, textvariable=self.fenetrecharge_value2, state="disabled")
        self.fenetrecharge_entry2.grid(row=10, column=8)

        self.fenetretemps_label = tk.Label(self.master, text="Fenetre temps zoomé")
        self.fenetretemps_label.grid(row=11, column=0)
        self.fenetretemps_entry = tk.Entry(self.master, textvariable=self.fenetretemps_value)
        self.fenetretemps_entry.grid(row=11, column=1)
        self.fenetretemps_entry2 = tk.Entry(self.master, textvariable=self.fenetretemps_value2)
        self.fenetretemps_entry2.grid(row=11, column=2)

        self.fenetrePMT_label = tk.Label(self.master, text="Fenetre PMT")
        self.fenetrePMT_label.grid(row=11, column=3)
        self.fenetrePMT_entry = tk.Entry(self.master, textvariable=self.fenetrePMT_value, state="disabled")
        self.fenetrePMT_entry.grid(row=11, column=4)
        self.fenetrePMT_entry2 = tk.Entry(self.master, textvariable=self.fenetrePMT_value2, state="disabled")
        self.fenetrePMT_entry2.grid(row=11, column=5)

        self.fenetreCE_label = tk.Label(self.master, text="Fenetre Champ électrique")
        self.fenetreCE_label.grid(row=11, column=6)
        self.fenetreCE_entry = tk.Entry(self.master, textvariable=self.fenetreCE_value, state="disabled")
        self.fenetreCE_entry.grid(row=11, column=7)
        self.fenetreCE_entry2 = tk.Entry(self.master, textvariable=self.fenetreCE_value2, state="disabled")
        self.fenetreCE_entry2.grid(row=11, column=8)

        #####Lissage
        self.lissage_checkbox = tk.Checkbutton(self.master, text="Lissage savgol?",variable=self.lissage_checkbox_var, command=self.show_fenetre_lissage)
        self.lissage_checkbox.grid(row=12, column=0)

        self.lissage_label = tk.Label(self.master, text="Fenêtre utilisé")
        self.lissage_label.grid(row=12, column=1)
        self.lissage_entry = tk.Entry(self.master, textvariable=self.lissage)
        self.lissage_entry.grid(row=12, column=2)

        self.polynome_label= tk.Label(self.master, text="Degré du polynome")
        self.polynome_label.grid(row=12, column=3)
        self.polynome_entry = tk.Entry(self.master, textvariable=self.polynome)
        self.polynome_entry.grid(row=12, column=4)


        self.camera_checkbox = tk.Checkbutton(self.master, text="Synchro caméra?",variable=self.camera_checkbox_var)
        self.camera_checkbox.grid(row=13, column=0)

        self.input_synchrocam_temps_label = tk.Label(self.master, text="Quel est le temps correspondant?")
        self.input_synchrocam_temps_label.grid(row=13, column=1)
        self.input_synchrocam_temps_entry = tk.Entry(self.master, textvariable=self.input_synchrocam_temps)
        self.input_synchrocam_temps_entry.grid(row=13, column=2)

        # Bouton pour sauvegarder les données
        self.save_button = tk.Button(self.master, text="Sauvegarder", command=self.save_data)
        self.save_button.grid(row=9, column=0, columnspan=5)



        # Création de la frame pour la figure
        self.figure_frame = tk.Frame(self.master)
        self.figure_frame.grid(row=0, column=9, rowspan=11)

        # Création de la figure
        self.figure = plt.figure(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.figure_frame)
        self.canvas.get_tk_widget().pack()

    def browse_file1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path1.set(file_path)

    def browse_file2(self):
        file_path2 = filedialog.askopenfilename()
        if file_path2:
            self.file_path2.set(file_path2)

    def browse_file3(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.file_path3.set(folder_path)

    def toggle_file_entry(self):
        if self.file_checkbox_var.get():
            if hasattr(self, 'browse_button2'):
                self.browse_button2.config(state="normal")
        else:
            if hasattr(self, 'browse_button2'):
                self.browse_button2.config(state="disabled")

    def show_fenetre_Tension(self):
        if self.checkbox_var1.get():
            self.fenetreTension_entry.config(state="normal")
            self.fenetreTension_entry2.config(state="normal")
            self.fenetreTension_label.config(state="normal")
        else:
            self.fenetreTension_entry.config(state="disabled")
            self.fenetreTension_entry2.config(state="disabled")
            self.fenetreTension_label.config(state="disabled")

    def show_fenetre_courant(self):
        if self.checkbox_var2.get():
            self.fenetrecourant_entry.config(state="normal")
            self.fenetrecourant_entry2.config(state="normal")
            self.fenetrecourant_label.config(state="normal")
            self.resistance_entry.config(state="normal")
            self.resistance_label.config(state="normal")
        else:
            self.fenetrecourant_entry.config(state="disabled")
            self.fenetrecourant_entry2.config(state="disabled")
            self.fenetrecourant_label.config(state="disabled")
            self.resistance_entry.config(state="disabled")
            self.resistance_label.config(state="disabled")

    def show_fenetre_charge(self):
        if self.checkbox_var3.get():
            self.fenetrecharge_entry.config(state="normal")
            self.fenetrecharge_entry2.config(state="normal")
            self.fenetrecharge_label.config(state="normal")
            self.capacitance_entry.config(state="normal")
            self.capacitance_label.config(state="normal")
        else:
            self.fenetrecharge_entry.config(state="disabled")
            self.fenetrecharge_entry2.config(state="disabled")
            self.fenetrecharge_label.config(state="disabled")
            self.capacitance_entry.config(state="disabled")
            self.capacitance_label.config(state="disabled")

    def show_fenetre_PMT(self):
        if self.checkbox_var4.get():
            self.fenetrePMT_entry.config(state="normal")
            self.fenetrePMT_entry2.config(state="normal")
            self.fenetrePMT_label.config(state="normal")
        else:
            self.fenetrePMT_entry.config(state="disabled")
            self.fenetrePMT_entry2.config(state="disabled")
            self.fenetrePMT_label.config(state="disabled")

    def show_fenetre_CE(self):
        if self.checkbox_var5.get():
            self.fenetreCE_entry.config(state="normal")
            self.fenetreCE_label.config(state="normal")
            self.fenetreCE_entry2.config(state="normal")
            self.antenna_factor_entry.config(state="normal")
            self.antenna_factor_label.config(state="normal")
        else:
            self.fenetreCE_entry.config(state="disabled")
            self.fenetreCE_entry2.config(state="disabled")
            self.fenetreCE_label.config(state="disabled")

    def show_fenetre_lissage(self):
        if self.lissage_checkbox_var.get():
            self.lissage_entry.config(state="normal")
            self.lissage_label.config(state="normal")
        else:
            self.lissage.config(state="disabled")
            self.lissage_label.config(state="disabled")

    def show_camera(self):
        if self.camera_checkbox_var.get():
            self.input_synchrocam_temps_entry.config(state="normal")
            self.input_synchrocam_temps_label.config(state="normal")
        else:
            self.input_synchrocam_temps_entry.config(state="disabled")
            self.input_synchrocam_temps_label.config(state="disabled")

    def save_data(self):
        # Récupération des données saisies par l'utilisateur
        data1 = self.input_data1.get()
        data2 = self.input_data2.get()
        dataentrytemps2=self.input_dataentrytemps2.get()
        file1_path = self.file_path1.get()
        file2_path = self.file_path2.get()
        file3_path= self.file_path3.get()

        # Récupération de l'état des cases cochées
        checkbox_states = [
            self.checkbox_var1.get(),
            self.checkbox_var2.get(),
            self.checkbox_var3.get(),
            self.checkbox_var4.get(),
            self.checkbox_var5.get()
        ]

        # Création des DataFrames waveform

        #columns = [self.clean_checkbox_name(checkbox) for checkbox, state in zip([self.checkbox1, self.checkbox2, self.checkbox3, self.checkbox4, self.checkbox5], checkbox_states) if state]
        if self.checkbox_var2.get()==True:
            columns=["haute_tension","courant","pmt","champ_électrique"]
        if self.checkbox_var3.get() == True:
            columns = ["haute_tension", "charge", "pmt", "champ_électrique"]
        else:
            columns = ["haute_tension", "courant", "pmt", "champ_électrique"]
        if file1_path:
            waveform = pd.read_csv(file1_path, names=columns)


        else:
            waveform = pd.DataFrame(columns=columns)
            print("Aucun fichier avec plasma sélectionné.")


        if self.file_checkbox_var.get() == True:
            waveformwop = pd.read_csv(file2_path, names=columns)


        else:
            waveformwop = pd.DataFrame(columns=columns)
            print("Aucun fichier avec plasma sélectionné.")

        temps = pd.DataFrame(np.linspace(float(self.entry1.get()), float(self.entrytemps2.get()), np.size(waveform['haute_tension'])), columns=['temps'])


        ##############################################lissage
        if self.lissage_checkbox_var.get() == True:
            if self.checkbox_var1.get()==True:
                waveform['haute_tension']=savgol_filter(waveform['haute_tension'], int(self.lissage_entry.get()), int(self.polynome_entry.get()))
            if self.checkbox_var2.get()==True:
                waveform['courant']=savgol_filter(waveform['courant'], int(self.lissage_entry.get()), int(self.polynome_entry.get()))
            if self.checkbox_var3.get() == True:
                waveform['charge'] = savgol_filter(waveform['charge'], int(self.lissage_entry.get()),int(self.polynome_entry.get()))
            if self.checkbox_var4.get() == True:
                waveform['pmt'] = savgol_filter(waveform['pmt'], int(self.lissage_entry.get()),int(self.polynome_entry.get()))
            if self.checkbox_var5.get() == True:
                waveform['champ_électrique'] = savgol_filter(waveform['champ_électrique'], int(self.lissage_entry.get()),int(self.polynome_entry.get()))

            if self.file_checkbox_var.get() == True:
                if self.checkbox_var1.get() == True:
                    waveformwop['haute_tension'] = savgol_filter(waveformwop['haute_tension'],int(self.lissage_entry.get()),int(self.polynome_entry.get()))
                if self.checkbox_var2.get() == True:
                    waveformwop['courant'] = savgol_filter(waveformwop['courant'], int(self.lissage_entry.get()),int(self.polynome_entry.get()))
                if self.checkbox_var3.get() == True:
                    waveformwop['charge'] = savgol_filter(waveformwop['charge'], int(self.lissage_entry.get()),int(self.polynome_entry.get()))
                if self.checkbox_var4.get() == True:
                    waveformwop['pmt'] = savgol_filter(waveformwop['pmt'], int(self.lissage_entry.get()),int(self.polynome_entry.get()))
                if self.checkbox_var5.get() == True:
                    waveformwop['champ_électrique'] = savgol_filter(waveformwop['champ_électrique'],int(self.lissage_entry.get()),int(self.polynome_entry.get()))


        #Courant/charges
        if self.checkbox_var2.get()==True:
            waveform["courant"]=(waveform["courant"]*1000)/int(self.resistance_entry.get())
        if self.checkbox_var3.get()==True:
            waveform["charge"]=(waveform["charge"]*1e9)*float(self.capacitance_entry.get())


        #####   CHAMP
        if self.checkbox_var5.get()== True:
            facteur_antenne=10**(int(self.antenna_factor_entry.get())/20)
            waveform["champ_électrique"]=waveform["champ_électrique"]*facteur_antenne/1000
            if self.file_checkbox_var.get() == True:
                waveformwop["champ_électrique"]=waveformwop["champ_électrique"]*facteur_antenne/1000
                waveform["champ_soustrait"]=waveform["champ_électrique"]-waveformwop["champ_électrique"]

        def tracer_graphiques(temps, variables, bools, fenêtretempszoom, camera_checkbox, synchro_cam_entry):
            fig, ax1 = plt.subplots(figsize=(10, 6),
                                    dpi=300)  # Augmentation de la résolution et de la taille de la figure
            axes = [ax1]

            # Définition des couleurs pour chaque variable
            colors = {'Applied Voltage [V]': 'orange', 'Current [mA]': 'black', 'Charge [nC]': 'black',
                      'PMT [V]': 'green', 'Electric field [kV/m]': 'blue'}

            lines = []

            max_ticks = 6  # Nombre maximum de ticks sur l'axe y

            for var, b in zip(variables, bools):
                if var is not None and (b or all(bool == False for bool in bools)):
                    ax = ax1 if len(axes) == 1 else ax1.twinx()

                    color = colors[var.label]

                    line, = ax.plot(temps['temps'], var.data, color=color, label=var.label, linewidth=2)
                    ax.set_ylabel(var.label, color=color, fontsize=16)
                    ax.tick_params(axis='y', labelcolor=color, labelsize=13)
                    ax.tick_params(axis='x', labelsize=13)

                    ax.spines['left' if len(axes) == 1 else 'right'].set_color(color)
                    ax.spines['left' if len(axes) == 1 else 'right'].set_linewidth(2)


                    if len(axes) > 1:
                        ax.spines['right'].set_position(('outward', 80 * (len(axes) - 2)))

                    axes.append(ax)
                    lines.append(line)
                    ax.set_ylim(var.fenetre)
                    ax.yaxis.set_major_locator(plt.MaxNLocator(max_ticks))  # Définir le nombre maximum de ticks
            x=''
            if camera_checkbox:
                x = float(synchro_cam_entry) + 0.840
                if float(synchro_cam_entry)> 495:
                    x = float(synchro_cam_entry) + 0.840

                ax1.axvline(x, color='grey')
                x_str = "{:.2f}".format(x)
                plt.title(self.entry2.get() + " " + x_str + "µs", fontsize=16)
            else:
                plt.title(self.entry2.get(), fontsize=16)

            plt.tight_layout()
            ax.spines['left'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.set_xlabel("Time [µs]", fontsize=16)

            labels = [line.get_label() for line in lines]
            plt.legend(lines, labels, loc='lower right' if len(axes) > 1 else 'upper left', fontsize=11)

            plt.tight_layout()
            ax1.grid(True, linestyle='--', which='both')

            plt.savefig(file3_path + '\\' + self.input_data2.get()  + '.png',
            bbox_inches = 'tight')  # Utilisation de bbox_inches pour ajuster la boîte autour de la figure

            ax.set_xlim(fenêtretempszoom)
            plt.savefig(file3_path + '\\' + self.input_data2.get() + "Zoomed" + str(x) + '.png', bbox_inches='tight')
            plt.show()

            if self.file_checkbox_var.get():
                fig, ax1 = plt.subplots(figsize=(10, 6), dpi=300)
                plt.grid(linestyle='--')

                ax2 = ax1.twinx()
                line1 = ax1.plot(temps['temps'], waveform["haute_tension"], color="orange", label="Applied Voltage",
                                 linewidth=2)
                line2 = ax2.plot(temps['temps'], waveform["champ_électrique"], color="green",
                                 label="Electric field measured", linewidth=2)
                line3 = ax2.plot(temps['temps'], waveformwop["champ_électrique"], color="red",
                                 label="Laplacian Electric field", linewidth=2)
                line4 = ax2.plot(temps['temps'], waveform["champ_soustrait"], color="blue",
                                 label="Electric field substracted", linewidth=2)

                ax1.set_ylabel("Applied Voltage [V]", fontsize=16, color="orange")
                ax2.set_ylabel("Electric field [kV/m]", fontsize=16)
                ax1.set_xlabel("Time [µs]", fontsize=16)
                ax1.set_ylim(fenêtreHauteTension)
                ax2.set_ylim(fenêtreCE)

                ax2.spines['left'].set_linewidth(2)
                ax2.spines['right'].set_linewidth(2)
                ax2.spines['left'].set_color("orange")

                ax1.tick_params(axis='y', labelcolor="orange", labelsize=13)
                ax2.tick_params(axis='y', labelsize=13)
                ax1.tick_params(axis='x', labelsize=13)

                x = ''
                if camera_checkbox:


                    x = float(synchro_cam_entry) + 0.840
                    if float(synchro_cam_entry) > 495:
                        x = float(synchro_cam_entry) + 0.840

                    ax1.axvline(x, color='grey')
                    x = "{:.2f}".format(x)
                    print(x)
                    plt.title(self.entry2.get() + " All fields" + str(x) + "µs", fontsize=16)
                else:
                    plt.title(self.entry2.get() + " All fields", fontsize=16)
                plt.tight_layout()
                lines = line1 + line3 + line2 + line4
                label = [l.get_label() for l in lines]
                ax1.legend(lines, label, loc='lower right', fontsize=10)

                plt.savefig(file3_path + '\\' + self.input_data2.get() + " All fields" + '.png',
                              bbox_inches='tight')
                ax1.set_xlim(fenêtretempszoom)
                plt.savefig(file3_path + '\\' + self.input_data2.get()  + " All fields" + "Zoomed" + '.png',bbox_inches = 'tight')
                plt.show()

        class Variable:
            def __init__(self, data=None, label=None, fenetre=None):
                self.data = data
                self.label = label
                self.fenetre = fenetre
        bools = checkbox_states

        fenêtreHauteTension = [int(self.fenetreTension_value.get()), int(self.fenetreTension_value2.get())]
        fenêtrecourant = [int(self.fenetrecourant_value.get()), int(self.fenetrecourant_value2.get())]
        fenêtrecharge = [int(self.fenetrecharge_value.get()), int(self.fenetrecharge_value2.get())]
        fenêtrePMT = [float(self.fenetrePMT_value.get()), float(self.fenetrePMT_value2.get())]
        fenêtreCE = [int(self.fenetreCE_value.get()), int(self.fenetreCE_value2.get())]
        fenêtretempszoom = [float(self.fenetretemps_entry.get()), float(self.fenetretemps_entry2.get())]

        champ_soustrait_data = waveform['champ_soustrait'] if self.file_checkbox_var.get() == True and bools[
            4] else None
        champ_electrique_data = waveform['champ_électrique'] if bools[4] else None

        variables = [
            Variable(waveform['haute_tension'] if bools[0] else None, 'Applied Voltage [V]', fenêtreHauteTension),
            Variable(waveform['courant'] if bools[1] else None, 'Current [mA]', fenêtrecourant),
            Variable(waveform['charge'] if bools[2] else None, 'Charge [nC]', fenêtrecharge),
            Variable(waveform['pmt'] if bools[3] else None, 'PMT [V]', fenêtrePMT),
            Variable(champ_soustrait_data if champ_soustrait_data is not None else champ_electrique_data,
                     'Electric field [kV/m]', fenêtreCE)
        ]





        # Appel de la fonction pour tracer les graphiques en fonction des booléens
        camera_checkboxcheck=self.camera_checkbox_var.get()
        input_synchrocam=self.input_synchrocam_temps_entry.get()
        tracer_graphiques(temps, variables, bools,fenêtretempszoom,camera_checkboxcheck,float(self.input_synchrocam_temps_entry.get()))
        print("LE PRINT EST IICICICICIICICIC",self.camera_checkbox_var.get(),float(self.input_synchrocam_temps_entry.get()))

        # Affichage du graphique dans l'interface utilisateur
        self.canvas.draw_idle()
        file_checkbox_state = self.file_checkbox_var.get()
        file_checkbox_state_lissage = self.lissage_checkbox_var.get()
        # Sauvegarde des données dans un fichier JSON
        data = {
            "data1": data1,
            "dataentrytemps2": dataentrytemps2,
            "data2": data2,
            "file1_path": file1_path,
            "file2_path": file2_path,
            "file3_path": file3_path,
            "lissage":self.lissage.get(),
            "polynome":self.polynome.get(),
            "question":file_checkbox_state,
            "lissage_checkbox": file_checkbox_state_lissage,
            "camera_checkbox" : camera_checkboxcheck,
            "input_synchrocam_temps_entry" : input_synchrocam ,
            "checkbox_states": checkbox_states,
            "antenna_factor": self.antenna_factor.get(),
            "resistance_value": self.resistance_value.get(),
            "capacitance_value": self.capacitance_value.get(),
            "Fenetre tension appliquee": self.fenetreTension_value.get(),
            "Fenetre tension appliquee2": self.fenetreTension_value2.get(),
            "Fenêtre Courant": self.fenetrecourant_value.get(),
            "Fenêtre Courant2": self.fenetrecourant_value2.get(),
            "Fenêtre Charge": self.fenetrecharge_value.get(),
            "Fenêtre Charge2": self.fenetrecharge_value2.get(),
            "Fenetre temps": self.fenetretemps_value.get(),
            "Fenetre temps2": self.fenetretemps_value2.get(),
            "Fenetre PMT": self.fenetrePMT_value.get(),
            "Fenetre PMT2": self.fenetrePMT_value2.get(),
            "Fenetre CE": self.fenetreCE_value.get(),
            "Fenetre CE2": self.fenetreCE_value2.get(),

        }
        with open("saved_data.json", "w") as file:
            json.dump(data, file)

        # Affichage d'un message de confirmation
        messagebox.showinfo("Sauvegarde", "Données sauvegardées avec succès!")

    def clean_checkbox_name(self, checkbox):
        return checkbox.cget("text").replace(" ", "_").lower()

    def load_saved_data(self):
        # Vérifie si le fichier de sauvegarde existe, le cas échéant, charge les données
        if os.path.exists("saved_data.json"):
            with open("saved_data.json", "r") as file:
                data = json.load(file)
                self.input_data1.set(data.get("data1", ""))
                self.input_data2.set(data.get("data2", ""))
                self.input_dataentrytemps2.set(data.get("dataentrytemps2", ""))
                self.file_path1.set(data.get("file1_path", ""))
                self.file_path2.set(data.get("file2_path", ""))
                self.file_path3.set(data.get("file3_path", ""))

                # Vérification de l'état de la case à cocher
                if data.get("file2_path"):
                    self.file_checkbox_var.set(True)
                    self.toggle_file_entry()

                # Chargement de l'état des cases cochées
                checkbox_states = data.get("checkbox_states", [False]*5)
                self.checkbox_var1.set(checkbox_states[0])
                self.checkbox_var2.set(checkbox_states[1])
                self.checkbox_var3.set(checkbox_states[2])
                self.checkbox_var4.set(checkbox_states[3])
                self.checkbox_var5.set(checkbox_states[4])
                self.lissage_checkbox_var.set(data.get("lissage_checkbox", False))
                self.camera_checkbox_var.set(data.get("camera_checkbox", False))
                self.file_checkbox_var.set(data.get("question", False))
                # Chargement des données supplémentaires
                self.antenna_factor.set(data.get("antenna_factor", ""))
                self.resistance_value.set(data.get("resistance_value", ""))
                self.capacitance_value.set(data.get("capacitance_value", ""))
                self.fenetreTension_value.set(data.get("Fenetre tension appliquee", ""))
                self.fenetreTension_value2.set(data.get("Fenetre tension appliquee2", ""))
                self.fenetrecourant_value.set(data.get("Fenêtre Courant", ""))
                self.fenetrecourant_value2.set(data.get("Fenêtre Courant2", ""))
                self.fenetrecharge_value.set(data.get("Fenêtre Charge", ""))
                self.fenetrecharge_value2.set(data.get("Fenêtre Charge2", ""))
                self.fenetretemps_value.set(data.get("Fenetre temps", ""))
                self.fenetretemps_value2.set(data.get("Fenetre temps2", ""))
                self.fenetrePMT_value.set(data.get("Fenetre PMT", ""))
                self.fenetrePMT_value2.set(data.get("Fenetre PMT2", ""))
                self.fenetreCE_value.set(data.get("Fenetre CE", ""))
                self.fenetreCE_value2.set(data.get("Fenetre CE2", ""))
                self.lissage.set(data.get("lissage", ""))
                self.input_synchrocam_temps.set(data.get("input_synchrocam_temps_entry", ""))
                self.polynome.set(data.get("polynome", ""))


# Création de la fenêtre principale
root = tk.Tk()

# Création de l'instance de l'application
app = App(root)

# Boucle principale
root.mainloop()
