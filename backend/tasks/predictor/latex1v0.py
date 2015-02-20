from worker import app
from tasks.mongoTask import MongoTask

@app.task(base=MongoTask, bind=True)
def run_prediction(self, params):
    return params
