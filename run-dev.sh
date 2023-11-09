#!/usr/bin/env/bash

echo -e "\n========== Runing in development mode ==========\n"


# Build venv if not existing
if [ ! -d "venv" ]; then
  echo "Building venv"
  python3 -m venv venv
fi

if [ -d "venv/Scripts" ]; then
  echo "Activating venv for windows"
  venv\Scripts\activate
elif [ -d "venv/bin" ]; then
  echo "Activating venv for linux/mac"
  source venv/bin/activate
else
  echo -e "Looks like something went wrong building the venv, No [venv/Scripts/ or venv/bin/ detected]"
  exit 1
fi


echo -e "\n========== Building Dependencies ==========\n"
pip install --upgrade -r requirements.txt


# Run tailwind builder and app in parallel
echo -e "\n========== Starting server [w/ reload] & tailwind [w/ reload] in parallel ==========\n"
uvicorn --reload --port 8080 src:app & npm run --prefix src/tailwindcss dev
