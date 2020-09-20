#!/usr/bin/python
# -*- coding: utf-8 -*-
from Tkinter import *
import yaml
from pepper.robot import Pepper
import numpy as np
from pepper import teleoperation


class Configuration:

    def __init__(self, config_file="./conf.yaml"):
        self.config_file = config_file
        self.conf = yaml.safe_load(open(self.config_file))


class PepperController:

    def __init__(self, root):
        self.configuration = Configuration()
        self.robot = None
        self.language = self.configuration.conf["language"]["lang"]

        self.root = root
        self.root.option_add('*Font', 'Arial 12')
        self.root.geometry("1000x800")
        self.root.title("Pepper Controller " + self.configuration.conf["configuration"]["version"])
        self.root.bind('<Escape>', lambda e: root.destroy())
        self.root.resizable(True, True) 

        self.group_connection = LabelFrame(root, text="Připojení")
        self.group_connection.grid(row=0, column=0, columnspan=4, rowspan=2, padx=5, pady=5)

        self.entry_address = Entry(self.group_connection)
        self.entry_port = Entry(self.group_connection)
        if self.configuration.conf["configuration"]["virtual"]:
            self.entry_address.insert(END, "localhost")
            self.entry_port.insert(END, "34223")
        else:
            self.entry_address.insert(END, self.configuration.conf["configuration"]["default_ip"])
            self.entry_port.insert(END, self.configuration.conf["configuration"]["default_port"])
        self.label_address = Label(self.group_connection, text="IP adresa")
        self.label_port = Label(self.group_connection, text="Port")
        self.button_connect = Button(self.group_connection, text="Připojit", command=self.connect)

        self.label_address.grid(row=0, column=0, sticky="nse")
        self.entry_address.grid(row=0, column=1)
        self.label_port.grid(row=1, column=0, sticky="nse")
        self.entry_port.grid(row=1, column=1)
        self.button_connect.grid(row=1, column=2)

        self.group_interaction = LabelFrame(root, text="Interaktivní režim")
        self.group_interaction.grid(row=2, column=0, columnspan=16, rowspan=2, padx=5, pady=5)
        self.button_say_no = Button(self.group_interaction, text="Ne", command=lambda: self.robot.say(
                                         str(np.random.choice(
                                             self.configuration.conf["language"][self.language]["no_list"]).encode("utf-8"))))
        self.button_say_yes = Button(self.group_interaction, text="Ano",
                                     command=lambda: self.robot.say(
                                         str(np.random.choice(
                                             self.configuration.conf["language"][self.language]["yes_list"]).encode("utf-8"))))
        self.button_say_dont_know = Button(self.group_interaction, text="Nevím", command=lambda: self.robot.say(
                                         str(np.random.choice(
                                             self.configuration.conf["language"][self.language]["dont_know_list"]).encode("utf-8"))))
        self.button_say_hello = Button(self.group_interaction, text="Pozdrav", command=lambda: self.robot.say(
                                         str(np.random.choice(
                                             self.configuration.conf["language"][self.language]["hello"]).encode("utf-8"))))
        self.button_pozvanka = Button(self.group_interaction, text="Pozvánka", command=lambda: self.invitation())
        self.button_slosovani = Button(self.group_interaction, text="Slosování", command=lambda: self.robot.say(
                                         str(np.random.choice(
                                             self.configuration.conf["language"][self.language]["slosovani"]).encode("utf-8"))))
        self.button_say_name = Button(self.group_interaction, text="Jsem Tony", command=lambda: self.robot.say(
            str(np.random.choice(
                self.configuration.conf["language"][self.language]["name"]).encode("utf-8"))))
        self.entry_say_text = Text(self.group_interaction, height= 4, width=150)
        self.entry_say_text.insert(END, self.configuration.conf["configuration"]["default_sentence"])
        self.button_say_custom_text = Button(self.group_interaction, text="Říct text", command=lambda: self.robot.say(
                                         self.entry_say_text.get("1.0",END).encode("utf-8")))
        self.button_stavitel = Button(self.group_interaction, text="Panatt.stavitel",  command=lambda: self.robot.say(
                                         str(np.random.choice(
                                             self.configuration.conf["language"][self.language]["stavitel"]).encode("utf-8"))))
        self.button_breeam = Button(self.group_interaction, text="BREEAM",  command=lambda: self.robot.say(
                                         str(np.random.choice(
                                             self.configuration.conf["language"][self.language]["breeam"]).encode("utf-8"))))
        self.button_wave = Button(self.group_interaction, text="Zamávej", command=lambda: self.robot.start_animation(
            np.random.choice(["Hey_1", "Hey_3", "Hey_4", "Hey_6"])
        ))
        self.button_specialista = Button(self.group_interaction, text="Panatt.specialista", command=lambda: self.robot.say(
                                         str(np.random.choice(
                                             self.configuration.conf["language"][self.language]["specialista"]).encode("utf-8"))))
        self.button_oceneni = Button(self.group_interaction, text="Panatt.ocenění", command=lambda: self.robot.say(
                                         str(np.random.choice(
                                             self.configuration.conf["language"][self.language]["oceneni"]).encode("utf-8"))))
        self.button_blinking = Button(self.group_interaction, text="Blikání", command=lambda: self.robot.autonomous_blinking())
        self.button_obraz = Button(self.group_interaction, text="Obraz", command=lambda: self.robot.streamCamera())

        self.entry_say_text.grid(row=0, column=0, columnspan=6, sticky=NSEW)

        # row 1
        self.button_say_custom_text.grid(row=1, column=0, sticky=NSEW)
        self.button_say_name.grid(row=1, column=1, sticky=NSEW)
        self.button_say_hello.grid(row=1, column=2, sticky=NSEW)
        self.button_wave.grid(row=1, column=3, sticky=NSEW)

        #row 2
        self.button_say_yes.grid(row=2, column=0, sticky=NSEW)
        self.button_say_no.grid(row=2, column=1, sticky=NSEW)
        self.button_say_dont_know.grid(row=2, column=2, sticky=NSEW)
        self.button_blinking.grid(row=2, column=3, sticky=NSEW)

        #row 3
        self.button_pozvanka.grid(row=3, column=0, sticky=EW)
        self.button_breeam.grid(row=3, column=1, sticky=NSEW)
        self.button_stavitel.grid(row=3, column=2, sticky=NSEW)
        self.button_specialista.grid(row=3, column=3, sticky=NSEW)

        #row 4
        self.button_slosovani.grid(row=4, column=0, sticky=EW)
        self.button_oceneni.grid(row=4, column=1, sticky=NSEW)
        self.button_obraz.grid(row=4, column=2, sticky=NSEW)


        self.group_tool = LabelFrame(root, text="Nástroje")
        self.group_tool.grid(row=4, column=0, columnspan=2, rowspan=3, padx=5, pady=5)

        self.button_switch_al = Button(self.group_tool, text="Autonomní režim",
                                       command=lambda: self.robot.autonomous_life())
        self.button_battery = Button(self.group_tool, text="Stav baterie", command=lambda: self.robot.battery_status())
        self.button_stop_all = Button(self.group_tool, text="Ukonči aplikace", command=lambda: self.robot.stop_behaviour())
        self.button_show_web = Button(self.group_tool, text="Zobraz logo", comman=lambda: self.robot.show_image(self.configuration.conf["configuration"]["logo"]))
        self.button_web_reset = Button(self.group_tool, text="Reset tablet", command=lambda: self.robot.reset_tablet())
        self.language_button_cz = Button(self.group_tool, text="Nastav češtinu", command=lambda: self.change_language("cz"))
        self.language_button_en = Button(self.group_tool, text="Nastav angličtinu", command=lambda: self.change_language("en"))
        self.show_invitation = Button(self.group_tool, text="Zobraz pozvánku", comman=lambda: self.robot.show_image(self.configuration.conf["configuration"]["pozvanka"]))
        self.awareness_on = Button(self.group_tool, text="Awareness On", command=lambda: self.robot.set_awareness(on=True))
        self.awareness_off = Button(self.group_tool, text="Awareness Off", command=lambda: self.robot.set_awareness(on=False))

        self.button_switch_al.grid(row=0, column=0, sticky=EW)
        self.button_battery.grid(row=0, column=1, sticky=EW)
        self.button_stop_all.grid(row=1, column=0, sticky=EW)
        self.button_show_web.grid(row=1, column=1, sticky=EW)
        self.language_button_cz.grid(row=2, column=0, sticky=EW)
        self.button_web_reset.grid(row=2, column=1, sticky=EW)
        self.language_button_en.grid(row=3, column=0, sticky=EW)
        self.show_invitation.grid(row=3, column=1, sticky=EW)
        self.awareness_off.grid(row=4, column=0, sticky=EW)
        self.awareness_on.grid(row=4, column=1, sticky=EW)

        self.group_application = LabelFrame(root, text="Aplikace")
        self.group_application.grid(row=4, column=2, columnspan=1, rowspan=1, padx=5, pady=5, sticky=NSEW)

        self.button_app_1 = Button(self.group_application, text=self.configuration.conf["application_1"]["name"], command=lambda: self.robot.start_behavior(self.configuration.conf["application_1"]["package"]))
        self.button_app_2 = Button(self.group_application, text="Tancuj", command=lambda: self.robot.dance())
        self.button_app_3 = Button(self.group_application, text=self.configuration.conf["application_3"]["name"], command=lambda: self.robot.start_behavior(self.configuration.conf["application_3"]["package"]))
        self.button_app_4 = Button(self.group_application, text=self.configuration.conf["application_4"]["name"], command=lambda: self.robot.start_behavior(self.configuration.conf["application_4"]["package"]))
        # self.button_app_5 = Button(self.group_application, text=self.configuration.conf["application_5"]["name"], command=lambda: self.robot.start_behavior(self.configuration.conf["application_5"]["package"]))
        # self.button_app_6 = Button(self.group_application, text=self.configuration.conf["application_6"]["name"], command=lambda: self.robot.start_behavior(self.configuration.conf["application_6"]["package"]))
        # self.button_app_7 = Button(self.group_application, text=self.configuration.conf["application_7"]["name"], command=lambda: self.robot.start_behavior(self.configuration.conf["application_7"]["package"]))

        self.button_app_1.grid(row=0, column=1, sticky=NSEW)
        self.button_app_2.grid(row=1, column=1, sticky=NSEW)
        self.button_app_3.grid(row=2, column=1, sticky=NSEW)
        self.button_app_4.grid(row=3, column=1, sticky=NSEW)
        # self.button_app_5.grid(row=4, column=1, sticky=NSEW)
        # self.button_app_6.grid(row=5, column=1, sticky=NSEW)
        # self.button_app_7.grid(row=6, column=1, sticky=NSEW)

        self.root.grid_columnconfigure(0, weight=1)
        
        # self.voice_shaping_scale = Scale(from_=0, to=200, orient=HORIZONTAL, label="Výška hlasu")
        # self.voice_speed_scale = Scale(from_=0, to=200, orient=HORIZONTAL, label="Rychlost hlasu")
        # self.voice_speed_scale.grid(row=5, column=0)
        # self.voice_shaping_scale.grid(row=5, column=1)
        # self.test_say_button = Button(self.root, text="Test hlasu", command=lambda: self.robot.test_say(speed=self.voice_speed_scale.get(), shape=self.voice_shaping_scale.get(), sentence=self.configuration.conf["language"][self.language]["test_sentence"]))
        # self.test_say_button.grid(row=6, column=0)

    def connect(self):
        ip_address = self.entry_address.get()
        port = self.entry_port.get()
        self.robot = Pepper(ip_address, port)
        self.change_language(self.language)

    def invitation(self):
        self.robot.show_image(self.configuration.conf["configuration"]["pozvanka"])
        self.robot.say(str(np.random.choice(self.configuration.conf["language"][self.language]["invitation_morning"]).encode("utf-8")))

    def change_language(self, lang):
        fncts = {"cz": self.robot.set_czech_language, "en": self.robot.set_english_language}
        fncts[lang]()
        self.language = lang


if __name__ == "__main__":
    application = Tk()
    PepperController(application)
    application.mainloop()