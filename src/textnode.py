from enum import Enum

class TEXTTYPE(Enum):
    NORMAL = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"

class TextNode:
    def __init__(self, text, TEXTTYPE, url=None):
        self.text = text
        self.text_type = TEXTTYPE
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False
        
    def __repr__(self):
        print(f"TextNode({self.text}, {self.text_type.value}, {self.url})")
    

