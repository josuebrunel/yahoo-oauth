rm -rf credentials.json
wget http://212.83.154.157/public/credentials.json
python -m unittest tests
rm -rf test.json
