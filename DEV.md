**<u>Dev documentation for this project</u>**

**File structure**

root - .py files and other important files like requirements and gitignore

templates - html files

static - css files

environmental variables - .env (look at .env_sample for structure)

**Steps after git pull**

1.  Trigger virtual environment using `venv`.

2.  Run `pip3 install -r requirements.txt`.

3.  Edit....

4.  If you added dependencies, run `pip3 freeze > requirements.txt` while still in venv.

5.  Git commit and push as and when needed.

**Tips**

-   For virtual environment, follow this link [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html). You should be able to type venv and trigger it then.
-   If working on a feature branch, it is recommended to change the requirements.txt file only of the feature is complete and usable. This makes sure of reducing dependencies that are not needed.
