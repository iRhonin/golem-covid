## Result 
![alt text](./covid.gif?raw=true)


## How it works
This program get a parameter from `data/owid-covid-data.csv` file (like `new_cases_per_million`) and plot every day data on the world map.
After all images generated (in `outputs`), it will gather them and create a gif.

## Usage
`python run.py --workers 4 --parameter new_deaths_per_million --start 2020-08-01 --end 2020-08-29`

## Data
- County codes: [PyGal](http://www.pygal.org/en/stable/documentation/types/maps/pygal_maps_world.html)
- Covid Data: [ourworldindata.org](https://ourworldindata.org/coronavirus)

## Commnads

1. docker build -t covid:v1 .

2. mkvirtualenv golem-covid

3. pip install gvmkit-build

4. gvmkit-build covid:v1

5. gvmkit-build covid:v1 --push

6. yagna service run

7. yagna payment init -r

8. yagna app-key create requestor

9. export YAGNA_APPKEY=

10. pip install yapapi

11. pip install -r requirements.txt

12. python run.py --workers 4 --parameter new_deaths_per_million
