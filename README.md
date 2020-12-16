# rapi-service
Restaurant API service (DAQ 2020 project)

This Restaurant API service provides information about restaurants in Bangkok.
This information includes basic information of restaurants and their received ratings from Michelin Guide, Google and tripadvisor.com.

## Team members
| Student Id | Name | GitHub account |
|------------|------|----------------|
| 6110545490 | Nutthanich Narphromar | [NutthanichN](https://github.com/NutthanichN) |
| 6110545554 | Tetach Rattanavikran | [theethaj](https://github.com/theethaj) |
| 6110545627 | Wijantra Cojamnong | [Wijantra](https://github.com/Wijantra) |

## Requirement
Python 3.7 or higher

## Setting up
1. Clone this repository using this command
    ```
    > git clone https://github.com/NutthanichN/rapi-service.git
    ```
2. Go to the project root directory `rapi_service`
2. Install required packages from `requirements.txt` using this command
    ```
    > pip install -r requirements.txt
    ```

## Running application
1. Make sure that you are in the project root folder `rapi_service`
2. To run an API service and the site, run python file `app.py` using this command
    ```
    > python app.py 
    ```
3. Open a browser and go to http://127.0.0.1:5000/rapi-site/
   * If you want to test all API endpoints, go to http://127.0.0.1:5000/rapi/ui/
