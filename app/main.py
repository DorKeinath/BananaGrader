#!/usr/bin/env python
'''
Banana Grader
=======================

Simple application for manage grades. In future you earn bananas for giving grades.

'''

import kivy
kivy.require('1.7.0')

import json
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, StringProperty, ObjectProperty, \
        NumericProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from datetime import date, timedelta
from kivy.uix.widget import Widget
import csv, decimal, codecs

class StudentView(Screen):
    student_nachname = StringProperty()
    student_vorname = StringProperty()
    student_pic = StringProperty()
    group_klasse = StringProperty()

class About(Screen):
    pass

class GroupDetails(Screen):
    def __init__(self, **kwargs):
        print(kwargs)
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

        self.notes = Notes(name='notes')
        self.home = Home(name='home')

        self.load_notes()
        self.load_home()
        self.students = Students(name='students')

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

        self.alle_schueler = []
        self.load_csv()

        return root

    def utf_8_encoder(self, unicode_csv_data):
        for line in unicode_csv_data:
            yield line.encode('utf-8')

    def unicode_csv_reader(self, unicode_csv_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.reader(self.utf_8_encoder(unicode_csv_data),
                                dialect=dialect, **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]

    def load_csv(self):
        # if not exists(self.students_fn):
        #     return
        # with open(self.students_fn) as fd:
        #     data = json.load(fd)
        with codecs.open(self.students_csv_fn, encoding='utf-8') as f:
            reader = self.unicode_csv_reader(f)
            keys = [k.strip() for k in reader.next()]
            result = []
            for row in reader:
                d=dict(zip(keys, row))
                result.append(d)
            self.alle_schueler = result
            print result

    def load_notes(self):
        if not exists(self.notes_fn):
            return
        with open(self.notes_fn) as fd:
            data = json.load(fd)
        self.notes.data = data

    def load_home(self):
        self.load_csv()
        data = self.alle_schueler
        for d in data:
            for k in ['vorname', 'nachname', 'tutor', 'pic']:
                    del d[k]
        klassen = [dict(t) for t in set([tuple(d.items()) for d in data])]
        klassen.sort(key=lambda k:k['klasse'])
        print ('[INFO    ] Die csv wurde eingelesen und die doppelten geloescht. Es gibt die folgenden Klassen:\n' +  str(klassen))
        self.home.data = klassen

    def load_students(self,klasse):
        self.load_csv()
        data2 = self.alle_schueler
        print ('Ich bilde eine Liste von Dicts der Klasse ' + str(klasse))
        schueler_der_klasse = []
        for d in data2:
            klasse_des_dicts = d['klasse']
            if klasse_des_dicts == klasse:
                schueler_der_klasse.append(d)
            else:
                print ('.')
        self.students.data = schueler_der_klasse
        print ('[INFO    ] self.students.data: \n ' + str(self.students.data))

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
            self.go_notes()

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
        self.root.current = view.name

    def go_next_student(self):
        if self.akt_schueler_index < (len(self.students.data) - 1):
            self.akt_schueler_index += 1
            # print(str(self.akt_schueler_index))
            self.go_students()
        else:
            print('Das war der letzte Schuler')
            self.go_home()
    # TODO
    # def export_to_csv(self):
    #     toCSV = self.notes.data
    #     csvname = 'noten_' + str(date.today()) + '.csv'
    #     keys = toCSV[0].keys()
    #     with open(csvname, 'wb') as output_file:
    #         dict_writer = csv.DictWriter(output_file, keys)
    #         dict_writer.writeheader()
    #         dict_writer.writerows(toCSV)

    @property
    def notes_fn(self):
        return join(self.user_data_dir, 'grades.json')

    @property
    def students_csv_fn(self):
        return join(self.user_data_dir, 'students.csv')

if __name__ == '__main__':
    # LabelBase.register(name='Roboto',
    #                    fn_regular='Roboto-Thin.ttf',
    #                    fn_bold='Roboto-Medium.ttf')
    BananaGraderApp().run()
