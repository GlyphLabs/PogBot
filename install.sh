#/bin/bash

git clone https://github.com/PurpLabs/PogBot.git
pip install poetry
cd PogBot
poetry install
cd src

env_file=".env"

if [ ! -f "$env_file" ]; then
  echo "You haven't filled out the environment variables yet!"
  exit 1
fi

missing_variables=0

required_variables=("TOKEN" "BRAINSHOP_ID" "BRAINSHOP_KEY" "STATCORD_TOKEN" "DATABASE_URL")

while IFS='=' read -r name value || [ -n "$name" ]; do
  if [[ $name != \#* ]]; then
    if [[ "${required_variables[*]}" =~ $name && -z "${!name}" ]]; then
      echo "Variable '$name' is not set in the environment file."
      missing_variables=1
    fi
  fi
done < "$env_file"

if [ $missing_variables -eq 0 ]; then
  echo "All variables are set in the environment file."
  python3 main.py
else
  echo "Some variables are missing in the environment file."
fi
