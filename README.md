# ILamp

ILamp is a lamp build from the sense hat and a raspberry pi capable of interacting with the web.

## Requirements
  - [Python 3.10](https://www.python.org/downloads/)
  - Raspberry PI
  - Sense hat
  - [Adafruit IO account](https://io.adafruit.com/)
  - Packages
    - [sense-hat](https://pypi.org/project/sense-hat/)
    ```sh
    pip install sense-hat
    ```
    - [adafruit-io](https://pypi.org/project/adafruit-io/)
    ```sh
    pip install adafruit-io
    ```
## Setup
  - install all the required packages
  - copy config.example.json to config.json and fill in all the data
  - run the application with the following command
  ```sh
  python main.py
  ```