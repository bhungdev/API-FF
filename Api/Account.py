import requests
import Proto.compiled.MajorLogin_pb2
from Utilities.until import encode_protobuf, decode_protobuf
import json
from Configuration.APIConfiguration import RELEASEVERSION


def get_garena_token(uid, password):
    """
    Get Garena token using uid and password
    
    Args:
        uid (str): User ID
        password (str): Password
    
    Returns:
        dict: JSON response from the API
    """
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"

    payload = {
        'uid': uid,
        'password': password,
        'response_type': "token",
        'client_type': "2",
        'client_secret': "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        'client_id': "100067"
    }

    headers = {
        'User-Agent': "GarenaMSDK/4.0.19P9(A063 ;Android 13;en;IN;)",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return None



def get_major_login(logintoken, openid):
    """
    Perform major login with the provided credentials
    """

    import requests, json
    print("🔍 [DEBUG] Start MajorLogin")
    print("🔍 logintoken:", str(logintoken)[:25], "...")
    print("🔍 openid:", openid)

    try:
        # Create encrypted payload
        encrypted_payload = encode_protobuf({
            "openid": openid,
            "logintoken": logintoken,
            "platform": "4",
        }, Proto.compiled.MajorLogin_pb2.request())

        url = "https://loginbp.ggblueshark.com/MajorLogin"
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 13; A063 Build/TKQ1.221220.001)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/octet-stream",
            'Expect': "100-continue",
            'Authorization': "Bearer",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': RELEASEVERSION,
        }

        print("🌐 Sending POST to:", url)
        response = requests.post(url, data=encrypted_payload, headers=headers)
        print("🧾 Raw response status:", response.status_code)
        print("🧾 Raw response body (first 300 chars):", response.content[:300])

        # Decode protobuf
        try:
            message = decode_protobuf(response.content, Proto.compiled.MajorLogin_pb2.response)
            print("✅ Decoded MajorLogin:", message)
            return message
        except Exception as e:
            print("❌ Decode error:", str(e))
            print("🧾 Raw text fallback:", response.text)
            return {"error": "decode_failed", "raw": response.text}

    except Exception as e:
        print("❌ Exception in get_major_login():", str(e))
        return {"error": str(e)}
