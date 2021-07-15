class Sentent():
    id=0;
    def __init__(self, english,vietnamese,paragraph_id,sentence_order):
        self.english = english
        self.vietnamese = vietnamese
        self.paragraph_id = paragraph_id
        self.sentence_order = sentence_order


    def get_header(self):
         return [
            "english",
            "vietnamese",
            "paragraph_id",
            "sentence_order"
         ]

    def toList(self):
        return [
         self.english,
         self.vietnamese,
         self.paragraph_id,
         self.sentence_order]
