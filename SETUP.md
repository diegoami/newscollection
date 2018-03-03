# SETUP INSTRUCTIONS

This file describes how to set up TECHCONTROVERSY to run locally.


# Configuration files

The main configuration file is _config.yml_, in the main directory of the project. If you need to change the locations of files used by the application this is the file that needs to be edited.


# Retrieving the data

Retrieve the latest dump from https://s3.console.aws.amazon.com/s3/buckets/techcontroversy/ (dump*.tgz)
Import the dump into a mysql user called 'tnaggregator'. From the mysql prompt execute

~~~~
SET AUTOCOMMIT=0;
source <dumpfile>.sql;
COMMIT;
GRANT ALL ON tnaggregator.* TO '<youruser>'@'%';
GRANT CREATE ON tnaggregator TO '<youruser>'@'%';
FLUSH PRIVILEGES;
~~~~

# Retrieving the models

Retrieve the latest tech articles models collection from https://s3.console.aws.amazon.com/s3/buckets/techcontroversy/ (_techarticles.tgz_)
The default configuration assumes that they are deployed under _/media/diego/QData_ (see root_dir in _config.yml_)

# Setting up Python

It is assumed that you use Python and Anaconda. Get the latest definition file from config/conda/ and create a conda environment from it. This is where you will run your application.

# Configuring for local environment

By default, database connection info should be setup into _/media/diego/keys/db_coords.yml_ (you can change that in config.yml). This is important to set up your access to data and to define the admin console password (signin_key).

# Starting the application

Switch to the conda environment you created and from the main directory execute _python boot_web.py_ . You should be able to access the site from http://localhost:8081








