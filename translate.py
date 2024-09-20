from googletrans import Translator

class LangTranslator():
    def __init__(self):
        self.translator = Translator(service_urls=['translate.googleapis.com'])

    def translate_to_native(self, english_txt, native_language):
        return self.translator.translate(english_txt, dest=native_language).text
    
    def translate_to_english(self, native_txt, native_language):
        return self.translator.translate(native_txt, src=native_language, dest='en').text
