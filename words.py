from faker import Faker

fake = Faker()


class Words:
    def __init__(self):
        self.current_word_list = None
        self.word_count = None
        self.current_word = None
        self.word_list = None
        self.word_dict = None
        self.start()

    def get_unique_word(self):
        word = fake.word().lower()
        while word in self.word_list:
            word = fake.word().lower()
        self.word_list.append(word)

    def initialize_word_list(self):
        for _ in range(50):
            self.get_unique_word()

    def next_word(self):
        self.word_count += 1
        if len(self.word_list) - self.word_count == 15:  # More words are added if the list is short on them
            for _ in range(10):
                self.get_unique_word()
        self.current_word = self.word_list[self.word_count]

    def add_word_dict(self, user_word_input):
        self.word_dict[self.current_word] = user_word_input.replace(" ", '')  # removing white spaces
        self.next_word()

    def get_current_word_list(self):
        if self.current_word_list.index(self.current_word) == 11:
            self.current_word_list = self.word_list[self.word_count - 6:self.word_count + 9]
        return self.current_word_list

    def get_current_word(self):
        return self.current_word

    def start(self):
        self.word_list = []
        self.initialize_word_list()
        self.current_word = self.word_list[0]
        self.current_word_list = self.word_list[0:15]
        self.word_count = 0
        self.word_dict = {}

    def get_raw_char_num(self):
        raw_char_num = 0
        for word in self.word_dict:
            raw_char_num += len(self.word_dict[word])
        return raw_char_num

    def get_correct_char_num(self):
        correct_char_num = 0
        for word in self.word_dict:
            if word == self.word_dict[word]:
                correct_char_num += len(word)
        return correct_char_num
