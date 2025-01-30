from SimConnect import SimConnect, AircraftRequests
from pypresence import Presence
import time
CLIENT_ID = "1334263929999986861"
rpc = Presence(CLIENT_ID)
rpc.connect()
sm = SimConnect()
aq = AircraftRequests(sm, _time=2000)  

def update_presence():
    aircraft_name = aq.get("TITLE") 
    altitude = aq.get("PLANE_ALTITUDE") 
    airspeed = aq.get("AIRSPEED_TRUE")  
    departure = aq.get("ATC_FLIGHT_NUMBER")  
    destination = aq.get("GPS_FLIGHT_PLAN_DEST")  
    flight_info = f"{departure} ➝ {destination}" if departure and destination else "En route"
    rpc.update(
        details=f"{aircraft_name}",
        state=f"{flight_info} | {altitude:.0f} ft, {airspeed:.0f} knots",
        large_image="embedded_cover",  
    )
while True:
    update_presence()
    time.sleep(15) 
