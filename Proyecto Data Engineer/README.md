## Part 1 Local Setup

1. install poetry (or safer, follow the instructions: https://python-poetry.org/docs/#installation)
```bash
pip install poetry
```

2. In the root directory execute `poetry install`
```bash
poetry install
```

3. [UNIX]: Give permission to the bash script
```bash
sudo chmod +x ./run.sh
```

4. [UNIX]: Run the FastAPI server via poetry with the bash script
```bash
poetry run ./run.sh
```

5. [WINDOWS]: Run the FastAPI server via poetry with the Python command
```bash
poetry run python app/main.py
```

6. Open [http://localhost:8001/](http://localhost:8001/) in your browser


7. To update the dependencies, run `poetry update`
```bash
poetry update
```
