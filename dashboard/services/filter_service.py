from dashboard.utils.api_client import get_json


def get_filter_options(location_id=None, apiary_id=None, hive_id=None):
    """
    Fetch hierarchical filter options via API.
    
    Returns a dictionary with locations, apiaries, hives, and sensors
    based on the provided filter parameters.
    """
    params = {}
    if location_id is not None:
        params["location_id"] = location_id
    if apiary_id is not None:
        params["apiary_id"] = apiary_id
    if hive_id is not None:
        params["hive_id"] = hive_id

    response = get_json("/api/monitoring/locations/filter-options", params=params)
    if not response:
        return {
            "locations": [],
            "apiaries": [],
            "hives": [],
            "sensors": [],
        }
    return response

