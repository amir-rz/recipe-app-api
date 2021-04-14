if [[ "$1" == "test" ]]; then
    docker-compose run app sh -c "python3 manage.py test && flake8"
# elif [[ "$1" == "runserver"]]; then
#     docker-compose run app sh -c "python3 manage.py runserver"
# elif [[ "$1" == "makemigrations"]]; then
#     docker-compose run app sh -c "python3 manage.py makemigrations $2"
# elif [[ "$1" == "migrate"]]; then
#     docker-compose run app sh -c "python3 manage.py migrate $2"
else
    echo "docker-compose run app sh -c '____ && flake8 '  : "
    read commandToRun
    
    docker-compose run app sh -c "python3 manage.py $commandToRun && flake8"
fi