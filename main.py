#!/usr/bin/env python
'''
Banana Grader
=============
Simple application for giving grades.
'''

import kivy
kivy.require('1.7.0')

import json
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, NoTransition
from kivy.properties import ListProperty, StringProperty, ObjectProperty, \
        NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
# Von mir

from datetime import date, timedelta
from kivy.uix.widget import Widget
from time import time

class StudentView(Screen):
    student_nachname = StringProperty()
    student_vorname = StringProperty()
    student_pic = StringProperty()
    group_klasse = StringProperty()

class About(Screen):
    pass

class GroupDetails(Screen):
    def __init__(self, **kwargs):
        # print(kwargs)
        #del kwargs['index']
        super(GroupDetails, self).__init__(**kwargs)
    note_index = NumericProperty()
    klasse = StringProperty()
    notenschema = StringProperty()
    group_index = NumericProperty()
    group_klasse = StringProperty()
    group_notenschema = StringProperty()

class Groups(Screen):
    test_button = ObjectProperty()
    data = ListProperty()

    def args_converter(self, row_index, item):
        return {
            'note_index': row_index,
            'note_content': item['content'],
            'note_klasse': item['klasse'],
            'note_vorname': item['vorname'],
            'note_nachname': item['nachname'],
            'note_tutor': item['tutor'],
            'note_bewertung': item['bewertung'],
            'note_title': item['title'], # Datum
            'note_eintrag': item['eintrag']}

    def zeig_was(self):
        self.test_button.text = 'Hallo'

    def zeig_die_gruppen(self):
        self.groups_list.item_strings = ['M1', 'M2']

class Notes(Screen):

    data = ListProperty()

    def args_converter(self, row_index, item):
        return {
            'note_index': row_index,
            'note_content': item['content'],
            'note_klasse': item['klasse'],
            'note_vorname': item['vorname'],
            'note_nachname': item['nachname'],
            'note_tutor': item['tutor'],
            'note_bewertung': item['bewertung'],
            'note_title': item['title'], # Datum
            'note_eintrag': item['eintrag']}

class Home(Screen):

    data = ListProperty()

    def args_converter(self, row_index, item):
        return {
            'group_index': row_index,
            'notenschema': item['notenschema'],
            'klasse': item['klasse']}

class GroupListItem(BoxLayout):

    def __init__(self, **kwargs):
        del kwargs['index']
        super(GroupListItem, self).__init__(**kwargs)
        #print(kwargs)
    group_index = NumericProperty()
    klasse = StringProperty()
    notenschema = StringProperty()

class Students(Screen):
    # Es werden die Eingaben in der students.json eindeutigen Variablen zugeordnet. Fuer's Property-Zeug.
    data2 = ListProperty()

    def args_converter(self, student_index, item):
        return {
            'student_index': student_index,
            'klasse': item['klasse'],
            'student_vorname': item['vorname'],
            'student_nachname': item['nachname'],
            'student_pic': item['pic'],
            'student_tutor': item['tutor']}

class NoteView(Screen):

    note_index = NumericProperty()
    note_klasse = StringProperty()
    note_vorname = StringProperty()
    note_nachname = StringProperty()
    note_tutor = StringProperty()
    note_bewertung = StringProperty()
    note_title = StringProperty() # Datum
    note_eintrag = StringProperty()
    note_content = StringProperty()
    note_pic = StringProperty()

class NoteListItem(BoxLayout):

    def __init__(self, **kwargs):
        del kwargs['index']
        super(NoteListItem, self).__init__(**kwargs)
#        print(kwargs)
    note_index = NumericProperty()
    note_klasse = StringProperty()
    note_vorname = StringProperty()
    note_nachname = StringProperty()
    note_tutor = StringProperty()
    note_bewertung = StringProperty()
    note_title = StringProperty() # Datum
    note_eintrag = StringProperty()
    note_content = StringProperty()

