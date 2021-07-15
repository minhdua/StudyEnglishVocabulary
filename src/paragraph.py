class Paragraph():
    id=0;
    def __init__(self,topic):
        self.topic = topic

    def get_header(self):
         return [
            "Id",
            "Topic"
         ]

    def toList(self):
        return [
         self.id,
         self.topic]
