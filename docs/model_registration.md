## Model Registration
The model artifact should be registered as it allows "one click" deployment for real time inferencing hosted on AKS or ACI. Even if the intention is to use it for batch inferencing with Azure ML pipelines it is a more organized way as shown below to keep full context of how the model was built verse just storing the pickle file off in a cloud storage location.

In context of this example pipeline, training has been completed in [iris_supervised_model.py](/azureml/iris_supervised_model.py). The best model accuracy has been recorded in the tags of the pipeline run. 

As discussed in the [Using Run Context to manage the pipeline execution](/docs/run_context.md) doc, retreive the parent pipeline run context with `parentrun = run.parent` and review the tags that have been set.

The below code block shows getting the accuracy score from the tag dictionary for the current pipeline run, but also an alternative method to interegate previous steps in the pipeline to retrieve the tags by using `parentrun.get_children()`

```
tagsdict = parentrun.get_tags()
if (tagsdict.get("best_model")) != None:
    model_type = tagsdict['best_model']
    model_accuracy = float(tagsdict['accuracy'])
    training_run_id = parentrun.id
else:
    for step in parentrun.get_children():
        print("Outputs of step " + step.name)
        if step.name == training_step_name:
                tagsdict = step.get_tags()
                model_type = tagsdict['best_model']
                model_accuracy = float(tagsdict['accuracy'])
                training_run_id = step.id
```

The model can be registered directly to the workspace, but the context of how the model was built is then disconnected from the training pipeline. Instead, the model will be registered from the pipeline run object. To do this the model artifact (model.pkl file) needs to be uploaded to the parent run. 
```
# to register a model to a run, the file has to be uploaded to that run first.
model_output = os.environ['AZUREML_DATAREFERENCE_model_output']
parentrun.upload_file('model.pkl',model_output+'/model.pkl')
```

Next, see if the model name is already registered. If so, record the accuracy score of the previous model to compare against the new model. If this is the first time the model has been trained it won't exist in the registry so set the accuracy to beat equal to 0.
```
try:
    model = Model(ws, model_name)
    acc_to_beat = float(model.properties["accuracy"])
except:
    acc_to_beat = 0
```

Compare the new model accuracy with the previous model accuracy to beat and if the model is better, register it. *Note: the model is being registered via `parentrun.register_model` and not `Model.register_model`. This is important as it nicely ties the registered model and artifact back to all the context of how it was created.*
```
if model_accuracy > acc_to_beat:
    print("model is better, registering")

    # Registering the model to the parent run (the pipeline). The entire pipeline encapsulates the training process.
    model = parentrun.register_model(
                       model_name=model_name,                # Name of the registered model in your workspace.
                       model_path=model_path,  # Local file to upload and register as a model.
                       model_framework=Model.Framework.SCIKITLEARN,  # Framework used to create the model.
                       model_framework_version=sklearn.__version__,  # Version of scikit-learn used to create the model.
                       sample_input_dataset=dataset,
                       resource_configuration=ResourceConfiguration(cpu=1, memory_in_gb=0.5),
                       description='basic iris classification',
                       tags={'quality': 'good', 'type': 'classification'})
```

Set additional properties for accuracy and model_type so that the next time training is ran the current accuracy will be compared against that model (just like above)
```
model.add_properties({"accuracy":model_accuracy,"model_type":model_type})
model.add_tags({"accuracy":model_accuracy,"model_type":model_type})
```

### Access the run logs, outputs, code snapshots from registered model
In the model registry, when registering from the run itself, it hyperlinks to the run id.

![Model](/docs/images/model_image.png)

This links back to the pipeline run. 
![Pipeline](/docs/images/pipeline_image.PNG)

Notice that when clicking on the iris_supervised_model.py step, there is access to the outputs/logs, metrics, and even the snapshots of the code used to generate the model artifact that is registered. 
![Snapshot](/docs/images/snapshot_image.PNG)

#### Conclusion
Registering the model from the pipeline run gives complete context of how the model was built and registered! Its sets up real time and bach inferencing deployment as next steps.