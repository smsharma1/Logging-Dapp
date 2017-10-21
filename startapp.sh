if [ ! $# == 2 ]; then
    echo "Usage: $0 ip_address port"
    exit
fi

multichaind chain1@$3:$4 -daemon
python getpermissions.py
python manage.py runserver
multichain-cli chain1 stop
