# COVID-19 Twitter Bot & Dashboard  

This repository contains source code for the COVID-19 Twitter bot and Dashboard.

This project was created to make coronavirus data (within Ontario) more accessible, interactive and meaningful to the general public.

## Dashboard
Dashboard utilizes the Plotly Dash library to create and present visualizations. Data is pulled from a Postgresql database that is updated daily.

![](readme_imgs/dashboard_img.png)

Interactive components of the app, such as the date range selector, are handled with JavaScript clientside callbacks. In contrast to Plotly-Dash's traditional method of serverside callbacks, clientside callbacks are significantly faster since they do not need to send requests to the server.

## Twitter Bot

[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40OntarioCovid19)](https://twitter.com/OntarioCovid19)


The bot queries data from the Government of Ontario's coronavirus API, formats the data, and sends a tweet via the Twitter API.

Daily updates occur at approximately 11:00AM EDT (UTC -4).

Follow @OntarioCovid19

## Built With
Python, Flask, Dash, Tweepy, Peewee, Postgresql, Heroku, Government of Ontario API, Twitter API

## Data Sources
[https://data.ontario.ca/organization/cabinet-office](https://data.ontario.ca/organization/cabinet-office)
