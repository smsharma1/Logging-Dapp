if [ ! $# == 2 ]; then
    echo "Usage: $0 ip_address port"
    exit
fi

multichaind chain1@$1:$2 -daemon
python getpermissions.py
python manage.py runserver 5000
multichain-cli chain1 stop
