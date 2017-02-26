#!/bin/bash
# Als Terminal öffnen

inotifywait -mq -e close_write /home/effe/Sync/kivy_auf_FP/BananaGrader_entwickler_version/ | while read FILE
do
#	kill $(ps aux | pgrep '[p]ython' | awk '{print $2}')
	pkill python
	echo "Die Datei $FILE wurde geschrieben."
	python /home/effe/Sync/kivy_auf_FP/BananaGrader_entwickler_version/main.py
done

