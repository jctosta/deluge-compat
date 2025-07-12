"""Built-in Deluge functions."""

import requests
import base64
import urllib.parse
import random
import math
from typing import Any, Dict, Union, Optional
from .types import Map, List, DelugeString, deluge_string


def getUrl(
    url: str, simple: bool = True, headers: Optional[Dict[str, str]] = None
) -> Union[str, Map]:
    """Perform a GET request to URL."""
    try:
        response = requests.get(url, headers=headers or {})
        if simple:
            return deluge_string(response.text)
        else:
            return Map(
                {
                    "status_code": response.status_code,
                    "text": response.text,
                    "headers": dict(response.headers),
                }
            )
    except Exception as e:
        if simple:
            return deluge_string("")
        else:
            return Map({"error": str(e)})


def postUrl(
    url: str,
    body: Optional[Map] = None,
    headers: Optional[Map] = None,
    simple: bool = True,
) -> Union[str, Map]:
    """Perform a POST request to URL."""
    try:
        post_headers = dict(headers) if headers else {}
        post_data = dict(body) if body else {}

        response = requests.post(url, json=post_data, headers=post_headers)
        if simple:
            return deluge_string(response.text)
        else:
            return Map(
                {
                    "status_code": response.status_code,
                    "text": response.text,
                    "headers": dict(response.headers),
                }
            )
    except Exception as e:
        if simple:
            return deluge_string("")
        else:
            return Map({"error": str(e)})


def encodeUrl(url: str) -> DelugeString:
    """URL encode a string."""
    return deluge_string(urllib.parse.quote(url))


def urlEncode(url: str) -> DelugeString:
    """Alias for encodeUrl."""
    return encodeUrl(url)


def urlDecode(url: str) -> DelugeString:
    """URL decode a string."""
    return deluge_string(urllib.parse.unquote(url))


def base64Encode(text: str) -> DelugeString:
    """Base64 encode a string."""
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    return deluge_string(encoded_bytes.decode("utf-8"))


def base64Decode(text: str) -> DelugeString:
    """Base64 decode a string."""
    try:
        decoded_bytes = base64.b64decode(text.encode("utf-8"))
        return deluge_string(decoded_bytes.decode("utf-8"))
    except Exception:
        return deluge_string("")


def aesEncode(key: str, text: str) -> DelugeString:
    """AES encrypt text (simplified implementation)."""
    # This is a placeholder - real AES encryption would require cryptography library
    import hashlib

    hash_key = hashlib.md5(key.encode()).hexdigest()
    # Simple XOR-based "encryption" for demo purposes
    result = ""
    for i, char in enumerate(text):
        result += chr(ord(char) ^ ord(hash_key[i % len(hash_key)]))
    return deluge_string(base64.b64encode(result.encode()).decode())


def aesDecode(key: str, encrypted_text: str) -> DelugeString:
    """AES decrypt text (simplified implementation)."""
    try:
        import hashlib

        hash_key = hashlib.md5(key.encode()).hexdigest()
        decoded = base64.b64decode(encrypted_text.encode()).decode()
        result = ""
        for i, char in enumerate(decoded):
            result += chr(ord(char) ^ ord(hash_key[i % len(hash_key)]))
        return deluge_string(result)
    except Exception:
        return deluge_string("")


def abs_func(number: Union[int, float]) -> Union[int, float]:
    """Absolute value of a number."""
    return abs(number)


def cos_func(number: Union[int, float]) -> float:
    """Cosine of an angle."""
    return math.cos(number)


def sin_func(number: Union[int, float]) -> float:
    """Sine of an angle."""
    return math.sin(number)


def tan_func(number: Union[int, float]) -> float:
    """Tangent of an angle."""
    return math.tan(number)


def log_func(number: Union[int, float]) -> float:
    """Natural logarithm."""
    return math.log(number)


def min_func(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Minimum of two numbers."""
    return min(a, b)


def max_func(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Maximum of two numbers."""
    return max(a, b)


def exp_func(number: Union[int, float]) -> float:
    """Exponential function (e^x)."""
    return math.exp(number)


def power_func(
    base: Union[int, float], exponent: Union[int, float]
) -> Union[int, float]:
    """Power function."""
    return pow(base, exponent)


def round_func(number: float, decimals: int = 0) -> float:
    """Round a number to specified decimal places."""
    return round(number, decimals)


def sqrt_func(number: Union[int, float]) -> float:
    """Square root."""
    return math.sqrt(number)


def toDecimal(number: int) -> float:
    """Convert integer to decimal."""
    return float(number)


def toHex(number: int) -> str:
    """Convert integer to hexadecimal."""
    return hex(number)


def ceil_func(number: float) -> int:
    """Ceiling function."""
    return math.ceil(number)


def floor_func(number: float) -> int:
    """Floor function."""
    return math.floor(number)


def randomNumber(max_value: int = 2000000000, min_value: int = 0) -> int:
    """Generate a random number."""
    return random.randint(min_value, max_value - 1)


def info(*args) -> None:
    """Log information (equivalent to Deluge's info statement)."""
    print("INFO:", *args)


def sendemail(*args, **kwargs) -> Map:
    """Placeholder for sending email."""
    return Map({"status": "email_sent"})


def sendsms(*args, **kwargs) -> Map:
    """Placeholder for sending SMS."""
    return Map({"status": "sms_sent"})


def pushNotification(*args, **kwargs) -> Map:
    """Placeholder for push notification."""
    return Map({"status": "notification_sent"})


def Collection() -> Map:
    """Create a new Collection (which can hold List or Map)."""
    return Map()


def ifnull(value: Any, default: Any) -> Any:
    """Return default if value is None/null."""
    return default if value is None else value


def replaceAll(text: str, search: str, replace: str) -> DelugeString:
    """Replace all occurrences in string."""
    return deluge_string(text.replace(search, replace))


# Create aliases for math functions to match Deluge naming
BUILTIN_FUNCTIONS = {
    "getUrl": getUrl,
    "postUrl": postUrl,
    "encodeUrl": encodeUrl,
    "urlEncode": urlEncode,
    "urlDecode": urlDecode,
    "base64Encode": base64Encode,
    "base64Decode": base64Decode,
    "aesEncode": aesEncode,
    "aesDecode": aesDecode,
    "abs": abs_func,
    "cos": cos_func,
    "sin": sin_func,
    "tan": tan_func,
    "log": log_func,
    "min": min_func,
    "max": max_func,
    "exp": exp_func,
    "power": power_func,
    "round": round_func,
    "sqrt": sqrt_func,
    "toDecimal": toDecimal,
    "toHex": toHex,
    "ceil": ceil_func,
    "floor": floor_func,
    "randomNumber": randomNumber,
    "info": info,
    "sendemail": sendemail,
    "sendsms": sendsms,
    "pushNotification": pushNotification,
    "Collection": Collection,
    "Map": Map,
    "List": List,
    "ifnull": ifnull,
    "replaceAll": replaceAll,
}
