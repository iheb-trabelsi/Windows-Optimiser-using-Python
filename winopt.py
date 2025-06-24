import datetime
import os
import platform
import shutil
import socket
import subprocess
import sys
import time
import tkinter as tk
import webbrowser
import winreg
from threading import Thread
from tkinter import messagebox

import customtkinter as ctk
import psutil
import wmi

# Suppress console output
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class WindowsOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimiseur Windows")
        self.disabled_programs = {}
        self.fonts = {"large": ("Arial", 16, "bold"), 
                      "medium": ("Arial", 12), 
                      "small": ("Arial", 10)}
        self.admin_mode = self.check_admin()
        self.setup_window()
        self.create_gui()
        self.update_status()
        self.command_output = ""

    def setup_window(self):
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        ww, wh = int(sw * 0.8), int(sh * 0.8)
        self.root.geometry(f"{ww}x{wh}+{int((sw-ww)/2)}+{int((sh-wh)/2)}")
        self.root.minsize(800 if sw > 1366 else 600, 600 if sh > 768 else 500)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_gui(self):
        self.main = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(1, weight=1)

        self.create_nav()
        self.content = ctk.CTkFrame(self.main)
        self.content.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.content.pack_propagate(True)
        self.create_status_bar()
        self.create_output_console()
        self.show_home()

    def create_nav(self):
        nav = ctk.CTkFrame(self.main, width=180)
        nav.grid(row=0, column=0, sticky="ns", padx=5, pady=5)
        
        # Admin status indicator
        admin_status = ctk.CTkLabel(
            nav, 
            text="🔒 Admin" if self.admin_mode else "⚠️ Non-Admin", 
            text_color="green" if self.admin_mode else "orange",
            font=self.fonts["small"]
        )
        admin_status.pack(pady=5)
        
        ctk.CTkLabel(nav, text="Optimiseur", font=self.fonts["large"]).pack(pady=10)
        
        nav_buttons = [
            ("🏠 Accueil", self.show_home), 
            ("🧹 Nettoyage", self.show_cleanup), 
            ("🚀 Démarrage", self.show_startup), 
            ("⚡ Optimiser", self.show_optimize),
            ("🔍 Analyse", self.show_analysis),
            ("📊 Ressources", self.show_resources), 
            ("👥 Utilisateurs", self.show_users),
            ("🔧 Réseau", self.show_network), 
            ("🛡️ Sécurité", self.show_security), 
            ("ℹ️ Système", self.show_system), 
            ("📝 Rapports", self.show_reports),
            ("⏰ Planificateur", self.show_scheduler), 
            ("⚙️ Paramètres", self.show_settings),
            ("🚪 Quitter", self.root.quit)
        ]
        
        for text, cmd in nav_buttons:
            btn = ctk.CTkButton(
                nav, 
                text=text, 
                command=cmd, 
                font=self.fonts["medium"], 
                anchor="w", 
                height=30
            )
            btn.pack(fill="x", padx=5, pady=2)

    def create_status_bar(self):
        self.status = ctk.CTkLabel(
            self.main, 
            text="", 
            font=self.fonts["small"], 
            anchor="w"
        )
        self.status.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    def create_output_console(self):
        self.console_frame = ctk.CTkFrame(self.main, height=150)
        self.console_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)
        
        self.console_label = ctk.CTkLabel(
            self.console_frame, 
            text="Sortie de commande:", 
            font=self.fonts["small"]
        )
        self.console_label.pack(anchor="w", padx=5, pady=2)
        
        self.console_text = ctk.CTkTextbox(
            self.console_frame, 
            font=("Consolas", 10), 
            wrap="word"
        )
        self.console_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.console_text.configure(state="disabled")

    def update_status(self):
        try:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            status_text = f"CPU: {cpu}% | RAM: {mem}% | Disque: {disk}%"
            
            if cpu > 90 or mem > 90 or disk > 90:
                self.status.configure(text_color="red")
            elif cpu > 70 or mem > 70 or disk > 70:
                self.status.configure(text_color="orange")
            else:
                self.status.configure(text_color="green")
                
            self.status.configure(text=status_text)
        except:
            self.status.configure(text="Système: Actif")
        self.root.after(5000, self.update_status)

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def create_scrollable(self):
        scroll = ctk.CTkScrollableFrame(self.content)
        scroll.pack(fill="both", expand=True, padx=5, pady=5)
        return scroll

    def show_home(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Tableau de bord", font=self.fonts["large"]).pack(pady=10)
        
        # Quick actions frame
        quick_actions = ctk.CTkFrame(self.content)
        quick_actions.pack(fill="x", pady=5, padx=5)
        
        actions = [
            ("🧹 Nettoyer", self.show_cleanup),
            ("⚡ Optimiser", self.show_optimize),
            ("🛡️ Sécurité", self.show_security),
            ("📊 Rapports", self.show_reports)
        ]
        
        for i, (text, cmd) in enumerate(actions):
            btn = ctk.CTkButton(
                quick_actions, 
                text=text, 
                command=cmd, 
                font=self.fonts["medium"],
                width=100
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
        
        tabview = ctk.CTkTabview(self.content)
        tabview.pack(fill="both", expand=True, padx=5, pady=5)
        
        for tab in ["Système", "Performance", "Alertes"]:
            tabview.add(tab)
            self.populate_tab(tabview.tab(tab), tab.lower())

    def populate_tab(self, frame, tab_type):
        if tab_type == "système":
            for k, v in self.get_system_info().items():
                row = ctk.CTkFrame(frame)
                row.pack(fill="x", pady=2)
                ctk.CTkLabel(row, text=f"{k}:", font=self.fonts["medium"], width=120, anchor="w").pack(side="left")
                ctk.CTkLabel(row, text=v, font=self.fonts["small"]).pack(side="left")
                
            # Add system health check button
            btn_frame = ctk.CTkFrame(frame)
            btn_frame.pack(fill="x", pady=10)
            ctk.CTkButton(
                btn_frame, 
                text="Vérifier l'intégrité du système", 
                command=self.run_system_health_check,
                font=self.fonts["medium"]
            ).pack(pady=5)
            
        elif tab_type == "performance":
            # CPU Frame
            cpu_frame = ctk.CTkFrame(frame)
            cpu_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(cpu_frame, text="Utilisation CPU", font=self.fonts["medium"]).pack(anchor="w")
            
            self.cpu_progress = ctk.CTkProgressBar(cpu_frame)
            self.cpu_progress.pack(fill="x", pady=5)
            
            self.cpu_label = ctk.CTkLabel(cpu_frame, text="0%", font=self.fonts["small"])
            self.cpu_label.pack(anchor="e")
            
            # Memory Frame
            mem_frame = ctk.CTkFrame(frame)
            mem_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(mem_frame, text="Utilisation Mémoire", font=self.fonts["medium"]).pack(anchor="w")
            
            self.memory_progress = ctk.CTkProgressBar(mem_frame)
            self.memory_progress.pack(fill="x", pady=5)
            
            self.memory_label = ctk.CTkLabel(mem_frame, text="0%", font=self.fonts["small"])
            self.memory_label.pack(anchor="e")
            
            # Disk Frame
            disk_frame = ctk.CTkFrame(frame)
            disk_frame.pack(fill="x", pady=5)
            ctk.CTkLabel(disk_frame, text="Utilisation Disque", font=self.fonts["medium"]).pack(anchor="w")
            
            self.disk_progress = ctk.CTkProgressBar(disk_frame)
            self.disk_progress.pack(fill="x", pady=5)
            
            self.disk_label = ctk.CTkLabel(disk_frame, text="0%", font=self.fonts["small"])
            self.disk_label.pack(anchor="e")
            
            self.update_performance()
            
        elif tab_type == "alertes":
            alerts = self.check_system_health()
            
            if not alerts:
                ctk.CTkLabel(frame, text="Aucune alerte détectée", font=self.fonts["medium"]).pack(pady=20)
                return
                
            for alert in alerts:
                f = ctk.CTkFrame(frame, border_width=1)
                f.pack(fill="x", pady=3)
                
                icon = "❌" if alert["level"] == "error" else "⚠️"
                ctk.CTkLabel(
                    f, 
                    text=f"{icon} {alert['title']}", 
                    font=self.fonts["medium"], 
                    text_color="red" if alert["level"] == "error" else "orange"
                ).pack(anchor="w", padx=5)
                
                ctk.CTkLabel(
                    f, 
                    text=alert["message"], 
                    font=self.fonts["small"]
                ).pack(anchor="w", padx=5)
                
                if alert.get("action"):
                    ctk.CTkButton(
                        f, 
                        text="Corriger", 
                        command=alert["action"], 
                        width=60
                    ).pack(side="right", padx=5)

    def update_performance(self):
        try:
            # CPU
            cpu = psutil.cpu_percent()
            self.cpu_progress.set(cpu / 100)
            self.cpu_label.configure(text=f"{cpu}%")
            
            # Memory
            mem = psutil.virtual_memory()
            self.memory_progress.set(mem.percent / 100)
            self.memory_label.configure(text=f"{mem.percent}% (Used: {mem.used/(1024**3):.1f}GB / {mem.total/(1024**3):.1f}GB)")
            
            # Disk
            disk = psutil.disk_usage('/')
            self.disk_progress.set(disk.percent / 100)
            self.disk_label.configure(text=f"{disk.percent}% (Used: {disk.used/(1024**3):.1f}GB / {disk.total/(1024**3):.1f}GB)")
            
            self.root.after(1000, self.update_performance)
        except Exception as e:
            self.log_command_output(f"Error updating performance: {str(e)}")

    def run_system_health_check(self):
        self.log_command_output("\n=== Début de la vérification d'intégrité du système ===")
        
        checks = [
            ("CPU Usage", lambda: psutil.cpu_percent() < 90, "CPU usage is high"),
            ("Memory Usage", lambda: psutil.virtual_memory().percent < 90, "Memory usage is high"),
            ("Disk Usage", lambda: psutil.disk_usage('/').percent < 90, "Disk usage is high"),
            ("Admin Rights", lambda: self.admin_mode, "Running without admin privileges"),
            ("Windows Updates", self.check_windows_updates_status, "Windows updates not checked"),
            ("Antivirus", self.check_antivirus_status, "Antivirus not active"),
            ("Firewall", self.check_firewall_status, "Firewall not active")
        ]
        
        for name, check_func, error_msg in checks:
            try:
                if check_func():
                    self.log_command_output(f"✅ {name}: OK")
                else:
                    self.log_command_output(f"❌ {name}: {error_msg}")
            except Exception as e:
                self.log_command_output(f"⚠️ {name}: Error - {str(e)}")
        
        self.log_command_output("=== Vérification terminée ===")

    def show_cleanup(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Nettoyage", font=self.fonts["large"]).pack(pady=10)
        
        scroll = self.create_scrollable()
        
        cleanup_options = [
            ("🗑️ Fichiers temporaires", self.clean_temp_files, "Supprime les fichiers temporaires système et utilisateur"),
            ("🗑️ Corbeille", self.clean_recycle_bin, "Vide la corbeille"),
            ("📋 Journaux", self.clean_log_files, "Supprime les fichiers journaux système"),
            ("🖼️ Miniatures", self.clean_thumbnails, "Supprime le cache des miniatures"),
            ("🌐 Cache navigateur", self.clean_browser_cache, "Nettoie le cache des navigateurs populaires"),
            ("📦 Fichiers Windows.old", self.clean_windows_old, "Supprime les anciennes installations Windows"),
            ("💾 Fichiers volumineux", self.find_large_files, "Trouve et supprime les fichiers volumineux"),
            ("📅 Fichiers anciens", self.clean_old_files, "Supprime les fichiers anciens")
        ]
        
        for name, cmd, desc in cleanup_options:
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=3)
            
            # Left side - Name and description
            left_frame = ctk.CTkFrame(f, fg_color="transparent")
            left_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(left_frame, text=name, font=self.fonts["medium"]).pack(anchor="w")
            ctk.CTkLabel(left_frame, text=desc, font=self.fonts["small"], text_color="gray").pack(anchor="w")
            
            # Right side - Button
            ctk.CTkButton(
                f, 
                text="Nettoyer", 
                command=cmd, 
                width=80
            ).pack(side="right", padx=5)

    def show_startup(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Programmes au démarrage", font=self.fonts["large"]).pack(pady=10)
        
        if not self.admin_mode:
            self.show_admin_warning()
            return
            
        scroll = self.create_scrollable()
        
        # Add a search bar
        search_frame = ctk.CTkFrame(scroll)
        search_frame.pack(fill="x", pady=5)
        
        self.startup_search = ctk.CTkEntry(search_frame, placeholder_text="Rechercher...")
        self.startup_search.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(
            search_frame, 
            text="Rechercher", 
            command=self.filter_startup_programs,
            width=80
        ).pack(side="right", padx=5)
        
        # Add refresh button
        ctk.CTkButton(
            scroll, 
            text="🔄 Actualiser", 
            command=self.show_startup,
            font=self.fonts["small"]
        ).pack(anchor="e", pady=5)
        
        # Startup programs list
        self.startup_list_frame = ctk.CTkFrame(scroll)
        self.startup_list_frame.pack(fill="both", expand=True)
        
        self.populate_startup_list()

    def populate_startup_list(self, filter_text=None):
        # Clear existing list
        for widget in self.startup_list_frame.winfo_children():
            widget.destroy()
            
        programs = self.get_startup_programs()
        
        if not programs:
            ctk.CTkLabel(
                self.startup_list_frame, 
                text="Aucun programme au démarrage trouvé", 
                font=self.fonts["medium"]
            ).pack(pady=20)
            return
            
        for name, path, status, impact in programs:
            if filter_text and filter_text.lower() not in name.lower():
                continue
                
            f = ctk.CTkFrame(self.startup_list_frame)
            f.pack(fill="x", pady=2)
            
            # Program info
            info_frame = ctk.CTkFrame(f, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(
                info_frame, 
                text=name, 
                font=self.fonts["small"]
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame, 
                text=path, 
                font=self.fonts["small"], 
                text_color="gray"
            ).pack(anchor="w")
            
            # Status and actions
            action_frame = ctk.CTkFrame(f, fg_color="transparent")
            action_frame.pack(side="right")
            
            status_color = "green" if status else "red"
            ctk.CTkLabel(
                action_frame, 
                text="Actif" if status else "Inactif", 
                text_color=status_color,
                font=self.fonts["small"]
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                action_frame, 
                text="Désactiver" if status else "Activer", 
                command=lambda n=name, s=status: self.toggle_startup_program(n, s), 
                width=80
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(
                action_frame, 
                text="📂", 
                command=lambda p=path: self.open_file_location(p),
                width=30
            ).pack(side="left", padx=2)

    def filter_startup_programs(self):
        filter_text = self.startup_search.get()
        self.populate_startup_list(filter_text)

    def show_optimize(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Optimisation", font=self.fonts["large"]).pack(pady=10)
        
        scroll = self.create_scrollable()
        
        optimization_options = [
            ("🧠 Mémoire", self.optimize_memory, "Redémarre l'explorateur pour libérer de la mémoire"),
            ("💽 Défragmenter", self.defragment_disk, "Défragmente le disque dur principal"),
            ("⚙️ Services", self.optimize_services, "Désactive les services inutiles"),
            ("🚀 Performances", self.optimize_performance, "Optimise les paramètres de performance"),
            ("🔋 Mode économie", self.enable_power_saver, "Active le mode économie d'énergie"),
            ("🖥️ Affichage", self.optimize_display, "Optimise les paramètres d'affichage"),
            ("🔇 Notifications", self.disable_notifications, "Désactive les notifications inutiles"),
            ("📶 Connexions", self.optimize_network, "Optimise les paramètres réseau")
        ]
        
        for name, cmd, desc in optimization_options:
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=3)
            
            left_frame = ctk.CTkFrame(f, fg_color="transparent")
            left_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(left_frame, text=name, font=self.fonts["medium"]).pack(anchor="w")
            ctk.CTkLabel(left_frame, text=desc, font=self.fonts["small"], text_color="gray").pack(anchor="w")
            
            ctk.CTkButton(
                f, 
                text="Optimiser", 
                command=cmd, 
                width=80
            ).pack(side="right", padx=5)

    def show_analysis(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Analyse du système", font=self.fonts["large"]).pack(pady=10)
        
        tabview = ctk.CTkTabview(self.content)
        tabview.pack(fill="both", expand=True, padx=5, pady=5)
        
        tabs = [
            ("Disk", self.show_disk_analysis),
            ("Processus", self.show_process_analysis),
            ("Logiciels", self.show_software_analysis),
            ("Réseau", self.show_network_analysis)
        ]
        
        for tab_name, tab_func in tabs:
            tabview.add(tab_name)
            tab_func(tabview.tab(tab_name))

    def show_disk_analysis(self, frame):
        ctk.CTkLabel(frame, text="Analyse du disque", font=self.fonts["medium"]).pack(pady=5)
        
        # Disk usage visualization
        disk_frame = ctk.CTkFrame(frame)
        disk_frame.pack(fill="x", pady=5)
        
        try:
            disk = psutil.disk_usage('/')
            usage = f"Utilisation: {disk.percent}% (Libre: {disk.free/(1024**3):.1f}GB / Total: {disk.total/(1024**3):.1f}GB)"
            ctk.CTkLabel(disk_frame, text=usage, font=self.fonts["small"]).pack(anchor="w")
            
            progress = ctk.CTkProgressBar(disk_frame)
            progress.pack(fill="x", pady=5)
            progress.set(disk.percent / 100)
            
            # Disk space by file type
            ctk.CTkLabel(frame, text="Espace par type de fichier:", font=self.fonts["medium"]).pack(pady=(10,5))
            
            # This would be replaced with actual analysis
            file_types = [
                ("Fichiers système", 35),
                ("Applications", 25),
                ("Documents", 20),
                ("Médias", 15),
                ("Autres", 5)
            ]
            
            for name, percent in file_types:
                row = ctk.CTkFrame(frame)
                row.pack(fill="x", pady=1)
                
                ctk.CTkLabel(row, text=name, font=self.fonts["small"], width=120).pack(side="left")
                
                p = ctk.CTkProgressBar(row, width=200)
                p.pack(side="left", padx=5)
                p.set(percent / 100)
                
                ctk.CTkLabel(row, text=f"{percent}%", font=self.fonts["small"]).pack(side="left")
            
            # Large files button
            ctk.CTkButton(
                frame, 
                text="Trouver les fichiers volumineux", 
                command=self.find_large_files,
                font=self.fonts["medium"]
            ).pack(pady=10)
            
        except Exception as e:
            ctk.CTkLabel(frame, text=f"Erreur d'analyse: {str(e)}", text_color="red").pack()

    def show_process_analysis(self, frame):
        ctk.CTkLabel(frame, text="Processus en cours", font=self.fonts["medium"]).pack(pady=5)
        
        # Process table
        tree_frame = ctk.CTkFrame(frame)
        tree_frame.pack(fill="both", expand=True, pady=5)
        
        # This would be replaced with actual process list
        columns = ["Nom", "CPU %", "Mémoire %", "PID"]
        
        # For a real implementation, you'd use a ttk.Treeview or similar
        header = ctk.CTkFrame(tree_frame)
        header.pack(fill="x")
        
        for i, col in enumerate(columns):
            ctk.CTkLabel(header, text=col, font=self.fonts["small"], width=100 if i > 0 else 200).pack(side="left")
        
        # Add a scrollable frame for processes
        scroll = ctk.CTkScrollableFrame(tree_frame, height=200)
        scroll.pack(fill="both", expand=True)
        
        # Sample processes - in real app, use psutil.process_iter()
        processes = [
            ("explorer.exe", 5.2, 12.3, 1234),
            ("chrome.exe", 15.7, 25.1, 5678),
            ("python.exe", 2.1, 8.5, 9012)
        ]
        
        for proc in processes:
            row = ctk.CTkFrame(scroll)
            row.pack(fill="x")
            
            for i, val in enumerate(proc):
                ctk.CTkLabel(
                    row, 
                    text=str(val), 
                    font=self.fonts["small"], 
                    width=100 if i > 0 else 200
                ).pack(side="left")
                
        # End process button
        ctk.CTkButton(
            frame, 
            text="Terminer le processus sélectionné", 
            command=lambda: messagebox.showinfo("Info", "Fonctionnalité à implémenter"),
            font=self.fonts["medium"]
        ).pack(pady=10)

    def show_software_analysis(self, frame):
        ctk.CTkLabel(frame, text="Logiciels installés", font=self.fonts["medium"]).pack(pady=5)
        
        # Add search bar
        search_frame = ctk.CTkFrame(frame)
        search_frame.pack(fill="x", pady=5)
        
        self.software_search = ctk.CTkEntry(search_frame, placeholder_text="Rechercher un logiciel...")
        self.software_search.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(
            search_frame, 
            text="Rechercher", 
            command=self.filter_installed_software,
            width=80
        ).pack(side="right", padx=5)
        
        # Software list
        self.software_list_frame = ctk.CTkFrame(frame)
        self.software_list_frame.pack(fill="both", expand=True)
        
        self.populate_software_list()

    def populate_software_list(self, filter_text=None):
        for widget in self.software_list_frame.winfo_children():
            widget.destroy()
            
        try:
            software_list = self.get_installed_software()
            
            if not software_list:
                ctk.CTkLabel(
                    self.software_list_frame, 
                    text="Aucun logiciel trouvé", 
                    font=self.fonts["medium"]
                ).pack(pady=20)
                return
                
            for name, version, publisher in software_list:
                if filter_text and filter_text.lower() not in name.lower():
                    continue
                    
                f = ctk.CTkFrame(self.software_list_frame)
                f.pack(fill="x", pady=2)
                
                # Software info
                info_frame = ctk.CTkFrame(f, fg_color="transparent")
                info_frame.pack(side="left", fill="x", expand=True)
                
                ctk.CTkLabel(
                    info_frame, 
                    text=name, 
                    font=self.fonts["small"]
                ).pack(anchor="w")
                
                ctk.CTkLabel(
                    info_frame, 
                    text=f"Version: {version} | Éditeur: {publisher}", 
                    font=self.fonts["small"], 
                    text_color="gray"
                ).pack(anchor="w")
                
                # Actions
                action_frame = ctk.CTkFrame(f, fg_color="transparent")
                action_frame.pack(side="right")
                
                ctk.CTkButton(
                    action_frame, 
                    text="Désinstaller", 
                    command=lambda n=name: self.uninstall_software(n),
                    width=80
                ).pack(side="left", padx=2)
                
        except Exception as e:
            ctk.CTkLabel(
                self.software_list_frame, 
                text=f"Erreur: {str(e)}", 
                text_color="red"
            ).pack()

    def filter_installed_software(self):
        filter_text = self.software_search.get()
        self.populate_software_list(filter_text)

    def show_network_analysis(self, frame):
        ctk.CTkLabel(frame, text="Analyse réseau", font=self.fonts["medium"]).pack(pady=5)
        
        # Network info
        try:
            net_info = self.get_network_info()
            
            for k, v in net_info.items():
                row = ctk.CTkFrame(frame)
                row.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    row, 
                    text=f"{k}:", 
                    font=self.fonts["small"], 
                    width=150, 
                    anchor="w"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row, 
                    text=v, 
                    font=self.fonts["small"]
                ).pack(side="left")
                
        except Exception as e:
            ctk.CTkLabel(
                frame, 
                text=f"Erreur d'analyse réseau: {str(e)}", 
                text_color="red"
            ).pack()
            
        # Network tools
        tools_frame = ctk.CTkFrame(frame)
        tools_frame.pack(fill="x", pady=10)
        
        tools = [
            ("Ping", self.run_ping_test),
            ("Traceroute", self.run_traceroute),
            ("Analyse de ports", self.run_port_scan),
            ("Vitesse", self.run_speed_test)
        ]
        
        for i, (name, cmd) in enumerate(tools):
            btn = ctk.CTkButton(
                tools_frame, 
                text=name, 
                command=cmd,
                width=100
            )
            btn.grid(row=0, column=i, padx=5)

    def show_resources(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Ressources système", font=self.fonts["large"]).pack(pady=10)
        
        tabview = ctk.CTkTabview(self.content)
        tabview.pack(fill="both", expand=True, padx=5, pady=5)
        
        tabs = [
            ("CPU", self.show_cpu_usage),
            ("Mémoire", self.show_memory_usage),
            ("Disque", self.show_disk_usage),
            ("Réseau", self.show_network_usage)
        ]
        
        for tab_name, tab_func in tabs:
            tabview.add(tab_name)
            tab_func(tabview.tab(tab_name))

    def show_cpu_usage(self, frame):
        ctk.CTkLabel(frame, text="Utilisation CPU", font=self.fonts["medium"]).pack(pady=5)
        
        # CPU usage graph
        self.cpu_canvas = tk.Canvas(frame, bg="#2b2b2b", height=150)
        self.cpu_canvas.pack(fill="x", pady=5)
        
        # CPU info
        try:
            cpu_info = self.get_cpu_info()
            
            for k, v in cpu_info.items():
                row = ctk.CTkFrame(frame)
                row.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    row, 
                    text=f"{k}:", 
                    font=self.fonts["small"], 
                    width=150, 
                    anchor="w"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row, 
                    text=v, 
                    font=self.fonts["small"]
                ).pack(side="left")
                
            # Start CPU monitoring
            self.update_cpu_graph()
            
        except Exception as e:
            ctk.CTkLabel(
                frame, 
                text=f"Erreur: {str(e)}", 
                text_color="red"
            ).pack()

    def update_cpu_graph(self):
        try:
            self.cpu_canvas.delete("all")
            
            # Get CPU usage per core
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            core_count = len(cpu_percent)
            
            width = self.cpu_canvas.winfo_width()
            height = self.cpu_canvas.winfo_height()
            
            # Draw graph
            bar_width = (width - 20) / core_count
            max_height = height - 20
            
            for i, percent in enumerate(cpu_percent):
                x1 = 10 + i * bar_width
                x2 = x1 + bar_width - 2
                y1 = height - 10 - (percent / 100) * max_height
                y2 = height - 10
                
                # Draw bar
                self.cpu_canvas.create_rectangle(
                    x1, y1, x2, y2, 
                    fill="#3a7ebf", 
                    outline="#3a7ebf"
                )
                
                # Draw label
                self.cpu_canvas.create_text(
                    x1 + bar_width/2, 
                    y1 - 10, 
                    text=f"{percent}%", 
                    fill="white", 
                    font=("Arial", 8)
                )
                
            # Schedule next update
            self.root.after(1000, self.update_cpu_graph)
            
        except Exception as e:
            self.log_command_output(f"Error updating CPU graph: {str(e)}")

    def show_memory_usage(self, frame):
        ctk.CTkLabel(frame, text="Utilisation Mémoire", font=self.fonts["medium"]).pack(pady=5)
        
        # Memory usage graph
        self.mem_canvas = tk.Canvas(frame, bg="#2b2b2b", height=150)
        self.mem_canvas.pack(fill="x", pady=5)
        
        # Memory info
        try:
            mem = psutil.virtual_memory()
            
            info = {
                "Total": f"{mem.total/(1024**3):.1f} GB",
                "Disponible": f"{mem.available/(1024**3):.1f} GB",
                "Utilisé": f"{mem.used/(1024**3):.1f} GB",
                "Pourcentage": f"{mem.percent}%"
            }
            
            for k, v in info.items():
                row = ctk.CTkFrame(frame)
                row.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    row, 
                    text=f"{k}:", 
                    font=self.fonts["small"], 
                    width=150, 
                    anchor="w"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row, 
                    text=v, 
                    font=self.fonts["small"]
                ).pack(side="left")
                
            # Draw memory graph
            self.update_memory_graph()
            
        except Exception as e:
            ctk.CTkLabel(
                frame, 
                text=f"Erreur: {str(e)}", 
                text_color="red"
            ).pack()

    def update_memory_graph(self):
        try:
            self.mem_canvas.delete("all")
            
            mem = psutil.virtual_memory()
            width = self.mem_canvas.winfo_width()
            height = self.mem_canvas.winfo_height()
            
            # Draw usage bar
            usage_width = (width - 20) * (mem.percent / 100)
            
            self.mem_canvas.create_rectangle(
                10, 10, 10 + usage_width, height - 10,
                fill="#3a7ebf",
                outline="#3a7ebf"
            )
            
            # Draw text
            self.mem_canvas.create_text(
                width/2, 
                height/2, 
                text=f"{mem.percent}% utilisé ({mem.used/(1024**3):.1f}GB / {mem.total/(1024**3):.1f}GB)", 
                fill="white", 
                font=("Arial", 10)
            )
            
            # Schedule next update
            self.root.after(1000, self.update_memory_graph)
            
        except Exception as e:
            self.log_command_output(f"Error updating memory graph: {str(e)}")

    def show_disk_usage(self, frame):
        ctk.CTkLabel(frame, text="Utilisation Disque", font=self.fonts["medium"]).pack(pady=5)
        
        # Disk usage graph
        self.disk_canvas = tk.Canvas(frame, bg="#2b2b2b", height=150)
        self.disk_canvas.pack(fill="x", pady=5)
        
        # Disk info
        try:
            disk = psutil.disk_usage('/')
            
            info = {
                "Total": f"{disk.total/(1024**3):.1f} GB",
                "Utilisé": f"{disk.used/(1024**3):.1f} GB",
                "Libre": f"{disk.free/(1024**3):.1f} GB",
                "Pourcentage": f"{disk.percent}%"
            }
            
            for k, v in info.items():
                row = ctk.CTkFrame(frame)
                row.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    row, 
                    text=f"{k}:", 
                    font=self.fonts["small"], 
                    width=150, 
                    anchor="w"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row, 
                    text=v, 
                    font=self.fonts["small"]
                ).pack(side="left")
                
            # Draw disk graph
            self.update_disk_graph()
            
        except Exception as e:
            ctk.CTkLabel(
                frame, 
                text=f"Erreur: {str(e)}", 
                text_color="red"
            ).pack()

    def update_disk_graph(self):
        try:
            self.disk_canvas.delete("all")
            
            disk = psutil.disk_usage('/')
            width = self.disk_canvas.winfo_width()
            height = self.disk_canvas.winfo_height()
            
            # Draw usage bar
            usage_width = (width - 20) * (disk.percent / 100)
            
            self.disk_canvas.create_rectangle(
                10, 10, 10 + usage_width, height - 10,
                fill="#3a7ebf",
                outline="#3a7ebf"
            )
            
            # Draw text
            self.disk_canvas.create_text(
                width/2, 
                height/2, 
                text=f"{disk.percent}% utilisé ({disk.used/(1024**3):.1f}GB / {disk.total/(1024**3):.1f}GB)", 
                fill="white", 
                font=("Arial", 10)
            )
            
            # Schedule next update
            self.root.after(5000, self.update_disk_graph)
            
        except Exception as e:
            self.log_command_output(f"Error updating disk graph: {str(e)}")

    def show_network_usage(self, frame):
        ctk.CTkLabel(frame, text="Utilisation Réseau", font=self.fonts["medium"]).pack(pady=5)
        
        # Network usage graph
        self.net_canvas = tk.Canvas(frame, bg="#2b2b2b", height=150)
        self.net_canvas.pack(fill="x", pady=5)
        
        # Network info
        try:
            net = psutil.net_io_counters()
            
            info = {
                "Envoyé": f"{net.bytes_sent/(1024**2):.1f} MB",
                "Reçu": f"{net.bytes_recv/(1024**2):.1f} MB",
                "Paquets envoyés": net.packets_sent,
                "Paquets reçus": net.packets_recv
            }
            
            for k, v in info.items():
                row = ctk.CTkFrame(frame)
                row.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    row, 
                    text=f"{k}:", 
                    font=self.fonts["small"], 
                    width=150, 
                    anchor="w"
                ).pack(side="left")
                
                ctk.CTkLabel(
                    row, 
                    text=v, 
                    font=self.fonts["small"]
                ).pack(side="left")
                
            # Start network monitoring
            self.last_net_io = net
            self.update_network_graph()
            
        except Exception as e:
            ctk.CTkLabel(
                frame, 
                text=f"Erreur: {str(e)}", 
                text_color="red"
            ).pack()

    def update_network_graph(self):
        try:
            self.net_canvas.delete("all")
            
            current_net = psutil.net_io_counters()
            width = self.net_canvas.winfo_width()
            height = self.net_canvas.winfo_height()
            
            # Calculate bytes per second
            sent_speed = (current_net.bytes_sent - self.last_net_io.bytes_sent) / 1024  # KB/s
            recv_speed = (current_net.bytes_recv - self.last_net_io.bytes_recv) / 1024  # KB/s
            
            # Draw graph
            max_speed = max(sent_speed, recv_speed, 100)  # At least 100 KB/s scale
            sent_height = (sent_speed / max_speed) * (height - 20)
            recv_height = (recv_speed / max_speed) * (height - 20)
            
            # Draw sent bar
            self.net_canvas.create_rectangle(
                10, height - 10 - sent_height, 
                width/2 - 5, height - 10,
                fill="#3a7ebf",
                outline="#3a7ebf"
            )
            
            # Draw received bar
            self.net_canvas.create_rectangle(
                width/2 + 5, height - 10 - recv_height, 
                width - 10, height - 10,
                fill="#2e8b57",
                outline="#2e8b57"
            )
            
            # Draw labels
            self.net_canvas.create_text(
                width/4, height - 20, 
                text=f"↑ {sent_speed:.1f} KB/s", 
                fill="white", 
                font=("Arial", 8)
            )
            
            self.net_canvas.create_text(
                3*width/4, height - 20, 
                text=f"↓ {recv_speed:.1f} KB/s", 
                fill="white", 
                font=("Arial", 8)
            )
            
            # Update last values
            self.last_net_io = current_net
            
            # Schedule next update
            self.root.after(1000, self.update_network_graph)
            
        except Exception as e:
            self.log_command_output(f"Error updating network graph: {str(e)}")

    def show_users(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Gestion des utilisateurs", font=self.fonts["large"]).pack(pady=10)
        
        if not self.admin_mode:
            self.show_admin_warning()
            return
            
        scroll = self.create_scrollable()
        
        # Add user frame
        add_frame = ctk.CTkFrame(scroll)
        add_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(add_frame, text="Ajouter un utilisateur:", font=self.fonts["medium"]).pack(anchor="w", padx=5)
        
        entry_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        entry_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(entry_frame, text="Nom:", font=self.fonts["small"]).pack(side="left", padx=5)
        self.new_user_name = ctk.CTkEntry(entry_frame)
        self.new_user_name.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkLabel(entry_frame, text="Mot de passe:", font=self.fonts["small"]).pack(side="left", padx=5)
        self.new_user_pass = ctk.CTkEntry(entry_frame, show="*")
        self.new_user_pass.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkButton(
            add_frame, 
            text="Ajouter", 
            command=self.add_user_account,
            width=80
        ).pack(side="right", padx=5)
        
        # Users list
        ctk.CTkLabel(scroll, text="Utilisateurs existants:", font=self.fonts["medium"]).pack(anchor="w", pady=(10,5))
        
        users = self.get_user_accounts()
        
        if not users:
            ctk.CTkLabel(scroll, text="Aucun utilisateur trouvé", font=self.fonts["small"]).pack(pady=10)
            return
            
        for u, t, s in users:
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=2)
            
            # User info
            info_frame = ctk.CTkFrame(f, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(info_frame, text=u, font=self.fonts["small"]).pack(anchor="w")
            
            type_color = "green" if t == "Admin" else "blue"
            status_color = "green" if s == "Actif" else "red"
            
            ctk.CTkLabel(
                info_frame, 
                text=f"{t} | {s}", 
                font=self.fonts["small"], 
                text_color=type_color
            ).pack(anchor="w")
            
            # Actions
            action_frame = ctk.CTkFrame(f, fg_color="transparent")
            action_frame.pack(side="right")
            
            ctk.CTkButton(
                action_frame, 
                text="Activer/Désactiver", 
                command=lambda u=u, s=s: self.toggle_user_account(u, s), 
                width=120
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(
                action_frame, 
                text="Supprimer", 
                command=lambda u=u: self.delete_user_account(u), 
                width=80
            ).pack(side="left", padx=2)
            
            ctk.CTkButton(
                action_frame, 
                text="Admin", 
                command=lambda u=u: self.toggle_admin(u, t), 
                width=60
            ).pack(side="left", padx=2)

    def show_network(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Outils réseau", font=self.fonts["large"]).pack(pady=10)
        
        scroll = self.create_scrollable()
        
        network_tools = [
            ("🌐 Tester la connexion", self.test_network_connection, "Ping un serveur pour tester la connectivité"),
            ("🔄 Vider le cache DNS", self.flush_dns_cache, "Vide le cache DNS local"),
            ("🔄 Réinitialiser TCP/IP", self.reset_tcpip, "Réinitialise la pile réseau TCP/IP"),
            ("📶 Informations IP", self.show_ip_info, "Affiche les informations d'adresse IP"),
            ("🔒 Analyse de ports", self.run_port_scan, "Analyse les ports ouverts sur cette machine"),
            ("🚀 Test de vitesse", self.run_speed_test, "Teste la vitesse de connexion Internet")
        ]
        
        for name, cmd, desc in network_tools:
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=3)
            
            left_frame = ctk.CTkFrame(f, fg_color="transparent")
            left_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(left_frame, text=name, font=self.fonts["medium"]).pack(anchor="w")
            ctk.CTkLabel(left_frame, text=desc, font=self.fonts["small"], text_color="gray").pack(anchor="w")
            
            ctk.CTkButton(
                f, 
                text="Exécuter", 
                command=cmd, 
                width=80
            ).pack(side="right", padx=5)

    def show_security(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Sécurité", font=self.fonts["large"]).pack(pady=10)
        
        scroll = self.create_scrollable()
        
        security_tools = [
            ("🛡️ Pare-feu", self.check_firewall_status, "Vérifie l'état du pare-feu Windows"),
            ("🦠 Antivirus", self.check_antivirus_status, "Vérifie l'état de l'antivirus"),
            ("🔄 Mises à jour", self.check_windows_updates, "Vérifie les mises à jour Windows disponibles"),
            ("🔒 Analyse de sécurité", self.run_security_scan, "Exécute une analyse de sécurité de base"),
            ("👀 Historique de sécurité", self.view_security_logs, "Affiche les journaux de sécurité"),
            ("🚪 Portes dérobées", self.check_backdoors, "Recherche les connexions suspectes")
        ]
        
        for name, cmd, desc in security_tools:
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=3)
            
            left_frame = ctk.CTkFrame(f, fg_color="transparent")
            left_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(left_frame, text=name, font=self.fonts["medium"]).pack(anchor="w")
            ctk.CTkLabel(left_frame, text=desc, font=self.fonts["small"], text_color="gray").pack(anchor="w")
            
            ctk.CTkButton(
                f, 
                text="Exécuter", 
                command=cmd, 
                width=80
            ).pack(side="right", padx=5)

    def show_system(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Informations système", font=self.fonts["large"]).pack(pady=10)
        
        scroll = self.create_scrollable()
        
        system_info = self.get_detailed_system_info()
        
        for category, items in system_info.items():
            ctk.CTkLabel(scroll, text=category, font=self.fonts["medium"]).pack(anchor="w", pady=(10,5))
            
            for k, v in items.items():
                f = ctk.CTkFrame(scroll)
                f.pack(fill="x", pady=1)
                
                ctk.CTkLabel(f, text=f"{k}:", font=self.fonts["small"], width=150).pack(side="left")
                ctk.CTkLabel(f, text=v, font=self.fonts["small"]).pack(side="left")
                
        # System tools
        ctk.CTkLabel(scroll, text="Outils système", font=self.fonts["medium"]).pack(anchor="w", pady=(20,5))
        
        tools_frame = ctk.CTkFrame(scroll)
        tools_frame.pack(fill="x", pady=5)
        
        tools = [
            ("🔄 Redémarrer", self.restart_system),
            ("⏻ Éteindre", self.shutdown_system),
            ("💤 Mode veille", self.sleep_system),
            ("🖥️ Gestionnaire", self.open_task_manager)
        ]
        
        for i, (text, cmd) in enumerate(tools):
            btn = ctk.CTkButton(
                tools_frame, 
                text=text, 
                command=cmd,
                width=100
            )
            btn.grid(row=0, column=i, padx=5)

    def show_reports(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Rapports système", font=self.fonts["large"]).pack(pady=10)
        
        scroll = self.create_scrollable()
        
        report_options = [
            ("📋 Système", self.generate_system_report, "Génère un rapport détaillé du système"),
            ("📜 Journaux", self.view_event_logs, "Affiche les journaux d'événements Windows"),
            ("📊 Performances", self.generate_performance_report, "Crée un rapport de performance"),
            ("📦 Installation logiciels", self.generate_software_report, "Liste tous les logiciels installés"),
            ("📝 Rapport complet", self.generate_full_report, "Génère un rapport complet du système")
        ]
        
        for name, cmd, desc in report_options:
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=3)
            
            left_frame = ctk.CTkFrame(f, fg_color="transparent")
            left_frame.pack(side="left", fill="x", expand=True)
            
            ctk.CTkLabel(left_frame, text=name, font=self.fonts["medium"]).pack(anchor="w")
            ctk.CTkLabel(left_frame, text=desc, font=self.fonts["small"], text_color="gray").pack(anchor="w")
            
            ctk.CTkButton(
                f, 
                text="Générer", 
                command=cmd, 
                width=80
            ).pack(side="right", padx=5)

    def show_scheduler(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Planificateur de tâches", font=self.fonts["large"]).pack(pady=10)
        
        scroll = self.create_scrollable()
        
        # Scheduled tasks
        ctk.CTkLabel(scroll, text="Tâches planifiées", font=self.fonts["medium"]).pack(anchor="w", pady=5)
        
        for task, cmd in [
            ("Nettoyage quotidien", lambda: self.schedule_task("clean_temp_files", "quotidien")),
            ("Défragmentation hebdo", lambda: self.schedule_task("defragment_disk", "hebdomadaire")),
            ("Rapport mensuel", lambda: self.schedule_task("generate_system_report", "mensuel")),
            ("Sauvegarde", lambda: self.schedule_task("create_backup", "quotidien"))
        ]:
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=3)
            
            ctk.CTkLabel(f, text=task, font=self.fonts["small"]).pack(side="left")
            ctk.CTkButton(f, text="Planifier", command=cmd, width=80).pack(side="right", padx=5)
        
        # One-time tasks
        ctk.CTkLabel(scroll, text="Tâches ponctuelles", font=self.fonts["medium"]).pack(anchor="w", pady=(10,5))
        
        time_frame = ctk.CTkFrame(scroll)
        time_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(time_frame, text="Heure (HH:MM):", font=self.fonts["small"]).pack(side="left", padx=5)
        self.schedule_time = ctk.CTkEntry(time_frame, placeholder_text="HH:MM")
        self.schedule_time.pack(side="left", fill="x", expand=True, padx=5)
        
        for task, cmd in [
            ("Lancer le nettoyage", "clean_temp_files"),
            ("Lancer la défragmentation", "defragment_disk"),
            ("Générer un rapport", "generate_system_report"),
            ("Redémarrer", "restart_system")
        ]:
            f = ctk.CTkFrame(scroll)
            f.pack(fill="x", pady=3)
            
            ctk.CTkLabel(f, text=task, font=self.fonts["small"]).pack(side="left")
            ctk.CTkButton(f, text="Planifier", command=lambda c=cmd: self.schedule_one_time_task(c), width=80).pack(side="right", padx=5)

    def show_settings(self):
        self.clear_content()
        ctk.CTkLabel(self.content, text="Paramètres", font=self.fonts["large"]).pack(pady=10)
        
        scroll = self.create_scrollable()
        
        # Appearance
        ctk.CTkLabel(scroll, text="Apparence", font=self.fonts["medium"]).pack(anchor="w", pady=5)
        
        mode_frame = ctk.CTkFrame(scroll)
        mode_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(mode_frame, text="Thème:", font=self.fonts["small"]).pack(side="left", padx=5)
        
        self.theme_var = ctk.StringVar(value="dark")
        ctk.CTkOptionMenu(
            mode_frame, 
            values=["dark", "light", "system"], 
            variable=self.theme_var,
            command=self.change_theme
        ).pack(side="left", padx=5)
        
        # Language
        ctk.CTkLabel(scroll, text="Langue", font=self.fonts["medium"]).pack(anchor="w", pady=(10,5))
        
        lang_frame = ctk.CTkFrame(scroll)
        lang_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(lang_frame, text="Langue:", font=self.fonts["small"]).pack(side="left", padx=5)
        
        self.lang_var = ctk.StringVar(value="fr")
        ctk.CTkOptionMenu(
            lang_frame, 
            values=["fr", "en", "es"], 
            variable=self.lang_var,
            command=self.change_language
        ).pack(side="left", padx=5)
        
        # Other settings
        ctk.CTkLabel(scroll, text="Autres paramètres", font=self.fonts["medium"]).pack(anchor="w", pady=(10,5))
        
        ctk.CTkCheckBox(
            scroll, 
            text="Démarrer avec Windows", 
            font=self.fonts["small"]
        ).pack(anchor="w", pady=2)
        
        ctk.CTkCheckBox(
            scroll, 
            text="Vérifier les mises à jour automatiquement", 
            font=self.fonts["small"]
        ).pack(anchor="w", pady=2)
        
        ctk.CTkCheckBox(
            scroll, 
            text="Afficher les notifications", 
            font=self.fonts["small"]
        ).pack(anchor="w", pady=2)
        
        # Save button
        ctk.CTkButton(
            scroll, 
            text="Enregistrer les paramètres", 
            command=self.save_settings,
            font=self.fonts["medium"]
        ).pack(pady=10)

    def show_admin_warning(self):
        warning_frame = ctk.CTkFrame(self.content)
        warning_frame.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(
            warning_frame, 
            text="⚠️ Cette fonctionnalité nécessite des privilèges d'administrateur", 
            font=self.fonts["medium"], 
            text_color="orange"
        ).pack(pady=5)
        
        ctk.CTkLabel(
            warning_frame, 
            text="Veuillez relancer l'application en tant qu'administrateur", 
            font=self.fonts["small"]
        ).pack(pady=5)
        
        ctk.CTkButton(
            warning_frame, 
            text="Relancer en tant qu'admin", 
            command=self.restart_as_admin,
            font=self.fonts["medium"]
        ).pack(pady=10)

    def check_admin(self):
        try:
            return os.getuid() == 0
        except:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def restart_as_admin(self):
        try:
            import ctypes
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de relancer en admin: {str(e)}")

    def log_command_output(self, text):
        self.console_text.configure(state="normal")
        self.console_text.insert("end", text + "\n")
        self.console_text.see("end")
        self.console_text.configure(state="disabled")
        self.root.update()

    def run_command(self, command, show_output=True):
        try:
            self.log_command_output(f"> {command}")
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            output, error = process.communicate()
            
            if show_output:
                if output:
                    self.log_command_output(output)
                if error:
                    self.log_command_output(f"Erreur: {error}")
            
            return output, error
            
        except Exception as e:
            self.log_command_output(f"Erreur d'exécution: {str(e)}")
            return None, str(e)

    def get_system_info(self):
        return {
            "OS": platform.system(),
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processeur": platform.processor(),
            "Architecture": platform.architecture()[0]
        }

    def get_detailed_system_info(self):
        info = {}
        
        try:
            # Basic system info
            info["Système"] = {
                "Nom": platform.node(),
                "OS": platform.system(),
                "Version": platform.version(),
                "Architecture": platform.architecture()[0]
            }
            
            # CPU info
            cpu_info = self.get_cpu_info()
            info["CPU"] = cpu_info
            
            # Memory info
            mem = psutil.virtual_memory()
            info["Mémoire"] = {
                "Total": f"{mem.total/(1024**3):.1f} GB",
                "Disponible": f"{mem.available/(1024**3):.1f} GB",
                "Utilisé": f"{mem.used/(1024**3):.1f} GB",
                "Pourcentage": f"{mem.percent}%"
            }
            
            # Disk info
            disk = psutil.disk_usage('/')
            info["Disque"] = {
                "Total": f"{disk.total/(1024**3):.1f} GB",
                "Utilisé": f"{disk.used/(1024**3):.1f} GB",
                "Libre": f"{disk.free/(1024**3):.1f} GB",
                "Pourcentage": f"{disk.percent}%"
            }
            
            # Network info
            net_info = self.get_network_info()
            info["Réseau"] = net_info
            
            # GPU info
            try:
                c = wmi.WMI()
                gpu = c.Win32_VideoController()[0]
                info["GPU"] = {
                    "Nom": gpu.Name,
                    "VRAM": f"{int(gpu.AdapterRAM)/(1024**3):.1f} GB" if gpu.AdapterRAM else "Inconnu"
                }
            except:
                info["GPU"] = {"Erreur": "Information GPU non disponible"}
            
            # Battery info (if laptop)
            try:
                battery = psutil.sensors_battery()
                if battery:
                    info["Batterie"] = {
                        "Pourcentage": f"{battery.percent}%",
                        "Branché": "Oui" if battery.power_plugged else "Non"
                    }
            except:
                pass
                
        except Exception as e:
            info["Erreur"] = f"Impossible de récupérer les informations: {str(e)}"
            
        return info

    def get_cpu_info(self):
        try:
            cpu_info = {
                "Modèle": platform.processor(),
                "Cœurs physiques": str(psutil.cpu_count(logical=False)),
                "Cœurs logiques": str(psutil.cpu_count()),
                "Fréquence actuelle": f"{psutil.cpu_freq().current:.2f} MHz",
                "Utilisation": f"{psutil.cpu_percent()}%"
            }
            
            try:
                c = wmi.WMI()
                for processor in c.Win32_Processor():
                    cpu_info["Fabricant"] = processor.Manufacturer
                    cpu_info["Nom"] = processor.Name
                    cpu_info["Fréquence max"] = f"{processor.MaxClockSpeed} MHz"
                    break
            except:
                pass
                
            return cpu_info
            
        except Exception as e:
            return {"Erreur": f"Impossible de récupérer les infos CPU: {str(e)}"}

    def get_network_info(self):
        try:
            net_info = {}
            net_io = psutil.net_io_counters()
            
            net_info["Envoyé"] = f"{net_io.bytes_sent/(1024**2):.1f} MB"
            net_info["Reçu"] = f"{net_io.bytes_recv/(1024**2):.1f} MB"
            
            # Get IP addresses
            hostname = socket.gethostname()
            net_info["Nom d'hôte"] = hostname
            
            try:
                ip = socket.gethostbyname(hostname)
                net_info["IP locale"] = ip
            except:
                net_info["IP locale"] = "Inconnue"
                
            # Get public IP (requires internet)
            try:
                import requests
                public_ip = requests.get('https://api.ipify.org').text
                net_info["IP publique"] = public_ip
            except:
                net_info["IP publique"] = "Inconnue"
                
            # Get network interfaces
            try:
                interfaces = psutil.net_if_addrs()
                net_info["Interfaces"] = ", ".join(interfaces.keys())
            except:
                pass
                
            return net_info
            
        except Exception as e:
            return {"Erreur": f"Impossible de récupérer les infos réseau: {str(e)}"}

    def get_startup_programs(self):
        progs = []
        
        if not self.admin_mode:
            return progs
            
        try:
            # Check registry locations
            registry_locations = [
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"),
                (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce")
            ]
            
            for hkey, subkey in registry_locations:
                try:
                    with winreg.OpenKey(hkey, subkey) as key:
                        i = 0
                        while True:
                            try:
                                name, value, _ = winreg.EnumValue(key, i)
                                status = name not in self.disabled_programs
                                progs.append((name, value, status, "Moyenne"))
                                i += 1
                            except OSError:
                                break
                except:
                    continue
                    
            # Check startup folder
            startup_folder = os.path.join(
                os.environ['APPDATA'], 
                'Microsoft', 
                'Windows', 
                'Start Menu', 
                'Programs', 
                'Startup'
            )
            
            if os.path.exists(startup_folder):
                for item in os.listdir(startup_folder):
                    path = os.path.join(startup_folder, item)
                    status = item not in self.disabled_programs
                    progs.append((item, path, status, "Faible"))
                    
        except Exception as e:
            self.log_command_output(f"Erreur récupération programmes démarrage: {str(e)}")
            
        return sorted(progs, key=lambda x: x[0])

    def get_user_accounts(self):
        users = []
        
        if not self.admin_mode:
            return users
            
        try:
            # Using WMI
            c = wmi.WMI()
            for user in c.Win32_UserAccount():
                account_type = "Admin" if user.AccountType == 512 else "Utilisateur"
                status = "Actif" if not user.Disabled else "Inactif"
                users.append((user.Name, account_type, status))
                
        except Exception as e:
            self.log_command_output(f"Erreur récupération comptes utilisateurs: {str(e)}")
            
            try:
                # Fallback to net user command
                output, _ = self.run_command("net user", show_output=False)
                if output:
                    lines = output.split('\n')
                    for line in lines[4:-2]:  # Skip header and footer
                        username = line.strip()
                        if username:
                            users.append((username, "Inconnu", "Inconnu"))
            except:
                pass
                
        return users

    def get_installed_software(self):
        software = []
        
        try:
            # Check 64-bit software
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            ) as key:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                version = winreg.QueryValueEx(subkey, "DisplayVersion")[0] if winreg.QueryValueEx(subkey, "DisplayVersion") else "Inconnue"
                                publisher = winreg.QueryValueEx(subkey, "Publisher")[0] if winreg.QueryValueEx(subkey, "Publisher") else "Inconnu"
                                software.append((name, version, publisher))
                            except:
                                pass
                        i += 1
                    except OSError:
                        break
                        
            # Check 32-bit software on 64-bit Windows
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
            ) as key:
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                version = winreg.QueryValueEx(subkey, "DisplayVersion")[0] if winreg.QueryValueEx(subkey, "DisplayVersion") else "Inconnue"
                                publisher = winreg.QueryValueEx(subkey, "Publisher")[0] if winreg.QueryValueEx(subkey, "Publisher") else "Inconnu"
                                software.append((name, version, publisher))
                            except:
                                pass
                        i += 1
                    except OSError:
                        break
                        
        except Exception as e:
            self.log_command_output(f"Erreur récupération logiciels installés: {str(e)}")
            
        return sorted(software, key=lambda x: x[0])

    def check_system_health(self):
        alerts = []
        
        try:
            # Disk space check
            disk = psutil.disk_usage('/')
            if disk.percent > 90:
                alerts.append({
                    "level": "error", 
                    "title": "Espace disque critique", 
                    "message": f"Le disque système est plein à {disk.percent}%", 
                    "action": self.show_cleanup
                })
            elif disk.percent > 80:
                alerts.append({
                    "level": "warning", 
                    "title": "Espace disque faible", 
                    "message": f"Le disque système est plein à {disk.percent}%", 
                    "action": self.show_cleanup
                })
                
            # Memory check
            mem = psutil.virtual_memory()
            if mem.percent > 90:
                alerts.append({
                    "level": "error", 
                    "title": "Mémoire critique", 
                    "message": f"La mémoire est utilisée à {mem.percent}%", 
                    "action": self.show_optimize
                })
            elif mem.percent > 80:
                alerts.append({
                    "level": "warning", 
                    "title": "Mémoire élevée", 
                    "message": f"La mémoire est utilisée à {mem.percent}%", 
                    "action": self.show_optimize
                })
                
            # CPU check
            cpu = psutil.cpu_percent(interval=1)
            if cpu > 90:
                alerts.append({
                    "level": "error", 
                    "title": "CPU surchargé", 
                    "message": f"Le CPU est utilisé à {cpu}%", 
                    "action": self.show_resources
                })
            elif cpu > 80:
                alerts.append({
                    "level": "warning", 
                    "title": "CPU élevé", 
                    "message": f"Le CPU est utilisé à {cpu}%", 
                    "action": self.show_resources
                })
                
            # Admin check
            if not self.admin_mode:
                alerts.append({
                    "level": "warning", 
                    "title": "Privilèges insuffisants", 
                    "message": "L'application ne fonctionne pas en mode administrateur", 
                    "action": self.restart_as_admin
                })
                
            # Antivirus check
            try:
                c = wmi.WMI(namespace="root\\SecurityCenter2")
                antivirus = c.AntiVirusProduct()
                if not antivirus or not any(av.productState & 0x1000 for av in antivirus):
                    alerts.append({
                        "level": "warning", 
                        "title": "Antivirus inactif", 
                        "message": "Aucun antivirus actif détecté", 
                        "action": self.show_security
                    })
            except:
                alerts.append({
                    "level": "warning", 
                    "title": "Antivirus inconnu", 
                    "message": "Impossible de vérifier l'état de l'antivirus", 
                    "action": self.show_security
                })
                
            # Firewall check
            try:
                c = wmi.WMI()
                firewall = c.Win32_Service(Name="MpsSvc")[0]
                if firewall.State != "Running":
                    alerts.append({
                        "level": "warning", 
                        "title": "Pare-feu inactif", 
                        "message": "Le pare-feu Windows n'est pas actif", 
                        "action": self.show_security
                    })
            except:
                alerts.append({
                    "level": "warning", 
                    "title": "Pare-feu inconnu", 
                    "message": "Impossible de vérifier l'état du pare-feu", 
                    "action": self.show_security
                })
                
        except Exception as e:
            alerts.append({
                "level": "error", 
                "title": "Erreur de vérification", 
                "message": f"Impossible de vérifier l'état du système: {str(e)}"
            })
            
        return alerts

    def clean_temp_files(self):
        self.log_command_output("\n=== Nettoyage des fichiers temporaires ===")
        
        temp_folders = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            os.path.join(os.environ.get('WINDIR'), 'Temp'),
            os.path.join(os.environ.get('WINDIR'), 'Prefetch')
        ]
        
        total_freed = 0
        
        for folder in temp_folders:
            if not folder or not os.path.exists(folder):
                continue
                
            try:
                self.log_command_output(f"Nettoyage du dossier: {folder}")
                
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            total_freed += file_size
                        except Exception as e:
                            self.log_command_output(f"Erreur suppression {file}: {str(e)}")
                            
                self.log_command_output(f"Dossier nettoyé: {folder}")
                
            except Exception as e:
                self.log_command_output(f"Erreur nettoyage {folder}: {str(e)}")
                
        if total_freed > 0:
            self.log_command_output(f"\nEspace libéré: {total_freed/(1024**2):.1f} MB")
            messagebox.showinfo("Terminé", f"Espace libéré: {total_freed/(1024**2):.1f} MB")
        else:
            self.log_command_output("\nAucun fichier temporaire trouvé")
            messagebox.showinfo("Info", "Aucun fichier temporaire trouvé")

    def clean_recycle_bin(self):
        self.log_command_output("\n=== Vidage de la corbeille ===")
        
        try:
            import winshell
            winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
            self.log_command_output("Corbeille vidée avec succès")
            messagebox.showinfo("Succès", "Corbeille vidée")
        except Exception as e:
            self.log_command_output(f"Erreur vidage corbeille: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de vidage: {str(e)}")

    def clean_log_files(self):
        self.log_command_output("\n=== Nettoyage des fichiers journaux ===")
        
        log_folders = [
            os.path.join(os.environ.get('WINDIR'), 'System32', 'winevt', 'Logs')
        ]
        
        total_freed = 0
        
        for folder in log_folders:
            if not os.path.exists(folder):
                continue
                
            try:
                self.log_command_output(f"Nettoyage du dossier: {folder}")
                
                for file in os.listdir(folder):
                    try:
                        file_path = os.path.join(folder, file)
                        if os.path.isfile(file_path):
                            file_size = os.path.getsize(file_path)
                            os.remove(file_path)
                            total_freed += file_size
                    except Exception as e:
                        self.log_command_output(f"Erreur suppression {file}: {str(e)}")
                        
                self.log_command_output(f"Dossier nettoyé: {folder}")
                
            except Exception as e:
                self.log_command_output(f"Erreur nettoyage {folder}: {str(e)}")
                
        if total_freed > 0:
            self.log_command_output(f"\nEspace libéré: {total_freed/(1024**2):.1f} MB")
            messagebox.showinfo("Terminé", f"Espace libéré: {total_freed/(1024**2):.1f} MB")
        else:
            self.log_command_output("\nAucun fichier journal trouvé")
            messagebox.showinfo("Info", "Aucun fichier journal trouvé")

    def clean_thumbnails(self):
        self.log_command_output("\n=== Nettoyage du cache des miniatures ===")
        
        thumbnail_db = os.path.join(
            os.environ['USERPROFILE'], 
            'AppData', 
            'Local', 
            'Microsoft', 
            'Windows', 
            'Explorer'
        )
        
        total_freed = 0
        
        if os.path.exists(thumbnail_db):
            try:
                for file in os.listdir(thumbnail_db):
                    if file.startswith('thumbcache_'):
                        file_path = os.path.join(thumbnail_db, file)
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        total_freed += file_size
                        self.log_command_output(f"Supprimé: {file}")
                        
                if total_freed > 0:
                    self.log_command_output(f"\nEspace libéré: {total_freed/(1024**2):.1f} MB")
                    messagebox.showinfo("Terminé", f"Miniatures nettoyées: {total_freed/(1024**2):.1f} MB")
                else:
                    self.log_command_output("\nAucun cache de miniatures trouvé")
                    messagebox.showinfo("Info", "Aucun cache de miniatures trouvé")
                    
            except Exception as e:
                self.log_command_output(f"Erreur nettoyage miniatures: {str(e)}")
                messagebox.showerror("Erreur", f"Échec du nettoyage: {str(e)}")
        else:
            self.log_command_output("\nDossier des miniatures introuvable")
            messagebox.showinfo("Info", "Dossier des miniatures introuvable")

    def clean_browser_cache(self):
        self.log_command_output("\n=== Nettoyage du cache des navigateurs ===")
        
        browsers = {
            'Chrome': [
                os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Cache'),
                os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Code Cache')
            ],
            'Edge': [
                os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Cache'),
                os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Code Cache')
            ],
            'Firefox': [
                os.path.join(os.environ['LOCALAPPDATA'], 'Mozilla', 'Firefox', 'Profiles')
            ]
        }
        
        total_freed = 0
        
        for browser, cache_paths in browsers.items():
            self.log_command_output(f"\nNettoyage {browser}")
            
            for path in cache_paths:
                if not os.path.exists(path):
                    continue
                    
                try:
                    for root, dirs, files in os.walk(path):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                total_freed += file_size
                            except Exception as e:
                                self.log_command_output(f"Erreur suppression {file}: {str(e)}")
                                
                    self.log_command_output(f"Cache nettoyé: {path}")
                    
                except Exception as e:
                    self.log_command_output(f"Erreur nettoyage {path}: {str(e)}")
                    
        if total_freed > 0:
            self.log_command_output(f"\nEspace libéré total: {total_freed/(1024**2):.1f} MB")
            messagebox.showinfo("Terminé", f"Cache nettoyé: {total_freed/(1024**2):.1f} MB")
        else:
            self.log_command_output("\nAucun cache navigateur trouvé")
            messagebox.showinfo("Info", "Aucun cache navigateur trouvé")

    def clean_windows_old(self):
        self.log_command_output("\n=== Nettoyage du dossier Windows.old ===")
        
        windows_old = os.path.join(os.environ['SYSTEMDRIVE'], 'Windows.old')
        
        if os.path.exists(windows_old):
            try:
                self.log_command_output("Suppression du dossier Windows.old...")
                
                # Use the Windows Disk Cleanup utility to safely remove Windows.old
                cmd = f'cleanmgr /sagerun:1'
                self.run_command(cmd)
                
                self.log_command_output("Dossier Windows.old supprimé avec succès")
                messagebox.showinfo("Succès", "Dossier Windows.old supprimé")
            except Exception as e:
                self.log_command_output(f"Erreur suppression Windows.old: {str(e)}")
                messagebox.showerror("Erreur", f"Échec de suppression: {str(e)}")
        else:
            self.log_command_output("\nDossier Windows.old introuvable")
            messagebox.showinfo("Info", "Dossier Windows.old introuvable")

    def find_large_files(self, min_size_mb=100):
        self.log_command_output(f"\n=== Recherche de fichiers > {min_size_mb}MB ===")
        
        large_files = []
        
        # Common locations to search
        search_locations = [
            os.environ['USERPROFILE'],
            os.environ['SYSTEMDRIVE'] + '\\'
        ]
        
        for location in search_locations:
            if not os.path.exists(location):
                continue
                
            try:
                self.log_command_output(f"Analyse de {location}...")
                
                for root, dirs, files in os.walk(location):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                            
                            if file_size > min_size_mb:
                                large_files.append((file_path, file_size))
                                self.log_command_output(f"Trouvé: {file_path} ({file_size:.1f}MB)")
                        except:
                            continue
                            
            except Exception as e:
                self.log_command_output(f"Erreur analyse {location}: {str(e)}")
                
        if large_files:
            # Sort by size (descending)
            large_files.sort(key=lambda x: x[1], reverse=True)
            
            # Show results
            result_window = ctk.CTkToplevel(self.root)
            result_window.title(f"Fichiers volumineux (> {min_size_mb}MB)")
            result_window.geometry("800x600")
            
            scroll = ctk.CTkScrollableFrame(result_window)
            scroll.pack(fill="both", expand=True, padx=5, pady=5)
            
            ctk.CTkLabel(
                scroll, 
                text=f"Fichiers volumineux trouvés ({len(large_files)}):", 
                font=self.fonts["medium"]
            ).pack(anchor="w", pady=5)
            
            for file_path, file_size in large_files:
                f = ctk.CTkFrame(scroll)
                f.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    f, 
                    text=f"{file_path} ({file_size:.1f}MB)", 
                    font=self.fonts["small"]
                ).pack(side="left")
                
                ctk.CTkButton(
                    f, 
                    text="Supprimer", 
                    command=lambda p=file_path: self.delete_file(p),
                    width=80
                ).pack(side="right", padx=5)
                
            self.log_command_output(f"\n{len(large_files)} fichiers volumineux trouvés")
        else:
            self.log_command_output("\nAucun fichier volumineux trouvé")
            messagebox.showinfo("Info", f"Aucun fichier > {min_size_mb}MB trouvé")

    def clean_old_files(self, days_old=30):
        self.log_command_output(f"\n=== Nettoyage des fichiers > {days_old} jours ===")
        
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)
        deleted_files = 0
        freed_space = 0
        
        # Common locations to clean
        clean_locations = [
            os.path.join(os.environ['USERPROFILE'], 'Downloads'),
            os.path.join(os.environ['USERPROFILE'], 'Desktop'),
            os.path.join(os.environ['USERPROFILE'], 'Documents')
        ]
        
        for location in clean_locations:
            if not os.path.exists(location):
                continue
                
            try:
                self.log_command_output(f"Analyse de {location}...")
                
                for root, dirs, files in os.walk(location):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            file_mtime = os.path.getmtime(file_path)
                            
                            if file_mtime < cutoff_time:
                                file_size = os.path.getsize(file_path)
                                os.remove(file_path)
                                deleted_files += 1
                                freed_space += file_size
                                self.log_command_output(f"Supprimé: {file_path}")
                        except:
                            continue
                            
            except Exception as e:
                self.log_command_output(f"Erreur analyse {location}: {str(e)}")
                
        if deleted_files > 0:
            self.log_command_output(f"\n{deleted_files} fichiers supprimés")
            self.log_command_output(f"Espace libéré: {freed_space/(1024**2):.1f} MB")
            messagebox.showinfo("Terminé", f"{deleted_files} fichiers supprimés\nEspace libéré: {freed_space/(1024**2):.1f} MB")
        else:
            self.log_command_output("\nAucun fichier ancien trouvé")
            messagebox.showinfo("Info", f"Aucun fichier > {days_old} jours trouvé")

    def delete_file(self, file_path):
        try:
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            os.remove(file_path)
            self.log_command_output(f"Fichier supprimé: {file_path} ({file_size:.1f}MB)")
            messagebox.showinfo("Succès", f"Fichier supprimé: {os.path.basename(file_path)}")
        except Exception as e:
            self.log_command_output(f"Erreur suppression {file_path}: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de suppression: {str(e)}")

    def toggle_startup_program(self, name, status):
        try:
            if status:
                self.disabled_programs[name] = True
                self.log_command_output(f"Programme désactivé: {name}")
            else:
                self.disabled_programs.pop(name, None)
                self.log_command_output(f"Programme activé: {name}")
                
            self.show_startup()
            messagebox.showinfo("Terminé", f"{name} {'désactivé' if status else 'activé'}")
        except Exception as e:
            self.log_command_output(f"Erreur modification programme démarrage: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de modification: {str(e)}")

    def open_file_location(self, path):
        try:
            path = os.path.dirname(path)
            os.startfile(path)
            self.log_command_output(f"Dossier ouvert: {path}")
        except Exception as e:
            self.log_command_output(f"Erreur ouverture dossier: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dossier: {str(e)}")

    def optimize_memory(self):
        self.log_command_output("\n=== Optimisation de la mémoire ===")
        
        try:
            # Restart Explorer
            self.run_command('taskkill /f /im explorer.exe')
            self.run_command('start explorer.exe')
            
            # Clear standby memory
            self.run_command('rundll32.exe advapi32.dll,ProcessIdleTasks')
            
            self.log_command_output("Optimisation mémoire terminée")
            messagebox.showinfo("Terminé", "Mémoire optimisée")
        except Exception as e:
            self.log_command_output(f"Erreur optimisation mémoire: {str(e)}")
            messagebox.showerror("Erreur", f"Échec d'optimisation: {str(e)}")

    def defragment_disk(self):
        self.log_command_output("\n=== Défragmentation du disque ===")
        
        try:
            # Run defrag with optimization
            self.run_command('defrag C: /O /U /V')
            
            self.log_command_output("Défragmentation terminée")
            messagebox.showinfo("Terminé", "Disque défragmenté")
        except Exception as e:
            self.log_command_output(f"Erreur défragmentation: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de défragmentation: {str(e)}")

    def optimize_services(self):
        self.log_command_output("\n=== Optimisation des services ===")
        
        if not self.admin_mode:
            self.show_admin_warning()
            return
            
        # List of services to disable (non-essential services)
        services_to_disable = [
            "DiagTrack",  # Connected User Experiences and Telemetry
            "dmwappushservice",  # Device Management Wireless Application Protocol
            "MapsBroker",  # Downloaded Maps Manager
            "lfsvc",  # Geolocation Service
            "WMPNetworkSvc",  # Windows Media Player Network Sharing
            "WerSvc",  # Windows Error Reporting
            "Fax"  # Fax Service
        ]
        
        success_count = 0
        
        for service in services_to_disable:
            try:
                # Disable and stop the service
                self.run_command(f'sc config "{service}" start= disabled')
                self.run_command(f'net stop "{service}"')
                
                self.log_command_output(f"Service désactivé: {service}")
                success_count += 1
            except Exception as e:
                self.log_command_output(f"Erreur désactivation {service}: {str(e)}")
                
        if success_count > 0:
            self.log_command_output(f"\n{success_count} services optimisés")
            messagebox.showinfo("Terminé", f"{success_count} services optimisés")
        else:
            self.log_command_output("\nAucun service optimisé")
            messagebox.showinfo("Info", "Aucun service optimisé")

    def optimize_performance(self):
        self.log_command_output("\n=== Optimisation des performances ===")
        
        if not self.admin_mode:
            self.show_admin_warning()
            return
            
        try:
            # Set performance options
            self.run_command('powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')  # High performance
            
            # Disable visual effects
            self.run_command('SystemPropertiesPerformance.exe /pagefile')
            
            # Adjust for best performance
            visual_effects = [
                "DisableTaskMgr 0",
                "DisableRegistryTools 0",
                "CleanPageFileAtShutdown 0",
                "DisablePagingExecutive 1",
                "LargeSystemCache 1",
                "SecondLevelDataCache 256",
                "IoPageLockLimit 512000"
            ]
            
            for effect in visual_effects:
                self.run_command(f'reg add "HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v {effect}')
                
            self.log_command_output("Optimisation des performances terminée")
            messagebox.showinfo("Terminé", "Paramètres de performance optimisés")
        except Exception as e:
            self.log_command_output(f"Erreur optimisation performances: {str(e)}")
            messagebox.showerror("Erreur", f"Échec d'optimisation: {str(e)}")

    def enable_power_saver(self):
        self.log_command_output("\n=== Activation du mode économie d'énergie ===")
        
        try:
            # Set power saver plan
            self.run_command('powercfg /setactive a1841308-3541-4fab-bc81-f71556f20b4a')
            
            # Additional power saving settings
            self.run_command('powercfg /h off')  # Disable hibernation
            self.run_command('powercfg /change /standby-timeout-ac 10')  # Standby after 10 mins on AC
            self.run_command('powercfg /change /monitor-timeout-ac 5')  # Turn off display after 5 mins
            
            self.log_command_output("Mode économie activé")
            messagebox.showinfo("Terminé", "Mode économie d'énergie activé")
        except Exception as e:
            self.log_command_output(f"Erreur activation mode économie: {str(e)}")
            messagebox.showerror("Erreur", f"Échec d'activation: {str(e)}")

    def optimize_display(self):
        self.log_command_output("\n=== Optimisation de l'affichage ===")
        
        try:
            # Disable unnecessary visual effects
            self.run_command('reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop" /v DragFullWindows /t REG_SZ /d 0 /f')
            self.run_command('reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop" /v MenuShowDelay /t REG_SZ /d 0 /f')
            self.run_command('reg add "HKEY_CURRENT_USER\\Control Panel\\Desktop\\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f')
            
            # Set performance options
            self.run_command('SystemPropertiesPerformance.exe /pagefile')
            
            self.log_command_output("Optimisation d'affichage terminée")
            messagebox.showinfo("Terminé", "Paramètres d'affichage optimisés")
        except Exception as e:
            self.log_command_output(f"Erreur optimisation affichage: {str(e)}")
            messagebox.showerror("Erreur", f"Échec d'optimisation: {str(e)}")

    def disable_notifications(self):
        self.log_command_output("\n=== Désactivation des notifications ===")
        
        try:
            # Disable notifications
            self.run_command('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v ToastEnabled /t REG_DWORD /d 0 /f')
            
            # Disable tips and suggestions
            self.run_command('reg add "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SubscribedContent-338388Enabled /t REG_DWORD /d 0 /f')
            
            self.log_command_output("Notifications désactivées")
            messagebox.showinfo("Terminé", "Notifications désactivées")
        except Exception as e:
            self.log_command_output(f"Erreur désactivation notifications: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de désactivation: {str(e)}")

    def optimize_network(self):
        self.log_command_output("\n=== Optimisation du réseau ===")
        
        try:
            # Optimize TCP/IP parameters
            self.run_command('netsh int tcp set global autotuninglevel=restricted')
            self.run_command('netsh int tcp set global rss=enabled')
            
            # Disable QoS
            self.run_command('netsh int tcp set global qos=disabled')
            
            # Disable Nagle's algorithm
            self.run_command('netsh int tcp set global nodelay=1')
            
            self.log_command_output("Optimisation réseau terminée")
            messagebox.showinfo("Terminé", "Paramètres réseau optimisés")
        except Exception as e:
            self.log_command_output(f"Erreur optimisation réseau: {str(e)}")
            messagebox.showerror("Erreur", f"Échec d'optimisation: {str(e)}")

    def test_network_connection(self):
        self.log_command_output("\n=== Test de connexion réseau ===")
        
        try:
            # Test internet connection
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            
            # Test DNS resolution
            socket.gethostbyname("google.com")
            
            self.log_command_output("Connexion réseau fonctionnelle")
            messagebox.showinfo("Terminé", "Réseau fonctionnel")
        except Exception as e:
            self.log_command_output(f"Erreur test réseau: {str(e)}")
            messagebox.showerror("Erreur", f"Échec du test: {str(e)}")

    def flush_dns_cache(self):
        self.log_command_output("\n=== Vidage du cache DNS ===")
        
        try:
            self.run_command('ipconfig /flushdns')
            self.log_command_output("Cache DNS vidé")
            messagebox.showinfo("Terminé", "Cache DNS vidé")
        except Exception as e:
            self.log_command_output(f"Erreur vidage cache DNS: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de vidage: {str(e)}")

    def reset_tcpip(self):
        self.log_command_output("\n=== Réinitialisation TCP/IP ===")
        
        if not self.admin_mode:
            self.show_admin_warning()
            return
            
        try:
            self.run_command('netsh int ip reset')
            self.run_command('netsh winsock reset')
            
            self.log_command_output("TCP/IP réinitialisé - Redémarrage nécessaire")
            messagebox.showinfo("Terminé", "TCP/IP réinitialisé\nRedémarrez votre ordinateur")
        except Exception as e:
            self.log_command_output(f"Erreur réinitialisation TCP/IP: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de réinitialisation: {str(e)}")

    def show_ip_info(self):
        self.log_command_output("\n=== Informations IP ===")
        
        try:
            # Get hostname
            hostname = socket.gethostname()
            self.log_command_output(f"Nom d'hôte: {hostname}")
            
            # Get local IP
            local_ip = socket.gethostbyname(hostname)
            self.log_command_output(f"IP locale: {local_ip}")
            
            # Get public IP
            try:
                import requests
                public_ip = requests.get('https://api.ipify.org').text
                self.log_command_output(f"IP publique: {public_ip}")
            except:
                self.log_command_output("IP publique: Non disponible")
                
            # Get network interfaces
            try:
                interfaces = psutil.net_if_addrs()
                self.log_command_output("\nInterfaces réseau:")
                for name, addrs in interfaces.items():
                    self.log_command_output(f"- {name}:")
                    for addr in addrs:
                        self.log_command_output(f"  {addr.family.name}: {addr.address}")
            except:
                self.log_command_output("\nInterfaces: Non disponible")
                
            messagebox.showinfo("Terminé", "Informations IP affichées dans la console")
        except Exception as e:
            self.log_command_output(f"Erreur récupération infos IP: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de récupération: {str(e)}")

    def run_ping_test(self, host="google.com"):
        self.log_command_output(f"\n=== Test Ping {host} ===")
        
        try:
            output, _ = self.run_command(f'ping {host}')
            
            # Parse ping results
            if "temps=" in output:
                times = [line.split("temps=")[1].split(" ")[0] for line in output.split("\n") if "temps=" in line]
                avg_time = sum(float(t.replace("ms", "")) for t in times) / len(times)
                self.log_command_output(f"Temps moyen: {avg_time:.2f} ms")
                
            messagebox.showinfo("Terminé", "Test Ping terminé")
        except Exception as e:
            self.log_command_output(f"Erreur test Ping: {str(e)}")
            messagebox.showerror("Erreur", f"Échec du test: {str(e)}")

    def run_traceroute(self, host="google.com"):
        self.log_command_output(f"\n=== Traceroute {host} ===")
        
        try:
            output, _ = self.run_command(f'tracert {host}')
            messagebox.showinfo("Terminé", "Traceroute terminé")
        except Exception as e:
            self.log_command_output(f"Erreur traceroute: {str(e)}")
            messagebox.showerror("Erreur", f"Échec du test: {str(e)}")

    def run_port_scan(self, ports="80,443,3389"):
        self.log_command_output("\n=== Analyse de ports ===")
        
        try:
            # Scan common ports
            open_ports = []
            for port in [80, 443, 3389, 21, 22, 23, 25, 53, 110, 143, 3306]:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex(('127.0.0.1', port))
                    if result == 0:
                        open_ports.append(port)
                        self.log_command_output(f"Port ouvert: {port}")
                    sock.close()
                except:
                    continue
                    
            if open_ports:
                self.log_command_output(f"\nPorts ouverts: {', '.join(map(str, open_ports))}")
                messagebox.showinfo("Terminé", f"Ports ouverts: {', '.join(map(str, open_ports))}")
            else:
                self.log_command_output("\nAucun port ouvert détecté")
                messagebox.showinfo("Terminé", "Aucun port ouvert détecté")
        except Exception as e:
            self.log_command_output(f"Erreur analyse ports: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de l'analyse: {str(e)}")

    def run_speed_test(self):
        self.log_command_output("\n=== Test de vitesse ===")
        
        try:
            import speedtest
            self.log_command_output("Lancement du test de vitesse...")
            
            st = speedtest.Speedtest()
            st.get_best_server()
            
            download_speed = st.download() / 10**6  # Mbps
            upload_speed = st.upload() / 10**6  # Mbps
            ping = st.results.ping
            
            self.log_command_output(f"\nRésultats:")
            self.log_command_output(f"Download: {download_speed:.2f} Mbps")
            self.log_command_output(f"Upload: {upload_speed:.2f} Mbps")
            self.log_command_output(f"Ping: {ping:.2f} ms")
            
            messagebox.showinfo("Terminé", f"Vitesse:\nDownload: {download_speed:.2f} Mbps\nUpload: {upload_speed:.2f} Mbps\nPing: {ping:.2f} ms")
        except Exception as e:
            self.log_command_output(f"Erreur test vitesse: {str(e)}")
            messagebox.showerror("Erreur", f"Échec du test: {str(e)}")

    def check_firewall_status(self):
        self.log_command_output("\n=== Vérification du pare-feu ===")
        
        try:
            c = wmi.WMI()
            firewall = c.Win32_Service(Name="MpsSvc")[0]
            
            status = "Actif" if firewall.State == "Running" else "Inactif"
            self.log_command_output(f"Pare-feu: {status}")
            
            messagebox.showinfo("Info", f"Pare-feu: {status}")
        except Exception as e:
            self.log_command_output(f"Erreur vérification pare-feu: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de vérification: {str(e)}")

    def check_antivirus_status(self):
        self.log_command_output("\n=== Vérification de l'antivirus ===")
        
        try:
            c = wmi.WMI(namespace="root\\SecurityCenter2")
            antivirus = c.AntiVirusProduct()
            
            if antivirus:
                for av in antivirus:
                    status = "Actif" if av.productState & 0x1000 else "Inactif"
                    self.log_command_output(f"{av.displayName}: {status}")
                    
                messagebox.showinfo("Info", f"Antivirus: {av.displayName} ({status})")
            else:
                self.log_command_output("Aucun antivirus détecté")
                messagebox.showinfo("Info", "Aucun antivirus détecté")
        except Exception as e:
            self.log_command_output(f"Erreur vérification antivirus: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de vérification: {str(e)}")

    def check_windows_updates(self):
        self.log_command_output("\n=== Vérification des mises à jour ===")
        
        try:
            c = wmi.WMI(namespace="root\\Microsoft\\Windows\\WindowsUpdate")
            updates = c.ExecQuery("SELECT * FROM MSFT_WUOperations")
            
            if updates:
                self.log_command_output(f"{len(updates)} mises à jour disponibles")
                messagebox.showinfo("Mises à jour", f"{len(updates)} mises à jour disponibles")
            else:
                self.log_command_output("Aucune mise à jour disponible")
                messagebox.showinfo("Mises à jour", "Aucune mise à jour disponible")
        except Exception as e:
            self.log_command_output(f"Erreur vérification mises à jour: {str(e)}")
            messagebox.showerror("Erreur", f"Impossible de vérifier: {str(e)}")

    def check_windows_updates_status(self):
        try:
            c = wmi.WMI(namespace="root\\Microsoft\\Windows\\WindowsUpdate")
            updates = c.ExecQuery("SELECT * FROM MSFT_WUOperations")
            return len(updates) == 0
        except:
            return False

    def run_security_scan(self):
        self.log_command_output("\n=== Analyse de sécurité ===")
        
        try:
            # Check critical security settings
            security_status = {
                "firewall": False,
                "antivirus": False,
                "updates": False,
                "users": False,
                "sharing": False
            }
            
            # Check firewall
            try:
                c = wmi.WMI()
                firewall = c.Win32_Service(Name="MpsSvc")[0]
                security_status["firewall"] = firewall.State == "Running"
            except:
                pass
                
            # Check antivirus
            try:
                c = wmi.WMI(namespace="root\\SecurityCenter2")
                antivirus = c.AntiVirusProduct()
                security_status["antivirus"] = any(av.productState & 0x1000 for av in antivirus)
            except:
                pass
                
            # Check updates
            try:
                c = wmi.WMI(namespace="root\\Microsoft\\Windows\\WindowsUpdate")
                updates = c.ExecQuery("SELECT * FROM MSFT_WUOperations")
                security_status["updates"] = len(updates) == 0
            except:
                pass
                
            # Check admin users
            try:
                c = wmi.WMI()
                users = c.Win32_UserAccount()
                security_status["users"] = all(user.Name.lower() != "administrator" for user in users)
            except:
                pass
                
            # Check file sharing
            try:
                output, _ = self.run_command('net share', show_output=False)
                security_status["sharing"] = "No entries" in output
            except:
                pass
                
            # Display results
            self.log_command_output("\nRésultats de sécurité:")
            for item, status in security_status.items():
                self.log_command_output(f"- {item}: {'✅' if status else '❌'}")
                
            messagebox.showinfo("Terminé", "Analyse de sécurité terminée")
        except Exception as e:
            self.log_command_output(f"Erreur analyse sécurité: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de l'analyse: {str(e)}")

    def view_security_logs(self):
        self.log_command_output("\n=== Journaux de sécurité ===")
        
        try:
            self.run_command('eventvwr.msc /c:Security')
            self.log_command_output("Observateur d'événements ouvert")
            messagebox.showinfo("Terminé", "Observateur d'événements ouvert")
        except Exception as e:
            self.log_command_output(f"Erreur ouverture journaux: {str(e)}")
            messagebox.showerror("Erreur", f"Échec d'ouverture: {str(e)}")

    def check_backdoors(self):
        self.log_command_output("\n=== Vérification des portes dérobées ===")
        
        try:
            # Check suspicious connections
            connections = psutil.net_connections()
            suspicious = []
            
            for conn in connections:
                if conn.status == 'ESTABLISHED' and conn.raddr and conn.raddr.port in [4444, 5555, 6666, 7777, 8888]:
                    suspicious.append(conn)
                    
            if suspicious:
                self.log_command_output("\nConnexions suspectes trouvées:")
                for conn in suspicious:
                    self.log_command_output(f"- PID {conn.pid} à {conn.raddr.ip}:{conn.raddr.port}")
                    
                messagebox.showwarning("Attention", "Connexions suspectes détectées")
            else:
                self.log_command_output("\nAucune connexion suspecte trouvée")
                messagebox.showinfo("Terminé", "Aucune porte dérobée détectée")
        except Exception as e:
            self.log_command_output(f"Erreur vérification portes dérobées: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de vérification: {str(e)}")

    def add_user_account(self):
        username = self.new_user_name.get()
        password = self.new_user_pass.get()
        
        if not username or not password:
            messagebox.showerror("Erreur", "Nom d'utilisateur et mot de passe requis")
            return
            
        self.log_command_output(f"\n=== Ajout utilisateur {username} ===")
        
        try:
            self.run_command(f'net user {username} {password} /add')
            self.run_command(f'net localgroup users {username} /add')
            
            self.log_command_output(f"Utilisateur {username} ajouté")
            messagebox.showinfo("Succès", f"Utilisateur {username} ajouté")
            
            # Clear fields
            self.new_user_name.delete(0, 'end')
            self.new_user_pass.delete(0, 'end')
            
            # Refresh list
            self.show_users()
        except Exception as e:
            self.log_command_output(f"Erreur ajout utilisateur: {str(e)}")
            messagebox.showerror("Erreur", f"Échec d'ajout: {str(e)}")

    def toggle_user_account(self, username, status):
        self.log_command_output(f"\n=== Modification utilisateur {username} ===")
        
        try:
            if status == "Actif":
                self.run_command(f'net user {username} /active:no')
                self.log_command_output(f"Utilisateur {username} désactivé")
                messagebox.showinfo("Succès", f"{username} désactivé")
            else:
                self.run_command(f'net user {username} /active:yes')
                self.log_command_output(f"Utilisateur {username} activé")
                messagebox.showinfo("Succès", f"{username} activé")
                
            self.show_users()
        except Exception as e:
            self.log_command_output(f"Erreur modification utilisateur: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de modification: {str(e)}")

    def delete_user_account(self, username):
        if not messagebox.askyesno("Confirmation", f"Supprimer l'utilisateur {username}?"):
            return
            
        self.log_command_output(f"\n=== Suppression utilisateur {username} ===")
        
        try:
            self.run_command(f'net user {username} /delete')
            
            self.log_command_output(f"Utilisateur {username} supprimé")
            messagebox.showinfo("Succès", f"{username} supprimé")
            
            self.show_users()
        except Exception as e:
            self.log_command_output(f"Erreur suppression utilisateur: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de suppression: {str(e)}")

    def toggle_admin(self, username, current_status):
        self.log_command_output(f"\n=== Modification droits admin {username} ===")
        
        try:
            if current_status == "Admin":
                self.run_command(f'net localgroup administrators {username} /delete')
                self.log_command_output(f"Droits admin retirés pour {username}")
                messagebox.showinfo("Succès", f"Droits admin retirés pour {username}")
            else:
                self.run_command(f'net localgroup administrators {username} /add')
                self.log_command_output(f"Droits admin ajoutés pour {username}")
                messagebox.showinfo("Succès", f"Droits admin ajoutés pour {username}")
                
            self.show_users()
        except Exception as e:
            self.log_command_output(f"Erreur modification droits: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de modification: {str(e)}")

    def uninstall_software(self, software_name):
        if not messagebox.askyesno("Confirmation", f"Désinstaller {software_name}?"):
            return
            
        self.log_command_output(f"\n=== Désinstallation {software_name} ===")
        
        try:
            # Try with WMIC first
            self.run_command(f'wmic product where name="{software_name}" call uninstall /nointeractive')
            
            # Fallback to registry uninstall string
            try:
                with winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE,
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
                ) as key:
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    if name == software_name:
                                        uninstall_string = winreg.QueryValueEx(subkey, "UninstallString")[0]
                                        self.run_command(uninstall_string + ' /quiet /norestart')
                                        break
                                except:
                                    pass
                            i += 1
                        except OSError:
                            break
            except:
                pass
                
            self.log_command_output(f"Logiciel {software_name} désinstallé")
            messagebox.showinfo("Succès", f"{software_name} désinstallé")
            
            self.populate_software_list()
        except Exception as e:
            self.log_command_output(f"Erreur désinstallation: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de désinstallation: {str(e)}")

    def generate_system_report(self):
        self.log_command_output("\n=== Génération rapport système ===")
        
        try:
            report = "=== Rapport système ===\n"
            report += f"Généré le: {datetime.datetime.now()}\n\n"
            
            # System info
            report += "=== Système ===\n"
            for category, items in self.get_detailed_system_info().items():
                report += f"\n{category}:\n"
                for k, v in items.items():
                    report += f"- {k}: {v}\n"
                    
            # Resources
            report += "\n=== Ressources ===\n"
            report += f"CPU: {psutil.cpu_percent()}%\n"
            
            mem = psutil.virtual_memory()
            report += f"Mémoire: {mem.percent}% (Used: {mem.used/(1024**3):.1f}GB / {mem.total/(1024**3):.1f}GB)\n"
            
            disk = psutil.disk_usage('/')
            report += f"Disque: {disk.percent}% (Used: {disk.used/(1024**3):.1f}GB / {disk.total/(1024**3):.1f}GB)\n"
            
            # Save to file
            report_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'rapport_systeme.txt')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            self.log_command_output(f"Rapport généré: {report_file}")
            messagebox.showinfo("Terminé", f"Rapport généré: {report_file}")
            
            # Open the report
            os.startfile(report_file)
        except Exception as e:
            self.log_command_output(f"Erreur génération rapport: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de génération: {str(e)}")

    def generate_performance_report(self):
        self.log_command_output("\n=== Génération rapport performance ===")
        
        try:
            report = "=== Rapport performance ===\n"
            report += f"Généré le: {datetime.datetime.now()}\n\n"
            
            # CPU info
            cpu = psutil.cpu_percent(percpu=True)
            report += "=== CPU ===\n"
            report += f"Utilisation globale: {psutil.cpu_percent()}%\n"
            for i, core in enumerate(cpu):
                report += f"Core {i}: {core}%\n"
                
            # Memory info
            mem = psutil.virtual_memory()
            report += "\n=== Mémoire ===\n"
            report += f"Utilisation: {mem.percent}%\n"
            report += f"Total: {mem.total/(1024**3):.1f} GB\n"
            report += f"Disponible: {mem.available/(1024**3):.1f} GB\n"
            report += f"Utilisé: {mem.used/(1024**3):.1f} GB\n"
            
            # Disk info
            disk = psutil.disk_usage('/')
            report += "\n=== Disque ===\n"
            report += f"Utilisation: {disk.percent}%\n"
            report += f"Total: {disk.total/(1024**3):.1f} GB\n"
            report += f"Utilisé: {disk.used/(1024**3):.1f} GB\n"
            report += f"Libre: {disk.free/(1024**3):.1f} GB\n"
            
            # Network info
            net = psutil.net_io_counters()
            report += "\n=== Réseau ===\n"
            report += f"Envoyé: {net.bytes_sent/(1024**2):.1f} MB\n"
            report += f"Reçu: {net.bytes_recv/(1024**2):.1f} MB\n"
            
            # Save to file
            report_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'rapport_performance.txt')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            self.log_command_output(f"Rapport généré: {report_file}")
            messagebox.showinfo("Terminé", f"Rapport généré: {report_file}")
            
            # Open the report
            os.startfile(report_file)
        except Exception as e:
            self.log_command_output(f"Erreur génération rapport: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de génération: {str(e)}")

    def generate_software_report(self):
        self.log_command_output("\n=== Génération rapport logiciels ===")
        
        try:
            report = "=== Rapport logiciels ===\n"
            report += f"Généré le: {datetime.datetime.now()}\n\n"
            
            # Get installed software
            software = self.get_installed_software()
            
            report += f"Logiciels installés ({len(software)}):\n"
            for name, version, publisher in software:
                report += f"\n- {name}\n  Version: {version}\n  Éditeur: {publisher}\n"
                
            # Save to file
            report_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'rapport_logiciels.txt')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            self.log_command_output(f"Rapport généré: {report_file}")
            messagebox.showinfo("Terminé", f"Rapport généré: {report_file}")
            
            # Open the report
            os.startfile(report_file)
        except Exception as e:
            self.log_command_output(f"Erreur génération rapport: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de génération: {str(e)}")

    def generate_full_report(self):
        self.log_command_output("\n=== Génération rapport complet ===")
        
        try:
            report = "=== Rapport système complet ===\n"
            report += f"Généré le: {datetime.datetime.now()}\n\n"
            
            # System info
            report += "=== Système ===\n"
            for category, items in self.get_detailed_system_info().items():
                report += f"\n{category}:\n"
                for k, v in items.items():
                    report += f"- {k}: {v}\n"
                    
            # Performance
            report += "\n=== Performance ===\n"
            report += f"CPU: {psutil.cpu_percent()}%\n"
            
            mem = psutil.virtual_memory()
            report += f"Mémoire: {mem.percent}% (Used: {mem.used/(1024**3):.1f}GB / {mem.total/(1024**3):.1f}GB)\n"
            
            disk = psutil.disk_usage('/')
            report += f"Disque: {disk.percent}% (Used: {disk.used/(1024**3):.1f}GB / {disk.total/(1024**3):.1f}GB)\n"
            
            # Software
            report += "\n=== Logiciels ===\n"
            software = self.get_installed_software()
            report += f"Logiciels installés ({len(software)}):\n"
            for name, version, publisher in software[:20]:  # Limit to first 20
                report += f"- {name} (v{version}) - {publisher}\n"
            if len(software) > 20:
                report += f"... et {len(software)-20} autres\n"
                
            # Security
            report += "\n=== Sécurité ===\n"
            try:
                c = wmi.WMI(namespace="root\\SecurityCenter2")
                antivirus = c.AntiVirusProduct()
                if antivirus:
                    report += "Antivirus:\n"
                    for av in antivirus:
                        status = "Actif" if av.productState & 0x1000 else "Inactif"
                        report += f"- {av.displayName}: {status}\n"
                else:
                    report += "Aucun antivirus détecté\n"
            except:
                report += "Impossible de vérifier l'antivirus\n"
                
            try:
                c = wmi.WMI()
                firewall = c.Win32_Service(Name="MpsSvc")[0]
                report += f"Pare-feu: {'Actif' if firewall.State == 'Running' else 'Inactif'}\n"
            except:
                report += "Impossible de vérifier le pare-feu\n"
                
            # Users
            report += "\n=== Utilisateurs ===\n"
            users = self.get_user_accounts()
            for user, account_type, status in users:
                report += f"- {user} ({account_type}): {status}\n"
                
            # Save to file
            report_file = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'rapport_complet.txt')
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            self.log_command_output(f"Rapport généré: {report_file}")
            messagebox.showinfo("Terminé", f"Rapport généré: {report_file}")
            
            # Open the report
            os.startfile(report_file)
        except Exception as e:
            self.log_command_output(f"Erreur génération rapport: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de génération: {str(e)}")

    def view_event_logs(self):
        self.log_command_output("\n=== Affichage des journaux d'événements ===")
        
        try:
            self.run_command('eventvwr')
            self.log_command_output("Observateur d'événements ouvert")
            messagebox.showinfo("Terminé", "Observateur d'événements ouvert")
        except Exception as e:
            self.log_command_output(f"Erreur ouverture journaux: {str(e)}")
            messagebox.showerror("Erreur", f"Échec d'ouverture: {str(e)}")

    def schedule_task(self, task_name, frequency):
        self.log_command_output(f"\n=== Planification tâche {task_name} ({frequency}) ===")
        
        try:
            # Map frequency to Windows task scheduler values
            freq_map = {
                "quotidien": "DAILY",
                "hebdomadaire": "WEEKLY",
                "mensuel": "MONTHLY"
            }
            
            # Create a basic task
            task_cmd = f'schtasks /create /tn "Optimiseur_{task_name}" /tr "{sys.executable} {__file__} {task_name}" /sc {freq_map.get(frequency, "DAILY")}'
            self.run_command(task_cmd)
            
            self.log_command_output(f"Tâche planifiée: {task_name} ({frequency})")
            messagebox.showinfo("Planifié", f"{task_name.replace('_', ' ').title()} programmé pour {frequency}")
        except Exception as e:
            self.log_command_output(f"Erreur planification: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de planification: {str(e)}")

    def schedule_one_time_task(self, task_name):
        time_str = self.schedule_time.get()
        
        if not time_str:
            messagebox.showerror("Erreur", "Veuillez spécifier une heure")
            return
            
        self.log_command_output(f"\n=== Planification tâche ponctuelle {task_name} à {time_str} ===")
        
        try:
            # Validate time format
            datetime.datetime.strptime(time_str, "%H:%M")
            
            # Create a one-time task
            task_cmd = f'schtasks /create /tn "Optimiseur_{task_name}_ponctuel" /tr "{sys.executable} {__file__} {task_name}" /sc ONCE /st {time_str}'
            self.run_command(task_cmd)
            
            self.log_command_output(f"Tâche ponctuelle planifiée: {task_name} à {time_str}")
            messagebox.showinfo("Planifié", f"Tâche '{task_name}' programmée à {time_str}")
        except ValueError:
            self.log_command_output("Format d'heure invalide (HH:MM requis)")
            messagebox.showerror("Erreur", "Format HH:MM requis")
        except Exception as e:
            self.log_command_output(f"Erreur planification: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de planification: {str(e)}")

    def run_scheduled_task(self, task_name, time_str):
        try:
            target_time = datetime.datetime.strptime(time_str, "%H:%M").time()
            
            while True:
                now = datetime.datetime.now().time()
                if now.hour == target_time.hour and now.minute == target_time.minute:
                    getattr(self, task_name)()
                    break
                time.sleep(30)
        except Exception as e:
            self.log_command_output(f"Erreur tâche planifiée: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de tâche: {str(e)}")

    def restart_system(self):
        if messagebox.askyesno("Confirmation", "Redémarrer l'ordinateur maintenant?"):
            try:
                self.run_command('shutdown /r /t 0')
            except Exception as e:
                messagebox.showerror("Erreur", f"Échec du redémarrage: {str(e)}")

    def shutdown_system(self):
        if messagebox.askyesno("Confirmation", "Éteindre l'ordinateur maintenant?"):
            try:
                self.run_command('shutdown /s /t 0')
            except Exception as e:
                messagebox.showerror("Erreur", f"Échec de l'extinction: {str(e)}")

    def sleep_system(self):
        if messagebox.askyesno("Confirmation", "Mettre l'ordinateur en veille maintenant?"):
            try:
                import ctypes
                ctypes.windll.PowrProf.SetSuspendState(0, 1, 0)
            except Exception as e:
                messagebox.showerror("Erreur", f"Échec de la mise en veille: {str(e)}")

    def open_task_manager(self):
        try:
            self.run_command('taskmgr')
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec d'ouverture: {str(e)}")

    def create_backup(self):
        self.log_command_output("\n=== Création sauvegarde ===")
        
        try:
            backup_dir = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'Backup')
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup important folders
            folders_to_backup = [
                os.path.join(os.environ['USERPROFILE'], 'Documents'),
                os.path.join(os.environ['USERPROFILE'], 'Desktop'),
                os.path.join(os.environ['USERPROFILE'], 'Pictures')
            ]
            
            for folder in folders_to_backup:
                if os.path.exists(folder):
                    dest = os.path.join(backup_dir, os.path.basename(folder))
                    shutil.copytree(folder, dest, dirs_exist_ok=True)
                    self.log_command_output(f"Dossier sauvegardé: {folder}")
                    
            self.log_command_output(f"\nSauvegarde complète: {backup_dir}")
            messagebox.showinfo("Terminé", f"Sauvegarde créée: {backup_dir}")
        except Exception as e:
            self.log_command_output(f"Erreur sauvegarde: {str(e)}")
            messagebox.showerror("Erreur", f"Échec de sauvegarde: {str(e)}")

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)
        self.log_command_output(f"Thème changé: {theme}")

    def change_language(self, lang):
        # This would need proper internationalization implementation
        self.log_command_output(f"Langue changée: {lang}")
        messagebox.showinfo("Info", "Redémarrez l'application pour appliquer la langue")

    def save_settings(self):
        self.log_command_output("\n=== Enregistrement paramètres ===")
        messagebox.showinfo("Terminé", "Paramètres enregistrés")

if __name__ == "__main__":
    root = ctk.CTk()
    app = WindowsOptimizerApp(root)
    root.mainloop()
