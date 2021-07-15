class NewWords():
    pronounce = None
    right_times = 0
    wrong_times = 0
    unit_code = None
    description=None
    synonymous = None
    antonym = None 
    units_contain = None
    create_date = None
    last_study_date = None
    def __init__(self, order,english,vietnamese,type_word,sentent_english,sentent_vietnamese,unit_code,description,synonymous,antonym,units_contain):
        self.order = order
        self.english = english
        self.vietnamese = vietnamese
        self.type_word = type_word
        self.sentent_english = sentent_english
        self.sentent_vietnamese = sentent_vietnamese
        self.unit_code = unit_code
        self.description
        self.synonymous
        self.antonym
        self.units_contain

    def get_header(self):
         return [
            "Order",
            "English",
            "VietNamese",
            "Type_Word",
            "Sample_English",
            "Sample_Vietnamese",
            "Unit Code",
            "Pronounce",
            "Right Time",
            "Wrong Time",
            "create_date",
            "last_study_date"
         ]
# order
    def get_order(self):
        return self.order

    def set_order(self, order):
        self.order = order

# english
    def get_english(self):
        return self.english

    def set_english(self, english):
        self.english = english
# vietnamese
    def get_vietnamese(self):
        return self.vietnamese

    def set_vietnamese(self, vietnamese):
        self.vietnamese = vietnamese
# type_word
    def get_type_word(self):
        return self.type_word

    def set_type_word(self, type_word):
        self.type_word = type_word
# sentent_english
    def get_sentent_english(self):
        return self.sentent_english

    def set_sentent_english(self, sentent_english):
        self.sentent_english = sentent_english
# sentent_vietnamese
    def get_sentent_vietnamese(self):
        return self.sentent_vietnamese

    def set_sentent_vietnamese(self, sentent_vietnamese):
        self.sentent_vietnamese = sentent_vietnamese

# unit_code
    def get_unit_code(self):
        return self.unit_code

    def set_unit_code(self, unit_code):
        self.unit_code = unit_code
# pronounce
    def get_pronounce(self):
        return self.pronounce

    def set_pronounce(self, pronounce):
        self.pronounce = pronounce
# right_times
    def get_right_times(self):
        return self.right_times

    def set_right_times(self, right_times):
        self.right_times = right_times

# right_times
    def get_wrong_times(self):
        return self.right_times

    def set_wrong_times(self, right_times):
        self.right_times = right_times

# create_date
    def get_create_date(self):
        return self.create_date

    def set_create_date(self, create_date):
        self.create_date = create_date

# last_study_date
    def get_last_study_date(self):
        return self.last_study_date

    def set_last_study_date(self, last_study_date):
        self.last_study_date = last_study_date

# unit_code
    def get_unit_code(self):
        return self.unit_code

    def set_unit_code(self, last_study_date):
        self.unit_code = unit_code

    def toList(self):
        return [
         self.order,
         self.english,
         self.vietnamese,
         self.type_word,
         self.sentent_english,
         self.sentent_vietnamese,
         self.pronounce,
         self.right_times,
         self.create_date,
         self.last_study_date]

    def __str__(self):
        return "english="+ str(self.english)+"-vietnamese="+str(self.vietnamese)+"-type_word="+str(self.type_word)+"-sentent_english="+str(self.sentent_english)+"-sentent_vietnamese="+str(self.sentent_vietnamese)+"-pronounce="+str(self.pronounce)+"-right_times="+str(self.right_times)+"-create_date="+str(self.create_date)+"-last_study_date="+str(self.last_study_date)
