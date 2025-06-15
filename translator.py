import requests

def translate_to_sinhala(text):
    try:
        response = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": "en",
                "tl": "si",
                "dt": "t",
                "q": text
            }
        )
        return response.json()[0][0][0]
    except:
        return "Sinhala translation unavailable."
