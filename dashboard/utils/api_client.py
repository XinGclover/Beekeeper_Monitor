import requests
from dashboard.utils.config import get_api_base_url


API_BASE_URL = get_api_base_url()

def fetch_json(
    path: str,
    method: str = "GET",
    params: dict | None = None,
    json: dict | None = None,
):
    url = f"{API_BASE_URL}{path}"

    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, params=params, json=json, timeout=30)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        raise RuntimeError(f"API request failed: {exc}") from exc