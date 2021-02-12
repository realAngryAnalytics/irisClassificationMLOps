# MLOps and AzureML example for irisClassification
Microsoft has extensive resources for MLOps, but the GitHub repository can be a little overwhelming. The intention for this repository is to provide a simple example of MLOps and AzureML.

Currently this repository features a multi-step training pipeline that registers a model if training is better than previous run. This is integrated with a GitHub Action to kick off the pipeline anytime there is a code checkin. It also shows how to publish and schedule the pipeline. 

![AzureML Pipeline](/docs/images/pipeline_image.PNG)

review .gitignore to see that config.json is not included and should be created locally with the following format
{
    "subscription_id": "***",
    "resource_group": "***",
    "workspace_name": "***"
}

Files to review
[iris_supervised_model.py](iris_supervised_model.py) is the original training file (see footnote below) that would be typical for a local training script.
[azureml/iris_supervised_model.py](azureml/iris_supervised_model.py) is the modified version of the training file to get the run context of the AzureML experiment and log metrics and set properties.
[azureml/train_pipeline.ipynb](azureml/train_pipeline.ipynb) is an interactive notebook that is the "driver" script to create (and run) the AzureML training pipeline.
[azureml/train_pipeline.py](azureml/train_pipeline.py) is the non-interactive "driver" script that is used in the GitHub Action to build and run the training pipeline. This script utilizes a services principal to connect to the AzureML workspace as it is non-interactive. Complete steps of service principal authentication setup can be found [here](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/manage-azureml-service/authentication-in-azureml/authentication-in-azureml.ipynb)
[.github/workflows/iristrain.yaml](.github/workflows/iristrain.yaml) is the GitHub Action file that is executed each time a code checkin occurs to run train_pipeline.py. It leverages GitHub Secrets to pass as environment variables to the python script.


AzureML MLOps
https://github.com/microsoft/MLOpsPython

this work is based on the original work of asherif844 and is being used to demonstrate github actions for MLOps
https://github.com/asherif844/irisClassification