import json
from datetime import datetime

class ProgressModule():
    def __init__(self):
        self.data_path = 'progress_data.json'
        with open(self.data_path, 'r') as file:
            self.progress_data = json.load(file)

    def get_occurance_probability(self, word):
        day1 = self.progress_data[word]["day1"]["num_correct"] / (self.progress_data[word]["day1"]["num_correct"] + self.progress_data[word]["day1"]["num_wrong"])
        day2 = self.progress_data[word]["day2"]["num_correct"] / (self.progress_data[word]["day2"]["num_correct"] + self.progress_data[word]["day2"]["num_wrong"])
        day3 = self.progress_data[word]["day3"]["num_correct"] / (self.progress_data[word]["day3"]["num_correct"] + self.progress_data[word]["day3"]["num_wrong"])
        day4 = self.progress_data[word]["day4"]["num_correct"] / (self.progress_data[word]["day4"]["num_correct"] + self.progress_data[word]["day4"]["num_wrong"])
        return 1 - ((day1 * 0.05) + (day2 * 0.1) + (day3 * 0.25) + (day4 * 0.6))
    
    def set_accuracy(self, word, day_number, num_correct, num_wrong):
        self.progress_data[word]["day" + str(day_number)]["num_correct"] = self.progress_data[word]["day" + str(day_number)]["num_correct"] + num_correct
        self.progress_data[word]["day" + str(day_number)]["num_wrong"] = self.progress_data[word]["day" + str(day_number)]["num_wrong"] + num_wrong
        with open(self.data_path, 'w') as file:
            json.dump(self.progress_data, file)
    
    def update_latest(self, word):
        current_date = str(datetime.now()).split(' ')[0]
        last_date = self.progress_data[word]["day5"]["date"]
        if datetime.strptime(last_date, "%Y-%m-%d").date() < datetime.strptime(current_date, "%Y-%m-%d").date():
            self.progress_data[word]["day1"]["date"] = self.progress_data[word]["day2"]["date"]
            self.progress_data[word]["day2"]["date"] = self.progress_data[word]["day3"]["date"]
            self.progress_data[word]["day3"]["date"] = self.progress_data[word]["day4"]["date"]
            self.progress_data[word]["day4"]["date"] = self.progress_data[word]["day5"]["date"]
            self.progress_data[word]["day1"]["num_correct"] = self.progress_data[word]["day2"]["num_correct"]
            self.progress_data[word]["day2"]["num_correct"] = self.progress_data[word]["day3"]["num_correct"]
            self.progress_data[word]["day3"]["num_correct"] = self.progress_data[word]["day4"]["num_correct"]
            self.progress_data[word]["day4"]["num_correct"] = self.progress_data[word]["day5"]["num_correct"]
            self.progress_data[word]["day1"]["num_wrong"] = self.progress_data[word]["day2"]["num_wrong"]
            self.progress_data[word]["day2"]["num_wrong"] = self.progress_data[word]["day3"]["num_wrong"]
            self.progress_data[word]["day3"]["num_wrong"] = self.progress_data[word]["day4"]["num_wrong"]
            self.progress_data[word]["day4"]["num_wrong"] = self.progress_data[word]["day5"]["num_wrong"]
            self.progress_data[word]["day5"]["date"] = current_date
            self.progress_data[word]["day5"]["num_correct"] = 1
            self.progress_data[word]["day5"]["num_wrong"] = 1
        with open(self.data_path, 'w') as file:
            json.dump(self.progress_data, file)
    
    def hasWord(self, word):
        try:
            self.progress_data[word]
            return True
        except:
            return False

    
    def gen_index(self, word):
        self.progress_data[word] = {}
        for day in range(1,6):
            self.progress_data[word]["day" + str(day)] = {}
            self.progress_data[word]["day" + str(day)]["num_correct"] = 1
            self.progress_data[word]["day" + str(day)]["num_wrong"] = 1
            self.progress_data[word]["day" + str(day)]["date"] = str(datetime.now()).split(' ')[0]
        with open(self.data_path, 'w') as file:
            json.dump(self.progress_data, file)


