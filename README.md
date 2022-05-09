# Parking Lot Management

## Prerequisites

1. Python 3.7.10
2. Pipenv

## Intallation
1. Clone the Git repository and goto the project root directory.
```sh
git clone https://gitlab.ergov.com/abid/parking-lot-monitoring.git
cd parking-lot-monitoring
cp .env.example .env
```
2. Install the dependencies using pipenv and activate virtual environment.
```sh
pipenv install
pipenv shell
```
3. Run the server using the below command
```sh
pipenv run flask run
```

The application can be browse with the below URL.
`http://localhost:5000`

## Useful Commands
A couple of helper commands are given below.
1. DB initialization
```sh
pipenv run flask db init
```
2. Migrate the database
```sh
pipenv run flask db migrate
```

## Some helping commands for DB usage
1. Create/ run Postgres/ Pgadmin container
```sh
docker pull postgres
docker run -p 5432:5432 --name postgresdb -e POSTGRES_PASSWORD=admin -d postgres

docker pull dpage/pgadmin4
docker run -p 5050:80  -e "PGADMIN_DEFAULT_EMAIL=admin@example.com" \
         -e "PGADMIN_DEFAULT_PASSWORD=password" \
         -d dpage/pgadmin4
```
2. 
```sh
# Create DB user for the project
create database parking_lot;
create user parking_lot with encrypted password 'password';
grant all privileges on database parking_lot to parking_lot;
# Login to the DB (host/ username maybe change accordingly)
psql -h 127.0.0.1 -d parking_lot -U admin -p 5432
```

## Conclusion
An useful user data script while launching Amazon EC2 instance to deploy flask project.
[Flask Deployment in AWS](https://github.com/abidkhan484/aws-practice/tree/main/flask-deployement)

Special thanks to [ParkingLot Repository](https://github.com/olgarose/ParkingLot).
