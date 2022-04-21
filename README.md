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
2. Install the dependencies using pipenv
```sh
pipenv install
```
3. Run the server using the below command
```sh
pipenv run python -m flask run
```

The application can be browse with the below URL.
`http://localhost:5000`

Special thanks to [ParkingLot Repository](https://github.com/olgarose/ParkingLot).
