from prefect.deployments import DeploymentSpec
from prefect.flow_runners import SubprocessFlowRunner
from prefect.orion.schemas.schedules import IntervalSchedule
from datetime import timedelta

DeploymentSpec(
    name="emotion-deployment",
    flow_location="./insert_emotions.py",
    flow_name="Emotion Analysis Pipeline",
    parameters={'msg':'Hello from my first deployment!'},
    tags=['ETL'],
    schedule=IntervalSchedule(interval=timedelta(minutes=5)),
    flow_runner=SubprocessFlowRunner()
)