#/bin/bash
POETRY_VERSION=1.3.2
 
sudo apt-get update && \
  sudo apt-get install --no-install-suggests -- no-install-recommends --yes python3-venv gcc libpython3-dev && \
  sudo apt-get clean && \
  rm -rf /var/lib/apt/lists/*

python3 -m venv /venv
/venv/bin/pip install --upgrade pip setuptools wheel
/venv/bin/pip install "poetry=={POETRY_VERSION}"

cp pyproject.toml poetry.lock \

/venv/bin/poetry export --without-hashes --format requirements.txt --output /requirements.txt

/venv/bin/pip install --disable-pip-version-check -r /requirements.txt

cp -R . /app

cd /app

/venv/bin/python3 src/main.py
