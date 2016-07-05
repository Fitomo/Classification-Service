# Fitomo Prediction Service

  Fitomo Prediction Service is a tool to forecast users' future "health scores", based on their current steps, sleep and heart rate data as well as previous trends.

## Table of Contents
1. [Usage](#Usage)
2. [Getting started](#Getting-Started)
  1. [Clone the latest version](#Installing-Dependencies)
  2. [Install dependencies](#Installing-Dependencies)
  3. [Run the application](#Run-Application)
3. [Tech Stack](#Tech-Stack)
4. [Team](#Team)
5. [Contributing](#Contributing)
6. [License](#License)

## Usage

  This service takes requests at '/api/getPrediction'; data to include is a dictionary with the following keys:
  ```sh
    steps
    total_sleep
    resting_hr
    step_week_slope
    sleep_week_slope
    hr_week_slope
  ```
  The service will then output the predicted health score (calculated using a gradient boosting regression).

## Getting started

#### 1. Clone the latest version

  Start by cloning the latest version of the Fitomo Prediction Service on your local machine by running:

  ```sh
  $ git clone https://github.com/Fitomo/Prediction-Service.git
  $ cd Prediction-Service
  ```

#### 2. Setup Environment

  1. Setup a virtual environment for the application:

  ```sh
  $ pyvenv-3.5 env
  $ source env/bin/activate
  $ deactivate
  ```

  2. Run the following command in your terminal to refresh your bash profile:

  ```sh
  $ echo "source `which activate.sh`" >> ~/.bashrc
  $ source ~/.bashrc
  ```

  3. Refresh your bash profile by leaving then entering the directory:

  ```sh
  $ cd ..
  $ cd Prediction-Service
  ```

#### 3. Install Dependencies
  From within the root directory run the following command to install all dependencies:

  ```sh
  $ pip install -r requirements.txt
  ```

#### 4. Run the application

  Run the following command in your terminal to run the app:

  ```sh
  $ python app/app.py
  ```

  After that open in your browser the localhost with your chosen port, e.g. ``` http://localhost:5000/ ``` to access the application.

## Tech Stack

##### Back end:
- Flask
- PostgreSQL
- SQLAlchemy

##### Algorithm:
- Scikit-Learn

## Directory Layout
```
├── /algorithm/                          # Algorithm-related code
│   ├── /predicted_health_algorithm.py/  # Creating and tuning the algorithm
│   ├── /data_prep/                      # Prepping and cleaning code for the algorithm
│     ├── /clean_data.py/                # Putting data into useful format for the algorithm
│     ├── /prep_generated_data.py/       # Prepare generated user data to be cleaned
│   ├── /results/                        # Results and analysis of algorithm
│     ├── /parameter_tuning_results.py/  # Prepare generated user data to be cleaned
├── /app/                                # Server source code
│   ├── /migrations/                     # Database migration data
│   ├── /app.py/                         # Core server file
│   ├── /config.py/                      # Configs for different situations
│   ├── /manage.py/                      # Manage database migrations
│   ├── /models.py/                      # Data model
│   ├── /health_prediction.pkl/          # Prediction algorithm
├── /tests/                              # Server and client side tests
└── requirements.txt                     # List of 3rd party libraries and utilities to be installed
└── .env                                 # Environment variables
```

## Contributing

  1. Fork the repo.
  2. Clone it to your local computer
  3. Cut a namespaced feature branch from master and name it appropriately
  4. Make commits and prefix each commit with the type of work you were doing
  5. BEFORE PUSHING UP YOUR CHANGES, rebase upstream changes into your branch, fix any potential conflicts, and then push to your fork.
  6. Submit a pull request directly to the master
  7. Someone else will perform code review to keep codebase clean
  8. Fix any errors or issues raised by the reviewer and push the fixes as a single new commit
  9. Repeat until the pull request is merged.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines in detail.

## License

M.I.T
