from quart import Quart, request, Response, websocket
import json
import asyncio
from functools import wraps

from brewhouse_controller import BrewhouseController

controller = BrewhouseController()

app = Quart(__name__)
        
@app.websocket('/ws')
async def ws():
    while True:
        new_data = controller.broadcast_data()
        await websocket.send(json.dumps(new_data))
        await asyncio.sleep(1)

@app.route("/start", methods=["POST"])
async def run():
    running = controller.start()
    return Response(json.dumps(running))

@app.route("/stop", methods=["POST"])
async def stop():
    running = controller.stop()
    return Response(json.dumps(running))

@app.route("/pump", methods=["GET"])
async def get_pumps():
    return Response("True")

@app.route("/pump/<id>", methods=["GET","POST"])
async def pump(id):
    if request.method == "GET":
        pump_state = controller.get_pump_state(id)
        return Response(json.dumps(pump_state), mimetype="application/json")
    elif request.method == "POST":
        pump_state = controller.cycle_pump_state(id)
        return Response(json.dumps(pump_state), mimetype="application/json")

@app.route("/step", methods=["GET", "POST"])
async def steps():
    if request.method == "GET":
        step = controller.get_current_step()
        return Response(json.dumps(step), mimetype="application/json")
    elif request.method == "POST":
        steps = controller.set_step(await request.json)
        return Response(json.dumps(steps), mimetype="application/json")

# @app.route("/step/<index>", methods=["GET", "PUT", "DELETE"])
# async def step(index):
#     if request.method == "GET":
#         step = controller.get_step_by_index(int(index))
#         return Response(json.dumps(step), mimetype="application/json")
#     elif request.method == "POST":
#         step = controller.update_step(int(index))
#         return Response(json.dumps(step), mimetype="application/json")
#     elif request.method == "DELETE":
#         success = controller.delete_step(int(index))
#         return Response(json.dumps(success), mimetype="application/json")

# @app.route("/step/current", methods=["GET"])
# async def current_step():
#     current_step = controller.get_current_step()
#     return Response(json.dumps(current_step), mimetype="application/json")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)