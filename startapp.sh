if [ ! $# == 2 ]; then
    echo "Usage: $0 ip_address port"
    exit
fi
echo "Generating Keys"
python generatekeys.py
echo "Ignore the error that accompanies if it is said that chain already exists or multichaind is already running"
multichaind chain1@$1:$2 -daemon
python getpermissions.py
echo "Note the username "
python manage.py runserver 5000
multichain-cli chain1 stop
