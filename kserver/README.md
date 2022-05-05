# ktestui
#### How to Set Up:  
1. Open Terminal in working directory.
2. Create a virtual environment: ```virtualenv .``` (Mac)
3. Go into the environment/directory. ```cd <____>``` (Mac)
4. Activate the environment: ```source bin/actiavte``` (Mac)
5. Install Django: ```pip install django``` (Mac)

#### How to run the server locally:
1. Open terminal in the cloned directory. (preferrably in Virtual Env.)
2. Type: ```python manage.py runserver```


#### How to initialize the server:
1. Open terminal in the cloned directory. (preferrably in Virtual Env.)
2. Type: ```python manage.py <command>```
3. ```<command>``` in the following order:  1. ```migrate```
                                            2. ```makemigrations```
                                            3. ```collectstatic```
4. ```<command>``` can be ```help``` to show list of all commands

### Some Easy Fixes
Sometimes DB needs to be updated if something went wrong while making changes.   
To fix: type ```python manage.py migrate --run-syncdb``` in the correct directory.


### To recreate the anaconda environment
```conda env create -f environment.yml```

### To export conda environment
```conda env export --no-builds > environment.yml```
