rm -rf credentials.json
wget http://212.83.154.157/public/credentials.json

if [ ! -z $1 ]; then
    TestCase=".${1}"
else
    TestCase=''
fi

if [ ! -z $2 ]; then
    Test=".${2}"
else
    Test=''
fi


python -m unittest tests$TestCase$Test
rm -rf test.json
