## Leverging Run Context 

Azure ML allows you to execute Python script in a container that you can send/run on AML compute clusters instead of your local machine. This could be a data transformation script, a training script, or an inferencing script. The below examples shows how you would do this for a simple training script ran stand alone (in absence of a pipeline) 

```
from azureml.core import Experiment
experiment_name = 'train-on-amlcompute'
experiment = Experiment(workspace = ws, name = experiment_name)

from azureml.core import ScriptRunConfig
src = ScriptRunConfig(source_directory=project_folder, 
                      script='train.py', 
                      compute_target=cpu_cluster, 
                      environment=myenv)
 
run = experiment.submit(config=src)
```

These "runs" are executed via a submit command from an experiment. Being able to log information to the run from within the script itself (in the above example train.py) is key. 

In this repo, [iris_supervised_model.py](./azureml/iris_supervised_model.py) leverages run context to log metrics, plots, and properties. 
`run = Run.get_context()`
This is the magic line that connects your vanilla Python script to the context of the run, inside the experiment, inside the Azure ML workspace. 

*TIP* When relying on run context of Azure ML (such as environment variables being passed in from the driver script) performing the following check early in your script can allow you to set defaults for anything that would have been passed in. This allows you to test locally and save time.
```
if (run.id.startswith('OfflineRun')):
	os.environ['AZUREML_DATAREFERENCE_irisdata'] = '.\sample_data.csv'
	os.environ['AZUREML_DATAREFERENCE_model_output'] = '.\model_output'
```

Now, you can log metrics
`run.log("accuracy",best_score)`
and tables
`run.log_confusion_matrix('Confusion matrix '+name, confusion_matrix(Y_train, model.predict(X_train)))`
See this [sample notebook](https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/track-and-monitor-experiments/logging-api/logging-api.ipynb) for all the things you can do with the logging api.


### Using run context to manage the pipeline execution
In a pipeline, each run is at the step level, or a child of a parent run which is the pipeline itself. 

![Pipeline Parent Child](/docs/images/pipeline_parent_child_image.PNG)

What we might choose to do is to log important metrics or properties at the pipeline level rather than at the step level. Or we could do both. *run.parent* will give the parent run context. The code below sets the two properties by passing in a dictionary as the parameter and those same values on two tags also.

```
run.parent.add_properties({'best_model':best_model[0],'accuracy':best_score})
run.parent.tag("best_model",best_model[0])
run.parent.tag("accuracy",best_score)
```

Properties are immutable while tags are not, however tags are more prodominent in the Azure ML UI so they are easier to read. 
![tags](/docs/images/tags_image.png)

To review the added properties you have to click "Raw JSON" under "see all properties".
![see all properties](/docs/images/see_all_properties.png)

![properties](/docs/images/properties_image.png)

Now that the results of our training are published to the parent pipeline tags (and properties), they can be used to control what happens in execution of later steps. In this example, the accuracy score is going to control if this model is will be registered or not. For details, review [Model Registration](/docs/model_registration.md)





set immutable properties or tags (not immutable). 
`run.add_properties({'best_model':best_model[0],'accuracy':best_score})`



