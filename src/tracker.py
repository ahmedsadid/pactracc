import os
import json
import easypost
import googlemaps
from dotenv import load_dotenv
load_dotenv()

def create_tracker(tracking_code, carrier, jsonify=True):
    client = easypost.EasyPostClient(os.getenv("EASYPOST_KEY_TEST"))
    tracker = client.tracker.create(
            tracking_code=tracking_code,
            carrier=carrier)
 
    if not jsonify:
        return tracker  # returns formatted string representation of easypost Tracker obj
    return json.loads(str(tracker)) # returns json representation of tracker data

def find_coordinates(zip):
    gmaps = googlemaps.Client(key=os.getenv("GMAPS_KEY"))
    return gmaps.geocode("zip code" + zip)[0]['geometry']['location']

def get_last_update(tracker):
    last_update = tracker["tracking_details"][-1]
    coordinates = find_coordinates(last_update["tracking_location"]["zip"])
    last_update["tracking_location"]["coordinates"] = coordinates

    return last_update

def simplified_tracker_JSON(tracking_code, carrier): 
    try:
        tracker = create_tracker(tracking_code, carrier)
        data = {
            "error": False,
            "tracking_code": tracker["tracking_code"],
            "carrier": tracker["carrier"],
            "est_delivery_date": tracker["carrier_detail"]["est_delivery_date_local"],
            "est_delivery_time": tracker["carrier_detail"]["est_delivery_time_local"],
            "latest_update": get_last_update(tracker)
        }
        return json.dumps(data)
    except:
        return json.dumps({"error": True})


#print(simplified_tracker_JSON("EZ2000000002", "USPS"))