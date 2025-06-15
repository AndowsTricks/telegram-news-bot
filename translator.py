
from googletrans import Translator

translator = Translator()

def translate_text(text, dest='si'):
    try:
        result = translator.translate(text, dest=dest)
        return result.text
    except Exception as e:
        print(f"Translate error: {e}")
        return text
