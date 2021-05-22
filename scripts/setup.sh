source venv/bin/activate
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "No venv found - creating a new one"
    apt-get install python3-venv
    python3 -m venv venv
    source venv/bin/activate
    python -m pip install -U pip
else
    echo "venv found"
fi
python -m pip install -U pip

pip install -r requirements.txt
