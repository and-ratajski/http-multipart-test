#!/bin/bash

first_port=30081
last_port=30085
tests_amount=10
test_file_1=test-file-1.tmp
test_file_2=test-file-2.tmp
test_file_3=test-file-3.tmp
test_output=test-results-limit-300m.csv

write_to_file () {
    if [ $1 -eq 8081 ]; then
        echo "express-fileupload,$2,$3,$4" >> $test_output
    elif [ $1 -eq 8082 ]; then
        echo "express-formidable,$2,$3,$4" >> $test_output
    elif [ $1 -eq 8083 ]; then
        echo "express-multer,$2,$3,$4" >> $test_output
    elif [ $1 -eq 8084 ]; then
        echo "fastapi-default,$2,$3,$4" >> $test_output
    elif [ $1 -eq 8085 ]; then
        echo "flask-default,$2,$3,$4" >> $test_output
    else
        echo "fastapi-streaming,$2,$3,$4" >> $test_output
    fi
}

for port in $(seq $first_port $last_port)
do

    for test_no in $(seq 1 $tests_amount)
    do
        start=`gdate +%s.%3N`  # on Linux use simply: `date +%s.%3N`
        curl -F uploadFile=@$test_file_1 http://localhost:$port/upload -o output.tmp
        end=`gdate +%s.%3N`  # on Linux use simply: `date +%s.%3N`
        write_to_file $port "test_file_1" $test_no `echo $end - $start | bc`
    done

    for test_no in $(seq 1 $tests_amount)
    do
        start=`gdate +%s.%3N`  # on Linux use simply: `date +%s.%3N`
        curl -F uploadFile=@$test_file_2 http://localhost:$port/upload -o output.tmp
        end=`gdate +%s.%3N`  # on Linux use simply: `date +%s.%3N`
        write_to_file $port "test_file_2" $test_no `echo $end - $start | bc`
    done

    for test_no in $(seq 1 $tests_amount)
    do
        start=`gdate +%s.%3N`  # on Linux use simply: `date +%s.%3N`
        curl -F uploadFile=@$test_file_3 http://localhost:$port/upload -o output.tmp
        end=`gdate +%s.%3N`  # on Linux use simply: `date +%s.%3N`
        write_to_file $port "test_file_3" $test_no `echo $end - $start | bc`
    done
    
done
