import openai
#DONT SHARE THIS KEY WITH ANYONE PLZZZZZ
openai.api_key = '<API_KEY>'

#Use GPT to generate a certain number of words from given EL level
class VocabGenerator():
    def __init__(self, vocab_level):
        self.vocab_level = vocab_level
    
    #Returns an array of generated words
    #works for num_words > 1
    def generateWords(self, num_words):
        prompt = "Generate " + str(num_words) + " " + self.vocab_level + " words"
        response = self.comp(prompt)
        words = []
        meta = ''.join([i for i in response.replace('\n', ' ') if not i.isdigit()]).strip().split('.')
        for string in meta:
            if string != '':
                words.append(string.strip())
        return words
    
    # function that takes in string argument as parameter
    def comp(self, PROMPT):
        # using OpenAI's Completion module that helps execute 
        # any tasks involving text
        response = openai.Completion.create(
            # model name used here is text-davinci-003
            # there are many other models available under the 
            # umbrella of GPT-3
            model="text-davinci-003",
            # passing the user input 
            prompt=PROMPT,
            max_tokens=1000,
        )
        return response['choices'][0]['text'].strip() if len(response['choices']) != 0 else None



