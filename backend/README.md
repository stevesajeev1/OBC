# Backend

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

Copy environment variable based on `.env.example`.

Generate prisma
```sh
prisma generate
```

### Compile and Hot-Reload for Development

```sh
fastapi dev
```

### Format with [Black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/)

```sh
black .
isort .
```