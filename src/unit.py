class Units():
    create_date = None
    update_date = None
    def __init__(self, unit_code,unit_topic):
        self.unit_code = unit_code
        self.unit_topic = unit_topic
    def get_header(self):
         return [
            "Unit Code",
            "Unit Topic"
         ]
# english
    def get_unit_code(self):
        return self.unit_code

    def set_unit_code(self, unit_code):
        self.unit_code = unit_code
# vietnamese
    def get_unit_topic(self):
        return self.unit_topic

    def set_unit_topic(self, unit_topic):
        self.unit_topic = unit_topic

# create_date
    def get_create_date(self):
        return self.create_date

    def set_create_date(self, create_date):
        self.create_date = create_date
# create_date
    def get_update_date(self):
        return self.update_date

    def set_update_date(self, update_date):
        self.update_date = update_date
        
    def toList(self):
        return [
         self.unit_code,
         self.unit_topic
        ]
