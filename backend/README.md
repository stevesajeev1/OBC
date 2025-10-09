# Backend

## Project Setup

1. Create virtual environment
```sh
python -m venv [name]
# activate
```

2. Install packages
```sh
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

If packages are later changed, update these files.
```sh
pip freeze > requirements.txt
uv add -r requirements.txt
```

3. Copy environment variable based on `.env.example`.

## Compile and Hot-Reload for Development

```sh
fastapi dev
```

## Format with [Black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/)

```sh
black .
isort .
```