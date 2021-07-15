class WordParagraph():
    id=0;
    def __init__(self, english,vietnamese,paragraph_id,number_of):
        self.english = english
        self.vietnamese = vietnamese
        self.paragraph_id = paragraph_id
        self.number_of = number_of


    def get_header(self):
         return [
            "english",
            "vietnamese",
            "paragraph_id",
            "number_of"
         ]

    def toList(self):
        return [
         self.english,
         self.vietnamese,
         self.paragraph_id,
         self.number_of]
