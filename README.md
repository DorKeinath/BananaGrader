# Banana Grader

 App for giving grades and earning bananas.

## Screenshots
[<img src="/screenshots/Banana_Grader_1_Home.png" width="200">](screenshots/Banana_Grader_1_Home.png)
[<img src="/screenshots/Banana_Grader_2_Give_grades.png" width="200">](screenshots/Banana_Grader_2_Give_grades.png)
[<img src="/screenshots/Banana_Grader_3_Learn_names.png" width="200">](screenshots/Banana_Grader_3_Learn_names.png)

## Installation
* To use it with your android, you can install the *Kivy Launcher* ([apk](https://kivy.org/#download) ,[Google Play](https://play.google.com/store/apps/details?id=org.kivy.pygame).
* To use it on an other device look [here](https://kivy.org/#download)

## Use

To import your **students** you can change the file named *students.csv*. Afterwards use

```python
python convert_students_to_json.py
```
to convert your csv to the necessary json file.

To get your **grades** use

```python
python convert_grades_to_csv.py
```
to convert your *grades.json* to a csv file.

## Concept

The idea behind the app is to realize a quick workflow: Students and given grades are managed on a personal computer via two csv files. So the Banana Grader can be used for two reasons:

1. To give grades to students
2. To learn the names of the students

Functions to implement:

* Give bananas for given grades
* Reverse order of given grades
* Increase velocity in creating dics
* Handle incorrect files (*students.csv*)
* Security stuff
* Write more in "About"
* Nicer symbols (left arrow)

##  Licenses

* This app uses the [Kivy](https://github.com/kivy/kivy) framework, which is released under the terms of the MIT License. Please refer to there LICENSE file. The base of the Banana Grader is the example/tutorial app called [Notes](https://github.com/kivy/kivy/tree/master/examples/tutorials/notes/final).
* The current UI design has been adapted from Moblintouch theme's SVGs and is licensed under the terms of the [LGPLv2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1).
* The default pictures are created by [NicholasJudy456](https://openclipart.org/collection/collection-detail/NicholasJudy456/12676)
