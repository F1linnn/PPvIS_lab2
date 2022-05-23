# parsers
from kivymd.uix.snackbar import Snackbar

from Utility.parsers.dom_writer import XmlWriter
from Utility.parsers.sax_reader import XmlReader


class VetScreenModel:
    _not_filtered = []

    def __init__(self, table):
        self.table = table
        self.dialog = None
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, data):
        for x in self._observers:
            x.model_is_changed(data)

    def read_from_file(self, file_name: str) -> None:
        """
        Read data from XML file
        :param file_name: XML file name
        :return: None
        """
        try:
            reader = XmlReader()
            reader.parser.setContentHandler(reader)
            reader.parser.parse("xml/" + file_name)
            for data in reader.table_data:
                self.add_new_animal(data)
        except Exception as e:
            print(e)
            exit()
            pass

    @staticmethod
    def create_empty_file(path):
        try:
            with open(path, 'w'):
                pass
            return True
        except Exception as e:
            return False

    def write_to_file(self, path: str):
        path = "xml/" + path
        if self.create_empty_file(path):
            dom = XmlWriter(path)
            data_dict = {}
            for row in self.table.row_data:
                data_dict["name"] = row[0]
                data_dict["date_birthday"] = row[1]
                data_dict["date_last"] = row[2]
                data_dict["doctor"] = row[3]
                data_dict["diagnoz"] = row[4]

                dom.create_animal(data_dict)
            dom.create_xml_file()

    def add_new_animal(self, row):
        try:
            self.table.row_data.append(
                (
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                )
            )
        except ValueError as v:
            Snackbar(text="Data inserting error").open()

    def refresh_animal_in_table(self):
        try:
            self.table.row_data += self._not_filtered
            self._not_filtered = []
        except Exception as e:
            pass

    def select_animal_by_filters(self, filters: list):
        not_filtered_animal = []
        for row in self.table.row_data:
            # first case
            if filters[0] or filters[1]:  # name and date
                name = row[0]
                filter_name = filters[0]
                if not (name == filter_name or row[1] == filters[1]):
                    not_filtered_animal.append(tuple(row))
                    print(len(not_filtered_animal))
                    continue
            # second case
            elif filters[2] or filters[3]:
                if not (row[2] == filters[2] or row[3] == filters[3]):
                    not_filtered_animal.append(tuple(row))
                continue
            # third case
            elif filters[4]:
                if not (row[4] == filters[4]):
                    not_filtered_animal.append(tuple(row))
                continue
        return not_filtered_animal

    def filter_animal_in_table(self, filters: list):
        self._not_filtered = self.select_animal_by_filters(filters=filters)
        for row in self._not_filtered:
            self.table.row_data.remove(row)

    @staticmethod
    def empty_filters(filters):
        for filter in filters:
            if filter != '':
                return False
        return True

    def delete_animal_from_table(self, filters):
        ''' delete a animals that are in _not_filtered list '''
        count_to_delete = 0
        if self.empty_filters(filters):
            return count_to_delete
        unselected_animals = self.select_animal_by_filters(filters=filters)
        for row in self.table.row_data[:]:
            if row not in unselected_animals:
                try:
                    self.table.row_data.remove(row)
                    count_to_delete += 1
                except Exception as e:
                    Snackbar(text="No such animals").open()
                    pass
        return count_to_delete
