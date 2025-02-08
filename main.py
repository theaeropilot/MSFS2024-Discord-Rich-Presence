import tkinter as tk
from tkinter import StringVar
from SimConnect import SimConnect, AircraftRequests
from pypresence import Presence
import time
import threading

CLIENT_ID = "1334263929999986861"
rpc, sm = None, None

root = tk.Tk()
root.title("MSFS2024 Rich Presence")
root.geometry("400x300")
root.configure(bg="#2b2b2b")

discord_status = tk.Label(root, text="Discord: ❌", fg="red", bg="#2b2b2b", font=("Arial", 12))
discord_status.pack(pady=10)
sim_status = tk.Label(root, text="SimConnect: ❌", fg="red", bg="#2b2b2b", font=("Arial", 12))
sim_status.pack(pady=10)

departure_var, destination_var = StringVar(), StringVar()

tk.Label(root, text="Departure: (Optional)", fg="white", bg="#2b2b2b", font=("Arial", 10)).pack()
departure_entry = tk.Entry(root, textvariable=departure_var, bg="#3b3b3b", fg="white", font=("Arial", 10))
departure_entry.pack(pady=5)

tk.Label(root, text="Arrival: (Optional)", fg="white", bg="#2b2b2b", font=("Arial", 10)).pack()
destination_entry = tk.Entry(root, textvariable=destination_var, bg="#3b3b3b", fg="white", font=("Arial", 10))
destination_entry.pack(pady=5)

def connect_services():
    global rpc, sm, aq
    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
        discord_status.config(text="Discord: ✅", fg="green")
    except:
        discord_status.config(text="Discord: ❌", fg="red")
    try:
        sm = SimConnect()
        aq = AircraftRequests(sm, _time=2000)
        sim_status.config(text="SimConnect: ✅", fg="green")
    except:
        sim_status.config(text="SimConnect: ❌", fg="red")

def clean_name(name):
    return name.decode("utf-8").split(":")[0].strip() if isinstance(name, bytes) else name.split(":")[0].strip() if name else "Unknown"

def update_presence():
    while True:
        try:
            if not rpc or not sm:
                time.sleep(3)
                continue
            aircraft_name = clean_name(aq.get("TITLE")) or "Unknown"
            altitude, airspeed = aq.get("PLANE_ALTITUDE") or 0, aq.get("AIRSPEED_TRUE") or 0
            heading, vertical_speed = aq.get("PLANE_HEADING_DEGREES_MAGNETIC") or 0, aq.get("VERTICAL_SPEED") or 0
            fuel_level = (aq.get("FUEL_TOTAL_QUANTITY") / aq.get("FUEL_CAPACITY")) * 100 if aq.get("FUEL_CAPACITY") else 0
            on_ground = aq.get("SIM_ON_GROUND") == 1
            autopilot_status = "On" if aq.get("AUTOPILOT_MASTER") == 1 else "Off"
            departure = departure_var.get() or clean_name(aq.get("GPS_FLIGHT_PLAN_ORIGIN")) or "Unknown"
            destination = destination_var.get() or clean_name(aq.get("GPS_FLIGHT_PLAN_DEST")) or "Unknown"
            flight_info = f"At {departure}" if on_ground else f"En route to {destination}"
            rpc.update(
                details=f"{aircraft_name} | Hdg {heading:.0f}°",
                state=f"{flight_info} | {altitude:.0f} ft, {airspeed:.0f} knots | VS {vertical_speed:.0f} fpm | Fuel {fuel_level:.0f}% | Autopilot: {autopilot_status}",
                large_image="embedded_cover",
                small_image="small",
                small_text="Microsoft Flight Simulator 2024",
                start=time.time(),
            )
        except Exception as e:
            print(f"Error updating presence: {e}")
        time.sleep(3)


connect_services()
threading.Thread(target=update_presence, daemon=True).start()
root.mainloop()
