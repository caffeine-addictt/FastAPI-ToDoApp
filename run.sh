#!/usr/bin/env/bash

echo -e "\n========== Runing in production mode ==========\n"


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
npm run --prefix src/tailwindcss prod


echo -e "\n========== Starting up server ==========\n"
uvicorn --port 8080 src:app
