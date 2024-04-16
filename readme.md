# Python Data Challenge

Attached [web_challenge.csv](./web_challenge.csv) contains sea routes extracted from AIS data. These are the routes between ports of Hamburg and Bremerhaven in Germany.

The file contains the following columns:
* route_id - some arbitrary route id
* from_port - route origin
* to_port - route destination
* leg_duration - trip duration in milliseconds
* points - an array of vessel observations from GPS where observation is [longitude, latitude, timestamp in epoch milliseconds, actual vessel speed in knots]

Please store the data in a database of your choice (can use Docker) and create a REST API (FastAPI required) that will allow the following operations.

* GET /routes
    * Returns a list of all routes metadata
    * Each route should contain the following fields:
        * route_id
        * from_port
        * to_port
        * leg_duration

* GET /routes/{route_id}
    * Returns a GeoJSON object with the route points

PS. Please publish the solution to your GitHub and invite us to review it.

## ---------------------------------------------------------------------
python -m uvicorn main:app --reload

http://localhost:8000/docs#/