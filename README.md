# Visual searcher 2

Python project that shows how searching algorithms work in problems like mazes, representing the blocks that our agent checked in purple, had in mind in yellow, and not checked in white. We can set a maze changing the var problem in main, using a matrix format for the maze with 1 as a valid movement square, 0 as a block, 'i' that indicates initial position and 'g', that indicates goal position.

## Purpose

This project was created for Artificial Intelligence course in Los Lagos University with Proffesor Joel Tores.

The project is an application in python that serves a pure html frontend and a websocket connection for the frontend for the asyncronous progression of the algorithms. The application let us choose between different search algorithms applied to a maze 

* [Inteligencia Artificial 2024 semestre 1 por Joel Torres](https://github.com/profeJoel/IA2024-1)

## Technologies

This project use FastAPI for serve a simple API and backend, this API serves 2 endpoint, one is the frontend as a html and a websocket connection that starts the selected algorithm in the frontend and updates with info every iteration of the alg.

## Usage

The best way to try the application is in local with dev mode.

Instructions:

1. built venv ```python3 -m venv venv```
2. select venv interpreter ```source venv/bin/activate``` in Mac or Linux and ```.\venv\Scripts\activate``` in Windows
3. install dependencies ```pip install -r requirements.txt```
4. run uvicorn ```uvicorn main:app --reload```

Now port 8000 should be executing the backend, you can get the frontend going to ```localhost:8000``` in web browser

**Note** Notice too that you can run a production execution running the dockerfile, if you need to change the port (for example in case that you have to expose default http port like 80), i recommend using --port cmd or changing the port in dockerfile in case that you are using docker

## Demo

<a href="https://p02--visual-searcher-2--f4p8zgqlvr7n.code.run/" target="_blank">Live demo is available</a> using deployment service of nortflank.
Be aware project is not intended to work perfectly in online deployment, so live demo may actually work not as well as in local. Also the demo is limited in terms of procces capacity and memory
