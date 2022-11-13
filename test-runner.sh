#!/bin/bash

# start=`gdate +%s.%3N`  # on Linux use simply: date +%s.%3N
# curl -F uploadFile=@book.zip http://localhost:8082/upload -o output.tmp
# end=`gdate +%s.%3N`  # on Linux use simply: date +%s.%3N
# echo Execution time was `echo $end - $start | bc` seconds.

tests_amount=10
test_file_1=test-file-1.tmp
test_file_2=test-file-2.tmp
first=8082
last=8085

send_to_file () {
    if [ $1 -eq 8081 ]; then
        echo "express-fileupload,$2,$3,$4" >> test-results.csv
    elif [ $1 -eq 8082 ]; then
        echo "express-formidable,$2,$3,$4" >> test-results.csv
    elif [ $1 -eq 8083 ]; then
        echo "express-multer,$2,$3,$4" >> test-results.csv
    elif [ $1 -eq 8084 ]; then
        echo "fastapi-default,$2,$3,$4" >> test-results.csv
    elif [ $1 -eq 8085 ]; then
        echo "flask-default,$2,$3,$4" >> test-results.csv
    else
        echo "fastapi-streaming,$2,$3,$4" >> test-results.csv
    fi
}

for port in $(seq $first $last)
do

    for test_no in $(seq 0 $tests_amount)
    do
        start=`gdate +%s.%3N`  # on Linux use simply: date +%s.%3N
        curl -F uploadFile=@$test_file_1 http://localhost:$port/upload -o output.tmp
        end=`gdate +%s.%3N`  # on Linux use simply: date +%s.%3N
        send_to_file $port "test_file_1" $test_no `echo $end - $start | bc`
    done

    for test_no in $(seq 0 $tests_amount)
    do
        start=`gdate +%s.%3N`  # on Linux use simply: date +%s.%3N
        curl -F uploadFile=@$test_file_2 http://localhost:$port/upload -o output.tmp
        end=`gdate +%s.%3N`  # on Linux use simply: date +%s.%3N
        send_to_file $port "test_file_2" $test_no `echo $end - $start | bc`
    done
    
done
