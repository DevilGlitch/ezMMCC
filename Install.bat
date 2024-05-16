@echo off
setlocal

rem Downloading check_minecraft_conflicts.py from GitHub
echo Downloading check_minecraft_conflicts.py...
curl -o check_minecraft_conflicts.py https://raw.githubusercontent.com/DevilGlitch/ezMMCC/main/check_minecraft_conflicts.py

rem Running check_minecraft_conflicts.py using the current Python installation
echo Running check_minecraft_conflicts.py...
python check_minecraft_conflicts.py

rem Open conflicting_jars.txt
echo Opening conflicting_jars.txt...
start conflicting_jars.txt

echo Finished.
pause
