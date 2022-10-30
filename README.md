This is Django Channels project to fetch data about cryptocurrencies from external sources in real-time

## Setup
Provide all env variables to env.env, then from project folder run

    docker-compose -f ./deploy/docker-compose.yml up

Make sure you have docker and docker-compose installed

## API
Connect to `ws://localhost:8000/ws/polygon/quotes` to start receiving crypto quotes data from Polygon.io

    wscat -c ws://localhost:8000/ws/polygon/quotes

You can filter quotes you need. Add `pairs` parameter to uri

    wscat -c ws://localhost:8000/ws/polygon/quotes?pairs=BTC-USD,ETH-BTC

To see the list of all available quotes connect to `ws://localhost:8000/ws/polygon/quotes/all`

    wscat -c ws://localhost:8000/ws/polygon/quotes/all

    