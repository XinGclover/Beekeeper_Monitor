import os
import time
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


# 1. Health check(Cold start waiting)

def wait_for_backend(max_wait: int = 60, interval: int = 2) -> bool:
    health_url = f"{API_BASE_URL}/health"
    start = time.time()

    while time.time() - start < max_wait:
        try:
            response = requests.get(health_url, timeout=5)
            response.raise_for_status()
            return True
        except requests.RequestException:
            time.sleep(interval)

    return False



# 2. General request method

def request_json(
    method: str,
    path: str,
    params: dict | None = None,
    json: dict | None = None,
    retries: int = 4,
    timeout: int = 20,
):
    url = f"{API_BASE_URL}{path}"
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=json,
                timeout=timeout,
            )
            response.raise_for_status()

            # Some APIs may not return JSON
            if response.text:
                return response.json()
            return None

        except requests.RequestException as e:
            last_error = e

            if attempt < retries:
                wait_seconds = 2 * attempt
                time.sleep(wait_seconds)
            else:
                raise RuntimeError(
                    f"{method} request failed after {retries} attempts: {url}"
                ) from last_error



# 3. Semantic encapsulation 

def get_json(path: str, params: dict | None = None, **kwargs):
    return request_json("GET", path, params=params, **kwargs)


def post_json(path: str, data: dict | None = None, **kwargs):
    return request_json("POST", path, json=data, **kwargs)


def put_json(path: str, data: dict | None = None, **kwargs):
    return request_json("PUT", path, json=data, **kwargs)


def delete_json(path: str, **kwargs):
    return request_json("DELETE", path, **kwargs)


# Alias for semantic clarity
fetch_json = get_json