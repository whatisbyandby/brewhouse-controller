from quart import Quart, request, Response
import json

from brewhouse_controller import BrewhouseController

controller = BrewhouseController()

app = Quart(__name__)

@app.route("/run", methods=["POST"])
async def run():
    running = controller.run()
    return Response(json.dumps(running))

@app.route("/stop", methods=["POST"])
async def stop():
    running = controller.stop()
    return Response(json.dumps(running))

@app.route("/step", methods=["GET", "POST"])
async def steps():
    if request.method == "GET":
        steps = controller.get_steps()
        return Response(json.dumps(steps), mimetype="application/json")
    elif request.method == "POST":
        steps = controller.set_steps(await request.json)
        return Response(json.dumps(steps), mimetype="application/json")

@app.route("/step/<index>", methods=["GET", "PUT", "DELETE"])
async def step(index):
    if request.method == "GET":
        step = controller.get_step_by_index(int(index))
        return Response(json.dumps(step), mimetype="application/json")
    elif request.method == "POST":
        step = controller.update_step(int(index))
        return Response(json.dumps(step), mimetype="application/json")
    elif request.method == "DELETE":
        success = controller.delete_step(int(index))
        return Response(json.dumps(success), mimetype="application/json")
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)