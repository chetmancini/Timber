rm *.pyc
kill $(ps | grep 'python' | awk '{print $1}')