class MutableTextInput(FloatLayout):

    text = StringProperty()
    multiline = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(MutableTextInput, self).__init__(**kwargs)
        Clock.schedule_once(self.prepare, 0)

    def prepare(self, *args):
        self.w_textinput = self.ids.w_textinput.__self__
        self.w_label = self.ids.w_label.__self__
        self.view()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            self.edit()
        return super(MutableTextInput, self).on_touch_down(touch)

    def edit(self):
        self.clear_widgets()
        self.add_widget(self.w_textinput)
        self.w_textinput.focus = True

    def view(self):
        self.clear_widgets()
        self.add_widget(self.w_label)

    def check_focus_and_view(self, textinput):
        if not textinput.focus:
            self.text = textinput.text
            self.view()

class BananaGraderApp(App):
    def build(self):
        self.title = 'Banana Grader'
        # Der obige Screen Notes bekommt den Namen self.notes, letztlich um in self.notes.data die Noteneingaben zu speichern
        self.notes = Notes(name='notes')
        self.home = Home(name='home')
        self.students = Students(name='students')

        self.load_home()
        self.load_notes()

        self.akt_schueler_index = 0
        self.schnelldurchlauf = True
        self.akt_klasse = []

        self.transition = SlideTransition(duration=.15)
        root = ScreenManager(transition=self.transition)
        root.add_widget(self.notes)
        root.add_widget(self.home)

        self.groups = Groups(name='groups')
        root.add_widget(self.groups)

        self.groupdetails = GroupDetails(name='groupdetails')
        root.add_widget(self.groupdetails)

        self.about = About(name="about")
        root.add_widget(self.about)

        root.current = 'home'
        return root


    def load_notes(self):
        if not exists(self.notes_fn):
            return
        with open(self.notes_fn) as fd:
            data = json.load(fd)
        self.notes.data = data

    def load_home(self):
        if not exists(self.students_fn):
            return
        with open(self.students_fn) as fd:
            data = json.load(fd)
        for d in data:
            for k in ['vorname', 'nachname', 'tutor', 'pic']:
                    del d[k]
        klassen = [dict(t) for t in set([tuple(d.items()) for d in data])]
        klassen.sort(key=lambda k:k['klasse'])
        self.home.data = klassen
        # print ('[INFO    ] Die student.json wurde als data eingelesen, voruebergehend klassenzugros genannt, um fuer den Home-Screen unnoetige dict-items zu loeschen und dann die doppelten Dictionaries zu loeschen. self.home.data ist jetzt:\n' +  str(klassen))

    def load_students(self,klasse):
        if not exists(self.students_fn):
            return
        with open(self.students_fn) as fd2:
            data2 = json.load(fd2)
            #data2 = [{u'notenschema': u'Oberstufe', u'pic': u'arensabr.jpg', u'tutor': u'Kei', u'nachname': u'Arena', u'vorname': u'Sabrina', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'belonata.jpg', u'tutor': u'Kei', u'nachname': u'Belousow', u'vorname': u'Natascha', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'bloefabi.jpg', u'tutor': u'Kei', u'nachname': u'Bl\xf6meke', u'vorname': u'Fabienne', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'dittsand.jpg', u'tutor': u'Kei', u'nachname': u'Dittes', u'vorname': u'Sandro', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'engbsime.jpg', u'tutor': u'Kei', u'nachname': u'Engbrecht', u'vorname': u'Simeon Cornelius', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'fuerlena.jpg', u'tutor': u'Kei', u'nachname': u'F\xfcrst', u'vorname': u'Lena', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'giesanto.jpg', u'tutor': u'Kei', u'nachname': u'Giesche', u'vorname': u'Antonia', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'gutjjako.jpg', u'tutor': u'Kei', u'nachname': u'Gutjahr', u'vorname': u'Jakob', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'herryann.jpg', u'tutor': u'Kei', u'nachname': u'Herrmann', u'vorname': u'Yannick', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'kanjjasm.jpg', u'tutor': u'Kei', u'nachname': u'Kanjuh', u'vorname': u'Jasmin', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'koegluca.jpg', u'tutor': u'Kei', u'nachname': u'K\xf6gel', u'vorname': u'Luca Fabio', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'kuebdavi.jpg', u'tutor': u'Kei', u'nachname': u'K\xfcbler', u'vorname': u'David', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'lehmdarl.jpg', u'tutor': u'Kei', u'nachname': u'Lehmann', u'vorname': u'Darleen', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'meisartu.jpg', u'tutor': u'Kei', u'nachname': u'Meisner', u'vorname': u'Artur', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'neumkevi.jpg', u'tutor': u'Kei', u'nachname': u'Neumann', u'vorname': u'Kevin', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'pinafatm.jpg', u'tutor': u'Kei', u'nachname': u'Pinarci', u'vorname': u'Fatma', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'sakamehm.jpg', u'tutor': u'Kei', u'nachname': u'Sakar', u'vorname': u'Mehmet', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'schatimo.jpg', u'tutor': u'Kei', u'nachname': u'Scharli', u'vorname': u'Timo Michael', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'schidani.jpg', u'tutor': u'Kei', u'nachname': u'Schild', u'vorname': u'Daniel', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'schnelis.jpg', u'tutor': u'Kei', u'nachname': u'Schnorr', u'vorname': u'Elisa', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'steihann.jpg', u'tutor': u'Kei', u'nachname': u'Steinbach', u'vorname': u'Hannah Katharina Lotta', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'taeumiri.jpg', u'tutor': u'Kei', u'nachname': u'T\xe4uber', u'vorname': u'Miriam', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'uenshued.jpg', u'tutor': u'Kei', u'nachname': u'\xdcnsal', u'vorname': u'H\xfcda-Nur', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'wagnjan.jpg', u'tutor': u'Kei', u'nachname': u'Wagner', u'vorname': u'Jan Matthias', u'klasse': u'M 2018c'}, {u'notenschema': u'Oberstufe', u'pic': u'samantha.jpg', u'tutor': u'Btz', u'nachname': u'Brunco', u'vorname': u'Samantha', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'laura.jpg', u'tutor': u'Scu', u'nachname': u'H\xf6rning', u'vorname': u'Laura', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'marija.jpg', u'tutor': u'Pes', u'nachname': u'Josovic', u'vorname': u'Marija', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'oktay.jpg', u'tutor': u'Btz', u'nachname': u'Kufaci', u'vorname': u'Oktay', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'anna-maria.jpg', u'tutor': u'Rw', u'nachname': u'Martin', u'vorname': u'Anna-Maria', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'david.jpg', u'tutor': u'Btz', u'nachname': u'Negele', u'vorname': u'David', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'laura_n.jpg', u'tutor': u'Btz', u'nachname': u'Nemati', u'vorname': u'Laura', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'martin.jpg', u'tutor': u'Pes', u'nachname': u'Nissen Gonzalez', u'vorname': u'Martin', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'leonie.jpg', u'tutor': u'Rw', u'nachname': u'Ose', u'vorname': u'Leonie', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'pinafatm.jpg', u'tutor': u'Kei', u'nachname': u'Pinarci', u'vorname': u'Fatma', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'fabian.jpg', u'tutor': u'Btz', u'nachname': u'Reinbold', u'vorname': u'Fabian', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'marcel.jpg', u'tutor': u'Scu', u'nachname': u'Stiebritz', u'vorname': u'Marcel', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'michelle.jpg', u'tutor': u'Rw', u'nachname': u'Wegelin', u'vorname': u'Michelle Naomi', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'jessica.jpg', u'tutor': u'Rw', u'nachname': u'Zipf', u'vorname': u'Jessica', u'klasse': u'Ethik 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'benedikt_bauer.jpg', u'tutor': u'nv', u'nachname': u'Bauer', u'vorname': u'Benedikt', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'madeleine_b.jpg', u'tutor': u'nv', u'nachname': u'Bleyel', u'vorname': u'Madeleine', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'isabel.jpg', u'tutor': u'nv', u'nachname': u'Bohlmann', u'vorname': u'Isabel', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'anton_gietl.jpg', u'tutor': u'nv', u'nachname': u'Gietl', u'vorname': u'Anton', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'stefan_g.jpg', u'tutor': u'nv', u'nachname': u'Gietl', u'vorname': u'Stefan', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'gutjjako.jpg', u'tutor': u'nv', u'nachname': u'Gutjahr', u'vorname': u'Jakob', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'martin_n.jpg', u'tutor': u'nv', u'nachname': u'Nissen Gonzalez', u'vorname': u'Martin', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'fabian.jpg', u'tutor': u'nv', u'nachname': u'Reinbold', u'vorname': u'Fabian', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'alexander_salameh.jpg', u'tutor': u'nv', u'nachname': u'Salameh', u'vorname': u'Alexander', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'marcel.jpg', u'tutor': u'nv', u'nachname': u'Stiebritz', u'vorname': u'Marcel', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'alina_telge.jpg', u'tutor': u'nv', u'nachname': u'Telge', u'vorname': u'Alina', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'julian_weidel.jpg', u'tutor': u'nv', u'nachname': u'Weidel', u'vorname': u'Julian', u'klasse': u'VKM 2018'}, {u'notenschema': u'Oberstufe', u'pic': u'jessica_z.jpg', u'tutor': u'nv', u'nachname': u'Zipf', u'vorname': u'Jessica', u'klasse': u'VKM 2018'}, {u'notenschema': u'Mittelstufe', u'pic': u'jescann.jpg', u'tutor': u'Vog', u'nachname': u'Jeschke', u'vorname': u'Ann-Sophie', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'ayhabaha.jpg', u'tutor': u'Vog', u'nachname': u'Ayhan', u'vorname': u'Baha', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'hofmcath.jpg', u'tutor': u'Vog', u'nachname': u'Hofmeister', u'vorname': u'Cathrin', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'hanzdani.jpg', u'tutor': u'Vog', u'nachname': u'Hanzelmann', u'vorname': u'Daniel Jason', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'muhmdavi.jpg', u'tutor': u'Vog', u'nachname': u'Muhm', u'vorname': u'David', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'dilldavi.jpg', u'tutor': u'Vog', u'nachname': u'Dillmann', u'vorname': u'David Eduard', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'goedelia.jpg', u'tutor': u'Vog', u'nachname': u'G\xf6del', u'vorname': u'Eliah Antonio', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'brenfabi.jpg', u'tutor': u'Vog', u'nachname': u'Brenneisen', u'vorname': u'Fabian Jakob', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'masufinn.jpg', u'tutor': u'Vog', u'nachname': u'Masuch', u'vorname': u'Finn', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'niedflor.jpg', u'tutor': u'Vog', u'nachname': u'Niedermaier', u'vorname': u'Florian', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'berggioi.jpg', u'tutor': u'Vog', u'nachname': u'Berger', u'vorname': u'Gioia Sophie', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'kasahasa.jpg', u'tutor': u'Vog', u'nachname': u'Kasap', u'vorname': u'Hasan', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'trumjust.jpg', u'tutor': u'Vog', u'nachname': u'Trumpf', u'vorname': u'Justin', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'baueloui.jpg', u'tutor': u'Vog', u'nachname': u'Bauer', u'vorname': u'Louis', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'burkluca.jpg', u'tutor': u'Vog', u'nachname': u'Burkhardt', u'vorname': u'Luca David', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'bindluca.png', u'tutor': u'Vog', u'nachname': u'Binder', u'vorname': u'Luca Michael', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'trefluis.jpg', u'tutor': u'Vog', u'nachname': u'Treffinger', u'vorname': u'Luis', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'schuluis.jpg', u'tutor': u'Vog', u'nachname': u'Schubert', u'vorname': u'Luis', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'trannhat.jpg', u'tutor': u'Vog', u'nachname': u'Tran Van', u'vorname': u'Nhat Lam', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'rempnico.png', u'tutor': u'Vog', u'nachname': u'Rempfer', u'vorname': u'Nico', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'bozkogul.jpg', u'tutor': u'Vog', u'nachname': u'Bozkurt', u'vorname': u'Ogulcan', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'schistef.jpg', u'tutor': u'Vog', u'nachname': u'Schiek', u'vorname': u'Stefan Daniel', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'stadtim.jpg', u'tutor': u'Vog', u'nachname': u'Stadlinger', u'vorname': u'Tim', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'schotizi.jpg', u'tutor': u'Vog', u'nachname': u'Schorpp', u'vorname': u'Tizian', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'czettobi.jpg', u'tutor': u'Vog', u'nachname': u'Czetsch', u'vorname': u'Tobias Theodor', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'krautom.jpg', u'tutor': u'Vog', u'nachname': u'Kraus', u'vorname': u'Tom Justin', u'klasse': u'M 8a'}, {u'notenschema': u'Mittelstufe', u'pic': u'bergrodn.jpg', u'tutor': u'Dz', u'nachname': u'Berger', u'vorname': u'Rodney Georg', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'dedenils.jpg', u'tutor': u'Dz', u'nachname': u'Dederichs', u'vorname': u'Nils', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'geiesimo.jpg', u'tutor': u'Dz', u'nachname': u'Geier', u'vorname': u'Simon', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'giulcara.jpg', u'tutor': u'Dz', u'nachname': u'Giuliano', u'vorname': u'Cara-Marie', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'habejoha.jpg', u'tutor': u'Dz', u'nachname': u'Habermann', u'vorname': u'Johannes Elias', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'hansnils.jpg', u'tutor': u'Dz', u'nachname': u'Hansen', u'vorname': u'Nils', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'heinbjoe.jpg', u'tutor': u'Dz', u'nachname': u'Heinze', u'vorname': u'Bj\xf6rn', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'herrbene.jpg', u'tutor': u'Dz', u'nachname': u'Herrmann', u'vorname': u'Benedikt', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'herrlea.jpg', u'tutor': u'Dz', u'nachname': u'Herrmann', u'vorname': u'Lea', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'kadefabi.jpg', u'tutor': u'Dz', u'nachname': u'Kaderabek', u'vorname': u'Fabian', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'kayshenr.jpg', u'tutor': u'Dz', u'nachname': u'Kayser', u'vorname': u'Henrik', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'klinanna.jpg', u'tutor': u'Dz', u'nachname': u'Klingel', u'vorname': u'Annabel Elisabeth', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'kuehmax.jpg', u'tutor': u'Dz', u'nachname': u'Kuhn', u'vorname': u'Sanja', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'kuhnsanj.jpg', u'tutor': u'Dz', u'nachname': u'K\xfchner', u'vorname': u'Max', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'leehans.jpg', u'tutor': u'Dz', u'nachname': u'Lee', u'vorname': u'Hans', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'leypbric.jpg', u'tutor': u'Dz', u'nachname': u'Leypoldt', u'vorname': u'Brick Brigen Luis', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'loehjona.jpg', u'tutor': u'Dz', u'nachname': u'L\xf6hr', u'vorname': u'Jonas Benjamin', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'polljoha.jpg', u'tutor': u'Dz', u'nachname': u'Pollich', u'vorname': u'Johannes', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'proehann.jpg', u'tutor': u'Dz', u'nachname': u'Pr\xf6ll', u'vorname': u'Hanna', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'richfabi.jpg', u'tutor': u'Dz', u'nachname': u'Richter', u'vorname': u'Fabian', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'ruednils.jpg', u'tutor': u'Dz', u'nachname': u'R\xfcdele', u'vorname': u'Nils', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'salasabr.jpg', u'tutor': u'Dz', u'nachname': u'Salameh', u'vorname': u'Sabrina', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'schwmika.jpg', u'tutor': u'Dz', u'nachname': u'Schwenk', u'vorname': u'Mika', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'soulvale.jpg', u'tutor': u'Dz', u'nachname': u'Soulier', u'vorname': u'Valerie', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'stiepatr.jpg', u'tutor': u'Dz', u'nachname': u'Stiebritz', u'vorname': u'Patrick', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'turntina.jpg', u'tutor': u'Dz', u'nachname': u'Turnwald', u'vorname': u'Tina', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'vierjoey.jpg', u'tutor': u'Dz', u'nachname': u'Viereck', u'vorname': u'Joey', u'klasse': u'M 9a'}, {u'notenschema': u'Mittelstufe', u'pic': u'walzdirk.jpg', u'tutor': u'Dz', u'nachname': u'Walz', u'vorname': u'Dirk', u'klasse': u'M 9a'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Arsov', u'vorname': u'Filip', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Beyer', u'vorname': u'Maximilian', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Billes', u'vorname': u'Stephanie', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'B\xf6gel', u'vorname': u'Jenny', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Cipolla', u'vorname': u'Gianluca', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Demir', u'vorname': u'Mine', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Doppelbauer', u'vorname': u'Alexander', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Fe\xdfenbecker', u'vorname': u'Anja', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Graf', u'vorname': u'Julius', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Grahm', u'vorname': u'Patrick', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Hoang', u'vorname': u'Gia Trung', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Krause', u'vorname': u'Amelie Margarethe', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Langer', u'vorname': u'Felix', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Link', u'vorname': u'Katharina', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Ries', u'vorname': u'Jeffrey', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Rogge', u'vorname': u'Karolin Ann', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Rose', u'vorname': u'Johannes', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'St\xe4bler', u'vorname': u'Robin', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Stefen', u'vorname': u'Nikola Vanessa', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Sulzer', u'vorname': u'Lisa', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'V\xf6gele', u'vorname': u'Dennis', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Wegelin', u'vorname': u'Sandra', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'Pes', u'nachname': u'Zieger', u'vorname': u'Nicolas', u'klasse': u'M 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Notter', u'vorname': u'Ann-Katrin', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Renz', u'vorname': u'Desiree', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Gerson', u'vorname': u'Eva', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Wildmann', u'vorname': u'Fabian', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'G\xf6ktepe', u'vorname': u'Fatma', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Bechthold', u'vorname': u'Jasmin', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Tangen', u'vorname': u'Johanna', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Borrey', u'vorname': u'J\xf6ran', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Potel', u'vorname': u'J\xf6rg', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Jakob', u'vorname': u'Julia', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Schl\xfcntz', u'vorname': u'Juliane', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Rogge', u'vorname': u'Karolin', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Kast', u'vorname': u'Larissa', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Akg\xfcl', u'vorname': u'Mahsun', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Ulus', u'vorname': u'Merve', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Stefen', u'vorname': u'Nikola', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Karadayi', u'vorname': u'\xd6zlem', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Chehab', u'vorname': u'Scheyma', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Lehmann', u'vorname': u'Sofia', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Schwedes', u'vorname': u'Stefanie', u'klasse': u'Ethik 2017'}, {u'notenschema': u'Oberstufe', u'pic': u'DDDDdddd.png', u'tutor': u'kA', u'nachname': u'Knies', u'vorname': u'Theresa', u'klasse': u'Ethik 2017'}]
        self.students.data = data2
        # print ('Ich bilde eine Liste von Dicts der Klasse ' + str(klasse))
        schueler_der_klasse = []
        for d in data2:
            klasse_des_dicts = d['klasse']
            if klasse_des_dicts == klasse:
                schueler_der_klasse.append(d)
            else:
                pass
        self.students.data = schueler_der_klasse
        # print ('[INFO    ] self.students.data: \n ' + str(self.students.data))

    def add_note(self,klasse):

        self.akt_klasse = klasse
        self.load_students(self.akt_klasse)
        self.schnelldurchlauf = True
        student = self.students.data[self.akt_schueler_index]
        self.notes.data.append({'title': str(date.today()), 'klasse': str(self.akt_klasse), 'vorname': student.get('vorname'), 'nachname': student.get('nachname'), 'bewertung': '', 'eintrag': '', 'tutor': '', 'pic': str(student.get('pic')), 'content': ''})
        note_index = len(self.notes.data) - 1
        self.edit_note(note_index)

    def set_note_bewertung(self, note_index, note_bewertung):
        self.notes.data[note_index]['bewertung'] = note_bewertung
        self.save_notes()
        self.refresh_notes()
        if self.akt_schueler_index < (len(self.students.data) - 1):
            self.akt_schueler_index += 1
            self.add_note(self.akt_klasse)
        else:
            self.akt_schueler_index = 0
            self.schnelldurchlauf = False
            self.go_home()

    def edit_note(self, note_index):
        note = self.notes.data[note_index]
        name = 'note{}'.format(note_index)
        if self.root.has_screen(name):
            self.root.remove_widget(self.root.get_screen(name))

        view = NoteView(
            name=name,
            note_index=note_index,
            note_title=note.get('title'),
            note_vorname=note.get('vorname'),
            note_bewertung=note.get('bewertung'),
            note_eintrag=note.get('eintrag'),
            note_tutor=note.get('tutor'),
            note_klasse=note.get('klasse'),
            note_nachname=note.get('nachname'),
            note_pic=note.get('pic'),
            note_content=note.get('content')
            )
        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.root.current = view.name

    def set_note_title(self, note_index, note_title):
        self.notes.data[note_index]['title'] = note_title
        self.save_notes()
        self.refresh_notes()

    def save_notes(self):
        with open(self.notes_fn, 'w') as fd:
            json.dump(self.notes.data, fd)

    def refresh_notes(self):
        data3 = self.notes.data
        self.notes.data = []
        self.notes.data = data3

    def del_note(self, note_index):
        del self.notes.data[note_index]
        self.save_notes()
        self.refresh_notes()
        self.akt_schueler_index = 0
        self.go_notes()

    def go_notes(self):
        self.transition.direction = 'right'
        self.root.current = 'notes'

    def set_note_content(self, note_index, note_content):
        self.notes.data[note_index]['content'] = note_content
        data = self.notes.data
        self.notes.data = []
        self.notes.data = data
        self.save_notes()
        self.refresh_notes()

    def go_groupdetails(self, group_index, klasse, notenschema):
        group = self.home.data[group_index]
        name = 'group{}'.format(group_index)
        if self.root.has_screen(name):
            self.root.remove_widget(self.root.get_screen(name))
        view = GroupDetails(
            name=name,
            group_index=group_index,
            group_klasse=group.get('klasse'),
            group_notenschema=group.get('notenschema')
            )
        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.root.current = view.name

    def start_student_show(self, klasse):
        self.load_students(klasse)
        self.schnelldurchlauf = True
        self.go_students()

    def go_home(self):
        self.schnelldurchlauf = False
        self.akt_schueler_index = 0
        self.transition.direction = 'right'
        self.root.current = 'home'

    def go_students(self):
        student = self.students.data[self.akt_schueler_index]
        name = 'student{}'.format(self.akt_schueler_index)
        if self.root.has_screen(name):
            self.root.remove_widget(self.root.get_screen(name))
        view = StudentView(
            name = name,
            student_nachname = student.get('nachname'),
            student_pic = student.get('pic'),
            student_vorname = student.get('vorname')
            )
        self.root.add_widget(view)
        self.transition.direction = 'left'
        self.transition.duration = 0.01
        self.root.current = view.name

    def go_next_student(self):
        if self.akt_schueler_index < (len(self.students.data) - 1):
            self.akt_schueler_index += 1
            # print(str(self.akt_schueler_index))
            self.go_students()
        else:
            # print('Das war der letzte Schuler')
            self.go_home()


    @property
    def notes_fn(self):
        return join('data/', 'grades.json')

    @property
    def students_fn(self):
        return join('data/', 'students.json')


if __name__ == '__main__':
    BananaGraderApp().run()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
