import xml.sax as sax


class XmlReader(sax.ContentHandler):
    def __init__(self) -> None:
        super().__init__()
        self.table_data = []
        self.animal_data = []
        self.parser = sax.make_parser()

    def startElement(self, name, attrs):
        """
        Rewritten function from inherited class which use as start parser element
        :param name: current element name
        :param attrs: attributes (don't used)
        :return: None
        """
        self.current = name
        if name == "animal":
            pass

    def characters(self, content) -> None:
        """
        Also rewritten function that perform getting data characters
        :param content: character
        :return: None
        """
        if self.current == "name":
            self.name = content
        elif self.current == "date_birthday":
            self.date_birthday = content
        elif self.current == "date_last":
            self.date_last = content
        elif self.current == "doctor":
            self.doctor = content
        elif self.current == "diagnoz":
            self.diagnoz = content

    def endElement(self, name) -> None:
        """
        Rewritten function from inherited class which use as end parser element
        :param name:
        :return: None
        """
        if self.current == "name":
            self.animal_data.append(self.name)
        elif self.current == "date_birthday":
            self.animal_data.append(self.date_birthday)
        elif self.current == "date_last":
            self.animal_data.append(self.date_last)
        elif self.current == "doctor":
            self.animal_data.append(self.doctor)
        elif self.current == "diagnoz":
            self.animal_data.append(self.diagnoz)
        if len(self.animal_data) == 5:
            self.table_data.append(tuple(self.animal_data))
            self.animal_data = []

        self.current = ""
