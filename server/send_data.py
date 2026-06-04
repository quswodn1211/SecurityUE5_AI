import json
import os
from typing import Any
from urllib import error, request


DEFAULT_TIMEOUT_SECONDS = 10
data_num = 0

def get_web_server_url() -> str | None:
    return os.getenv("WEB_SERVER_ANALYSIS_URL", "http://ec2-13-124-52-143.ap-northeast-2.compute.amazonaws.com:8000/api/detect/analyze") or os.getenv("AWS_WEB_SERVER_ANALYSIS_URL")


def send_analysis_result(
    result: dict[str, Any],
    url: str | None = None,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    global data_num
    target_url = url or get_web_server_url()
    if not target_url:
        return {
            "forwarded": False,
            "reason": "WEB_SERVER_ANALYSIS_URL is not configured.",
        }
    data_num += 1
    if data_num % 5 != 0:  # Forward only 1 out of every 5 data points
        return {
            "forwarded": False,
            "reason": "not ..1 th data",
        }
    
    body = json.dumps(result, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        target_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=timeout) as response:
            response_body = response.read().decode("utf-8")
            parsed_body: Any
            try:
                parsed_body = json.loads(response_body) if response_body else None
            except json.JSONDecodeError:
                parsed_body = response_body

            return {
                "forwarded": 200 <= response.status < 300,
                "status_code": response.status,
                "response": parsed_body,
            }
    except error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        return {
            "forwarded": False,
            "status_code": exc.code,
            "error": response_body,
        }
    except error.URLError as exc:
        return {
            "forwarded": False,
            "error": str(exc.reason),
        }
