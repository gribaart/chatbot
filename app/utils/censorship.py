class Censorship:
    banned_words_list = ["", "", "", "", "", "", ""]

    def is_output_safe(self, text):
        for word in self.banned_words_list:
            if word in text:
                return False
        return True

    def get_words_blacklist(self):
        return self.banned_words_list
    

