import argparse

import pandas
import pygal


def update_county_codes(data, country_codes):
    return data.merge(country_codes, left_on='location', right_on='country', how='right').fillna(0)


def plot(data, date, parameter: str, output: str):
    clean_title = parameter.replace('_', ' ').title()
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = f'{clean_title} of Corona Virus\n{date}'
    worldmap_chart.add(f'{date}', data)
    worldmap_chart.show_legend = False
    worldmap_chart.render_to_png(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', required=True)
    parser.add_argument('--data', required=True)
    parser.add_argument('--country-codes', required=True)
    parser.add_argument('--parameter', default='new_deaths')
    parser.add_argument('--output', required=False)

    args = parser.parse_args()
    date = args.date
    parameter = args.parameter
    data_path = args.data
    country_codes_path = args.country_codes
    output = args.output or f'{date}.png'

    data = pandas.read_csv(data_path)
    country_codes = pandas.read_csv(country_codes_path)

    data = data[data['date'] == date]
    data = update_county_codes(data, country_codes)
    data = data[data[parameter] != 0]
    
    plot_data = data[['code', parameter]]
    plot_data = plot_data.set_index('code').to_dict()[parameter]
    plot(plot_data, date, parameter, output)
