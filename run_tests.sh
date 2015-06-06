wget $oauth1
wget $oauth2

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
