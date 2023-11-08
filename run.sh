echo "Setting up development environment"
echo "Make sure that you are in the venv"
echo "Starting in 5..."
sleep 5

pip install --upgrade -r requirements.txt

echo -e "\n========== Starting up server ==========\n"
uvicorn --reload src:app
