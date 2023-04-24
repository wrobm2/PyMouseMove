# PyMouseMove

This is a fairly basic python program ive made in free time, purely because i wanted to make my workflow as keyboard driven as possible

You may use it how you please, i do not care, but also will not be held liable. 

couple other viable usecases i guess 
 - Hooking up a joystick to your pc ( this is not a good way to do it, but sure! )
 - Helping persons with disabilities set up a easy input device ( ijkl is easier to interact with than all the variations that a mouse can have in movement )
 - vimmifying everything you do 24/7 ( based )

You can install it one of three ways

# 1. Installing via releases
Steps:
 1. Go to the releases section on github ( ctrl + f and type in releases )
 2. Click on the latest release
 3. Download the executable file pymousemove.exe
 4. Download any one of the json files ( these are configs ) ( you can download multiple and it will prompt you to switch between them )
 5. As long as the executable and the json files are in the same directory, then just run the executable, and enjoy 

# 2. Installing from git 
This assumes you have python installed, if you dont, download it from https://www.python.org/
Steps: 
 1. Click on the green code button at the top middle right area 
 2. Click Download zip 
 3. Extract the zip to a folder
 4. Open that folder in cmd / terminal / whatever
 5. type pip install -r requirements.txt ( and hit enter )
 6. type python .\mousemove.py 
    ( you can alternatively just type python mous and then hit tab )
 7. rejoice


# 3. Download from dist folder
Steps:
 1. Click dist folder
 2. download the json file
 3. download pymousemove.exe
 ( you can use other configs but i am sending ijkl as its the best option im aware of )

# Info
Almost all related code is in the pymousemove.py file

I am so immensely open to pull requests i have hit a wall with a number of sections of this program and i would love to receive any and all help 

copy folder is just libraries because it wont build unless i put it there. i dont know if i am doing something wrong or what, but thats what we got. 
^ this is especially the pyfiglet library it wants the fonts for it and it kind find the fonts just via an import statement for whatever reason 
