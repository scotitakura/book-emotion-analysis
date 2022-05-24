from prefect.deployments import DeploymentSpec, SubprocessFlowRunner

DeploymentSpec(
    name="my-first-deployment",
    flow_location="./insert_emotions.py",
    flow_name="Emotion Analysis Pipeline",
    parameters={'msg':'Hello from my first deployment!'},
    tags=['ETL'],
    flow_runner=SubprocessFlowRunner()
)