import os
import re

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.screen import Screen
from kivymd.uix.snackbar import Snackbar

import Utility.dialog_windows as window


class VetScreenView(MDScreen):
    controller = ObjectProperty()
    model = ObjectProperty()

    def __init__(self, **kw):
        super().__init__(**kw)
        self.model.add_observer(self)
        self.screen = Screen()
        self.dialog = None

    def open_dialog(self, mode: str):
        """ Call input, filter and delete windows, save and upload """
        if mode == "input":
            self.dialog = window.InputWindow(model=self.model, controller=self.controller)
        elif mode == "filter":
            self.dialog = window.FilterWindow(model=self.model, controller=self.controller)
        elif mode == "delete":
            self.dialog = window.DeleteWindow(model=self.model, controller=self.controller)
        elif mode == "upload":
            self.dialog = window.UploadWindow(model=self.model, controller=self.controller)
        elif mode == "save":
            self.dialog = window.SaveWindow(model=self.model, controller=self.controller)

        self.dialog.open()
        self.controller.dialog(mode, self.dialog)

    def close_dialog(self, dialog_data: list = []):
        check = re.search(r'\d{2}\.\d{2}\.\d{4}', dialog_data[1])
        check2 = re.search(r'\d{2}\.\d{2}\.\d{4}', dialog_data[2])
        if self.dialog.mode == "input":
            if check is not None and check2 is not None:
                    self.controller.input_animal(dialog_data)
            else:
                Snackbar(text=f"Uncorrect type date(dd.mm.yyyy)").open()
        elif self.dialog.mode == "filter":
                self.controller.filter_animals(dialog_data)
        elif self.dialog.mode == "delete":
            unlucky = self.controller.delete_animals(dialog_data)
            Snackbar(text=f"{unlucky} animals are deleted!").open()
        elif self.dialog.mode == "upload":
            self.controller.upload_from_file(dialog_data)
        elif self.dialog.mode == "save":
            self.controller.save_in_file(dialog_data)
        self.dialog = None
    def model_is_changed(self, data):
        """ The method is called when the model changes. """
        self.close_dialog(data)

    def refresh(self):
        self.controller.refresh()

    def build(self):
        self.add_widget(self.model.table)
        return self


Builder.load_file(os.path.join(os.path.dirname(__file__), "vetscreen.kv"))
