## Project Setup

Create virtual environment
```sh
python -m venv [name]
# activate
```

Install packages
```sh
pip install -r requirements.txt
```

Create a `.env` file
```sh
cp .env.example .env
# fill out .env
```

### Compile and Hot-Reload for Development

```sh
fastapi dev main.py
```

### Format with [Black](https://github.com/psf/black)

```sh
black .
```