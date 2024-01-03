import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from ttkthemes import ThemedStyle

class InterfaceMistral(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Interface Mistral')

        # Appliquer le thème 'arc'
        style = ThemedStyle(self)
        style.set_theme("arc")

        # Configuration du fond
        self.configure(bg='#121212')
        style.configure('TFrame', background='#2E1437')
        style.configure('TLabel', background='#2E1437', foreground='#ffffff')
        style.configure('TButton', background='#ffffff', foreground='#000000')
        style.configure('TCombobox', fieldbackground='#ffffff', foreground='#000000')
        style.configure('TEntry', fieldbackground='#ffffff', foreground='#000000')

        # Variables pour stocker les entrées utilisateur
        self.api_key_var = tk.StringVar()
        self.api_key_var.set('')  # Initialiser avec une chaîne vide
        self.model_var = tk.StringVar()
        self.model_var.set('mistral-tiny')
        self.role_var = tk.StringVar()
        self.role_var.set('user')
        self.content_var = tk.StringVar()
        self.content_var.set('Who is the most renowned French painter?')
        self.result_var = tk.StringVar()

        # Créer les widgets
        self.frame = ttk.Frame(self)
        self.frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        self.label_api_key = ttk.Label(self.frame, text='Clé API Mistral:')
        self.entry_api_key = ttk.Entry(self.frame, textvariable=self.api_key_var, show='*')
        self.label_model = ttk.Label(self.frame, text='Modèle:')
        self.combo_model = ttk.Combobox(self.frame, textvariable=self.model_var, values=['mistral-tiny', 'mistral-small', 'mistral-medium'])
        self.label_role = ttk.Label(self.frame, text='Rôle:')
        self.combo_role = ttk.Combobox(self.frame, textvariable=self.role_var, values=['user', 'assistant'])
        self.label_content = ttk.Label(self.frame, text='Contenu:')

        # Nouveau : Utiliser Text au lieu de Entry pour self.entry_content
        self.entry_content = tk.Text(self.frame, wrap="word", height=5, width=100)

        # Nouveau : Créer une barre de défilement pour self.entry_content
        self.entry_scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.entry_content.yview)
        self.entry_content.config(yscrollcommand=self.entry_scrollbar.set)

        self.button_send_request = ttk.Button(self.frame, text='Envoyer Requête', command=self.send_request)
        self.label_result = ttk.Label(self.frame, text='Résultat:')
        self.result_text = tk.Text(self.frame, height=5, width=50, wrap="word", state=tk.DISABLED)

        # Nouveau : Créer une barre de défilement pour self.result_text
        self.scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=self.scrollbar.set)

        # Placer les widgets dans la fenêtre
        self.label_api_key.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_api_key.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_model.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
        self.combo_model.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_role.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
        self.combo_role.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_content.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
        self.entry_content.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)
        self.entry_scrollbar.grid(row=3, column=2, pady=5, sticky=tk.NS)
        self.button_send_request.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_result.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
        self.result_text.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W + tk.E + tk.N + tk.S)
        self.scrollbar.grid(row=5, column=2, pady=5, sticky=tk.NS)

        # Configurer le poids des lignes et colonnes pour le redimensionnement
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(5, weight=1)

    def send_request(self):
        # Obtenir les entrées utilisateur
        api_key = self.api_key_var.get()
        model = self.model_var.get()
        role = self.role_var.get()
        content = self.entry_content.get("1.0", tk.END).strip()

        # Créer le corps de la requête
        request_body = {
            "model": model,
            "messages": [{"role": role, "content": content}]
        }

        try:
            response = self.make_api_request(api_key, request_body)
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                self.result_var.set(content)
                self.result_text.config(state=tk.NORMAL)
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, content)
                self.result_text.config(state=tk.DISABLED)
                messagebox.showinfo('Succès', 'Requête réussie!\nContenu affiché dans la fenêtre.')
            else:
                messagebox.showerror('Erreur', 'Erreur lors de la requête. Code de statut : {}'.format(response.status_code))
        except Exception as e:
            messagebox.showerror('Erreur', 'Une erreur s\'est produite : {}'.format(str(e)))

    def make_api_request(self, api_key, request_body):
        url = 'https://api.mistral.ai/v1/chat/completions'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(api_key)
        }

        # Effectuer la requête POST
        response = requests.post(url, headers=headers, data=json.dumps(request_body))
        return response

if __name__ == "__main__":
    app = InterfaceMistral()
    app.geometry("800x600")  # Taille initiale de la fenêtre
    app.mainloop()
