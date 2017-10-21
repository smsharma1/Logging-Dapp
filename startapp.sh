if [ ! $# == 4 ]; then
    echo "Usage: $0 OARS_username OARS_password ip_address port"
    exit
fi

user=$1
pass=$2
echo $user $pass

multichaind chain1@$3:$4 -daemon
multichain-cli chain1 getaddresses | python getpermissions.py
multichain-cli chain1 stop
