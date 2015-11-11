# child_ai
kaggle task for child 8 grader

# how to install
```
pip install virtualenv
virtualenv-2.7 .venv
source .venv/bin/activate
pip install -e .
```

# how to decrypt/encrypt data
If you want to get the data from encoded files (first time or after an update) run:
```
source .venv/bin/activate
cipher decrypt -p <password> -l encrypted_files.list 
```

If you need to commit more encrypted data, add the data to the list and run
```
source .venv/bin/activate
cipher encrypt -p <password> -l encrypted_files.list
```

