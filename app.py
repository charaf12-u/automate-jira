import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
import requests
import threading
from dotenv import load_dotenv
from PIL import Image
import base64

# Charger les variables d'environnement
load_dotenv()
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

class JiraApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Jira Automate Pro")
        self.geometry("700x750")
        self.resizable(False, False)
        
        # Paths for icons
        self.asset_dir = os.path.join(os.path.dirname(__file__), "assets")
        
        # Configuration des couleurs (Premium Dark & Gold)
        self.bg_color = "#0B0F19"
        self.card_color = "#161E2E"
        self.gold_color = "#c4a15a"
        self.gold_hover = "#F2D06B"
        self.text_color = "#F8FAFC"
        self.muted_text = "#94A3B8"
        self.border_color = "#2D3748"
        self.entry_bg = "#0F172A"
        
        ctk.set_appearance_mode("dark")
        self.configure(fg_color=self.bg_color)
        
        # Charger les icônes
        self.load_icons()
        
        # Polices
        self.font_title = ctk.CTkFont(family="Segoe UI", size=32, weight="bold")
        self.font_main = ctk.CTkFont(family="Segoe UI", size=14)
        self.font_label = ctk.CTkFont(family="Segoe UI", size=14, weight="bold")
        self.font_btn = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        
        # Header Section
        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(pady=(50, 20), fill="x")
        
        # Title Image (Metallic Effect)
        if self.icon_logo:
            self.title_label = ctk.CTkLabel(self.header, text="", image=self.icon_logo)
        else:
            self.title_label = ctk.CTkLabel(self.header, text="JIRA AUTOMATE", font=self.font_title, text_color="#E2E8F0")
        self.title_label.pack()
        
        self.subtitle = ctk.CTkLabel(self.header, text="Importation intelligente vers Jira Cloud", font=self.font_main, text_color=self.muted_text)
        self.subtitle.pack()
        
        # Main Card Container (Glassmorphism look)
        self.container = ctk.CTkFrame(self, fg_color=self.card_color, corner_radius=24, border_width=1, border_color=self.border_color)
        self.container.pack(pady=10, padx=60, fill="both", expand=True)
        
        # Project Key Section
        self.key_label_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.key_label_frame.pack(anchor="w", padx=40, pady=(40, 8))
        
        self.key_icon_label = ctk.CTkLabel(self.key_label_frame, text="", image=self.icon_key)
        self.key_icon_label.pack(side="left", padx=(0, 10))
        
        self.create_label("Clé du Projet Jira", self.key_label_frame).pack(side="left")
        
        self.project_entry = self.create_entry(self.container, placeholder="ex: PROJ")
        self.project_entry.pack(padx=40, fill="x")
        if JIRA_PROJECT_KEY:
            self.project_entry.insert(0, JIRA_PROJECT_KEY)
            
        # JSON File Section
        self.file_label_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.file_label_frame.pack(anchor="w", padx=40, pady=(30, 8))
        
        self.file_icon_label = ctk.CTkLabel(self.file_label_frame, text="", image=self.icon_json)
        self.file_icon_label.pack(side="left", padx=(0, 10))
        
        self.create_label("Fichier JSON (Tasks)", self.file_label_frame).pack(side="left")
        
        self.file_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.file_frame.pack(fill="x", padx=40)
        
        self.file_entry = self.create_entry(self.file_frame, placeholder="Sélectionnez un fichier...")
        self.file_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))
        
        self.browse_btn = ctk.CTkButton(self.file_frame, text="Parcourir", width=110, height=48, 
                                        fg_color=self.gold_color, hover_color=self.gold_hover, text_color=self.bg_color,
                                        font=self.font_btn, corner_radius=12, command=self.browse_file)
        self.browse_btn.pack(side="right")
        
        # Footer Action
        self.footer = ctk.CTkFrame(self.container, fg_color="transparent")
        self.footer.pack(fill="both", expand=True, padx=40, pady=(50, 40))
        
        self.import_btn = ctk.CTkButton(self.footer, text="  LANCER L'IMPORTATION", height=60, 
                                        image=self.icon_rocket, compound="left",
                                        fg_color=self.gold_color, hover_color=self.gold_hover, text_color=self.bg_color,
                                        font=self.font_btn, corner_radius=15, command=self.start_import)
        self.import_btn.pack(fill="x", pady=(0, 25))
        
        self.status_label = ctk.CTkLabel(self.footer, text="Prêt à l'importation.", font=self.font_main, text_color=self.muted_text)
        self.status_label.pack()

    def load_icons(self):
        try:
            self.icon_key = ctk.CTkImage(light_image=Image.open(os.path.join(self.asset_dir, "key.png")),
                                         dark_image=Image.open(os.path.join(self.asset_dir, "key.png")),
                                         size=(20, 20))
            self.icon_json = ctk.CTkImage(light_image=Image.open(os.path.join(self.asset_dir, "json.png")),
                                          dark_image=Image.open(os.path.join(self.asset_dir, "json.png")),
                                          size=(20, 20))
            self.icon_rocket = ctk.CTkImage(light_image=Image.open(os.path.join(self.asset_dir, "rocket.png")),
                                            dark_image=Image.open(os.path.join(self.asset_dir, "rocket.png")),
                                            size=(24, 24))
            self.icon_logo = ctk.CTkImage(light_image=Image.open(os.path.join(self.asset_dir, "logo.png")),
                                          dark_image=Image.open(os.path.join(self.asset_dir, "logo.png")),
                                          size=(320, 64))  # Adjusted width from 400
        except Exception as e:
            print(f"Erreur chargement icônes: {e}")
            self.icon_key = None
            self.icon_json = None
            self.icon_rocket = None
            self.icon_logo = None

    def create_label(self, text, master):
        return ctk.CTkLabel(master, text=text, font=self.font_label, text_color="#E2E8F0")

    def create_entry(self, master, placeholder):
        return ctk.CTkEntry(master, placeholder_text=placeholder, height=52, font=self.font_main,
                            fg_color=self.entry_bg, border_color=self.border_color, text_color="#FFFFFF",
                            placeholder_text_color="#64748B", corner_radius=12, border_width=1)

    def browse_file(self):
        file = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file:
            self.file_entry.delete(0, 'end')
            self.file_entry.insert(0, file)

    def start_import(self):
        project = self.project_entry.get().strip()
        json_path = self.file_entry.get().strip()
        
        if not project or not json_path:
            messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
            return
            
        if not all([JIRA_DOMAIN, JIRA_EMAIL, JIRA_API_TOKEN]):
            messagebox.showerror("Configuration", "Veuillez configurer votre .env avec JIRA_DOMAIN, JIRA_EMAIL et JIRA_API_TOKEN.")
            return

        self.import_btn.configure(state="disabled", text="⏳ En cours...")
        self.status_label.configure(text="Initialisation de l'importation...", text_color=self.gold_color)
        
        threading.Thread(target=self.process_import, args=(project, json_path), daemon=True).start()

    def process_import(self, project, json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            tasks = data if isinstance(data, list) else data.get("tasks", [])
            
            auth_str = f"{JIRA_EMAIL}:{JIRA_API_TOKEN}"
            auth_b64 = base64.b64encode(auth_str.encode()).decode()
            
            headers = {
                "Authorization": f"Basic {auth_b64}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            url = f"https://{JIRA_DOMAIN}/rest/api/3/issue"
            
            count = 0
            for i, task in enumerate(tasks, 1):
                self.status_label.configure(text=f"Importation {i}/{len(tasks)} : {task.get('summary', 'Task')}...")
                
                payload = {
                    "fields": {
                        "project": {"key": project},
                        "summary": task.get("summary", task.get("title", "No Title")),
                        "description": {
                            "type": "doc",
                            "version": 1,
                            "content": [
                                {
                                    "type": "paragraph",
                                    "content": [
                                        {"type": "text", "text": task.get("description", task.get("desc", ""))}
                                    ]
                                }
                            ]
                        },
                        "issuetype": {"name": task.get("issuetype", "Task")}
                    }
                }
                
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 201:
                    count += 1
                else:
                    print(f"Error {response.status_code}: {response.text}")
            
            self.status_label.configure(text=f"✅ {count} tâches importées avec succès !", text_color="#10B981")
            messagebox.showinfo("Succès", f"{count} issues ont été créées sur Jira.")
            
        except Exception as e:
            self.status_label.configure(text="❌ Une erreur est survenue.", text_color="#EF4444")
            messagebox.showerror("Erreur", str(e))
        finally:
            self.import_btn.configure(state="normal", text="🚀 LANCER L'IMPORTATION")

if __name__ == "__main__":
    app = JiraApp()
    app.mainloop()
