import tkinter as tk
from tkinter import ttk
import random


class GrowControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grow Control")

        # Fenstergröße (kannst du ändern oder entfernen)
        self.root.geometry("1280x720")

        # Schriftarten
        self.base_font = ("Segoe UI", 16)
        self.title_font = ("Segoe UI", 20, "bold")

        # Grundlayout mit Grid
        self.root.rowconfigure(0, weight=1)   # Status
        self.root.rowconfigure(1, weight=4)   # Hauptbereich
        self.root.rowconfigure(2, weight=1)   # Navigation
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        # === Statusleiste oben ===
        status_frame = ttk.Frame(self.root, padding=20)
        status_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.temp_label = tk.Label(
            status_frame, text="Temp: -- °C", font=self.title_font
        )
        self.hum_label = tk.Label(
            status_frame, text="RH: -- %", font=self.title_font
        )
        self.mode_label = tk.Label(
            status_frame, text="Mode: Veg", font=self.title_font
        )

        self.temp_label.pack(side="left", padx=20)
        self.hum_label.pack(side="left", padx=20)
        self.mode_label.pack(side="right", padx=20)

        # === Hauptbereich Mitte ===
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # --- Licht-Spalte ---
        light_frame = ttk.LabelFrame(main_frame, text="Licht", padding=20)
        light_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        tk.Label(light_frame, text="SANlight 1 (%)", font=self.base_font).pack(
            anchor="w"
        )
        self.l1_var = tk.IntVar(value=100)
        self.l1_slider = tk.Scale(
            light_frame,
            from_=0,
            to=100,
            orient="horizontal",
            font=self.base_font,
            showvalue=True,
            length=300,
            command=self.on_l1_change,
        )
        self.l1_slider.set(100)
        self.l1_slider.pack(fill="x", pady=10)

        tk.Label(light_frame, text="SANlight 2 (%)", font=self.base_font).pack(
            anchor="w"
        )
        self.l2_var = tk.IntVar(value=100)
        self.l2_slider = tk.Scale(
            light_frame,
            from_=0,
            to=100,
            orient="horizontal",
            font=self.base_font,
            showvalue=True,
            length=300,
            command=self.on_l2_change,
        )
        self.l2_slider.set(100)
        self.l2_slider.pack(fill="x", pady=10)

        # --- Klima-Spalte ---
        climate_frame = ttk.LabelFrame(main_frame, text="Klima", padding=20)
        climate_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.fan_on = tk.BooleanVar(value=False)
        self.circ_on = tk.BooleanVar(value=False)

        self.fan_button = tk.Button(
            climate_frame,
            text="Abluft AUS",
            font=self.base_font,
            height=2,
            command=self.toggle_fan,
        )
        self.fan_button.pack(fill="x", pady=10)

        self.circ_button = tk.Button(
            climate_frame,
            text="Umluft AUS",
            font=self.base_font,
            height=2,
            command=self.toggle_circ,
        )
        self.circ_button.pack(fill="x", pady=10)

        tk.Label(
            climate_frame,
            text="Ziel-Temp / RH (später)",
            font=self.base_font,
        ).pack(pady=20)

        # === Navigation unten ===
        nav_frame = ttk.Frame(self.root, padding=10)
        nav_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        for col in range(4):
            nav_frame.columnconfigure(col, weight=1)

        self.btn_dashboard = tk.Button(
            nav_frame,
            text="Dashboard",
            font=self.base_font,
            height=2,
            command=self.on_dashboard,
        )
        self.btn_lights = tk.Button(
            nav_frame,
            text="Licht",
            font=self.base_font,
            height=2,
            command=self.on_lights,
        )
        self.btn_climate = tk.Button(
            nav_frame,
            text="Klima",
            font=self.base_font,
            height=2,
            command=self.on_climate,
        )
        self.btn_settings = tk.Button(
            nav_frame,
            text="Einstellungen",
            font=self.base_font,
            height=2,
            command=self.on_settings,
        )

        self.btn_dashboard.grid(row=0, column=0, sticky="nsew", padx=5)
        self.btn_lights.grid(row=0, column=1, sticky="nsew", padx=5)
        self.btn_climate.grid(row=0, column=2, sticky="nsew", padx=5)
        self.btn_settings.grid(row=0, column=3, sticky="nsew", padx=5)

        # Demo-Sensorwerte (werden simuliert)
        self.temp_c = 24.5
        self.rh = 60.0

        # Demo-Loop starten
        self.update_sensors_demo()

    # === Event-Handler ===
    def on_l1_change(self, value):
        val = int(float(value))
        print(f"SANlight 1 auf {val}%")
        # später hier: Befehl an ESP32 senden

    def on_l2_change(self, value):
        val = int(float(value))
        print(f"SANlight 2 auf {val}%")
        # später hier: Befehl an ESP32 senden

    def toggle_fan(self):
        self.fan_on.set(not self.fan_on.get())
        state = self.fan_on.get()
        self.fan_button.config(text=f"Abluft {'AN' if state else 'AUS'}")
        print(f"Abluft {'eingeschaltet' if state else 'ausgeschaltet'}")

    def toggle_circ(self):
        self.circ_on.set(not self.circ_on.get())
        state = self.circ_on.get()
        self.circ_button.config(text=f"Umluft {'AN' if state else 'AUS'}")
        print(f"Umluft {'eingeschaltet' if state else 'ausgeschaltet'}")

    def on_dashboard(self):
        print("Dashboard-Button gedrückt")

    def on_lights(self):
        print("Licht-Button gedrückt")

    def on_climate(self):
        print("Klima-Button gedrückt")

    def on_settings(self):
        print("Einstellungen-Button gedrückt")

    def update_sensors_demo(self):
        """Simuliert Temperatur & Luftfeuchte (Demo-Modus)."""
        # kleine zufällige Schwankung
        self.temp_c += random.uniform(-0.2, 0.2)
        self.rh += random.uniform(-0.5, 0.5)

        # auf sinnvolle Bereiche begrenzen
        self.temp_c = max(18.0, min(32.0, self.temp_c))
        self.rh = max(40.0, min(80.0, self.rh))

        self.temp_label.config(text=f"Temp: {self.temp_c:.1f} °C")
        self.hum_label.config(text=f"RH: {self.rh:.1f} %")

        # alle 3 Sekunden erneut aufrufen
        self.root.after(3000, self.update_sensors_demo)


if __name__ == "__main__":
    root = tk.Tk()
    app = GrowControlApp(root)
    root.mainloop()
