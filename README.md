# Banana Grader
[<img src="/app/icon.png" width="50">](app/icon.png) App for giving grades and earning bananas.

## Screenshots
[<img src="/screenshots/Banana_Grader_1_Home.png" width="200">](screenshots/Banana_Grader_1_Home.png)
[<img src="/screenshots/Banana_Grader_2_Give_grades.png" width="200">](screenshots/Banana_Grader_2_Give_grades.png)
[<img src="/screenshots/Banana_Grader_3_Learn_names.png" width="200">](screenshots/Banana_Grader_3_Learn_names.png) 

## Installation
The code you find here on GitHub isn't compiled and still under construction, therefore you can [install Kivy](https://kivy.org/docs/installation/installation.html#stable-version) to run it. It's not running with the Kivy Launcher because it doesn't support the used csv module.

Before running the app (with *sudo python main.py*) you  have to copy the data in the `data_of_user-data-dir`  to your [user data directory](https://kivy.org/docs/api-kivy.app.html?highlight=user_data_dir#kivy.app.App.user_data_dir).

To import your students you can change the file named *students.csv*.

To get your grades you can take the file named *grades.json* and [convert](http://www.convertcsv.com/json-to-csv.htm) it to csv.

## Concept

The idea behind the app is to realize a quick workflow: Students and given grades are managed on a personal computer via two **csv* files. The Banana Grader imports the students.csv and stores given grades into grades.csv. 
So the Banana Grader can be used for two reasons: 

1. To give grades to students
2. To learn the names of the students

Functions to implement:

* Export grades to csv (they are stored in grads.json)
* Give bananas for given grades
* Copy default files to user data directory
* Handle incorrect files
* Write more in "About"
* Nicer symbols (left arrow) 

##  Licenses

* This app uses the [Kivy](https://github.com/kivy/kivy) framework, which is released under the terms of the MIT License. Please refer to there LICENSE file. The base of the Banana Grader is the example/tutorial app called [Notes](https://github.com/kivy/kivy/tree/master/examples/tutorials/notes/final).
* The current UI design has been adapted from Moblintouch theme's SVGs and is licensed under the terms of the [LGPLv2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1).
* The default pictures are created by [NicholasJudy456](https://openclipart.org/collection/collection-detail/NicholasJudy456/12676)
