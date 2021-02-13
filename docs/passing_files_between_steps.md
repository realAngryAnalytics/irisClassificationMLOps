## Passing Files and Datasets between steps
Other than a few blogs I have found on the internet, instructions on how to properly pass files or datasets between steps are hard to find. 

![AzureML Pipeline](/docs/images/pipeline_image.PNG)

In the above image you can see that irisdata is passed into iris_supervised_model.py and then model_output is the output. When you define the pipeline in the driver script, the input data is a DataReference object and any data passed between steps is a PipelineData object.

```
from azureml.core.datastore import Datastore
from azureml.data.data_reference import DataReference
ds = ws.get_default_datastore()
print("Default Blobstore's name: {}".format(ds.name))

dataset_ref = DataReference(
    datastore=ds,
    data_reference_name='irisdata',
    path_on_datastore="data/sample_data.csv")
print("DataReference object created")
```

```
from azureml.pipeline.core import Pipeline, PipelineData
model_output = PipelineData("model_output",datastore=ds)
print("PipelineData object created for models")
```

In the PythonScriptStep, utilize the input and output parameters.