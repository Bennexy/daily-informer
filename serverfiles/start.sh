
ABSPATH=/opt/daily-informer

cd $ABSPATH

source $ABSPATH/venv/bin/activate
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "No venv found - creating a new one"
    sudo apt-get install python3-venv
    python3 -m venv venv
    source venv/bin/activate
    python -m pip install -U pip
else
    echo "venv found"
fi
touch buffer
python -m pip install -U pip

pip install -r requirements.txt > buffer

rm -rf buffer


sudo venv/bin/python $ABSPATH/daily_informer/telegram/__init__.py



