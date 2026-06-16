# cs145-IoT-Cup

run this to go into the virtual env
```bash
source ./cs145/bin/activate
```

run this to start the wireguard (u need the `/etc/wireguard/cs145.conf` file)
```bash
sudo wg-quick cs145
```


run this to start the server
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000
```

run this to run the `test.py` script
```bash
python3 test.py
```


if something doesn't work try downloading stuff that wasn't in the `requirements.txt` file
```bash
pip3 install uvicorn fastapi requests
```