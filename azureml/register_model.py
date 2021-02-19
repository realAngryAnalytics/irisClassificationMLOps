from azureml.core import Run, Workspace
from azureml.core import Model
from azureml.core.resource_configuration import ResourceConfiguration
import sklearn
import sys
import os


print("...getting run context, experiment, and workspace")
run = Run.get_context()
# if (run.id.startswith('OfflineRun')):
#     # ws = Workspace.from_config()
#     # exp = Experiment(ws,'iris_classifcation')
# else:
exp = run.experiment
ws = run.experiment.workspace
parentrun = run.parent




print("...getting arguments (model_name, training_step_name)")
model_name = sys.argv[2]
print("model_name",model_name)
training_step_name = sys.argv[4] 
print("training_step_name",training_step_name)


training_run_id = None
for step in parentrun.get_children():
    print("Outputs of step " + step.name)
    if step.name == training_step_name:
            step.download_file('model_output',output_file_path='.')
            model_type = step.get_properties()['best_model']
            model_accuracy = float(step.get_properties()['accuracy'])
            training_run_id = step.id    

if (training_run_id == None):
    sys.exit("Failed to retrieve training step for model information")

dataset = os.environ['AZUREML_DATAREFERENCE_irisdata']
#model appears to be a mount path
model_output = os.environ['AZUREML_DATAREFERENCE_model_output']
print("model path",model_output)
print("files in model path",os.listdir(path=model_output))
#the as the model is registered via the run below, upload the model file to the run

run.upload_file('model.pkl',model_output+'/model.pkl')
# will actually register the model to the parent which encapsulates all the steps 
parentrun.upload_file('model.pkl',model_output+'/model.pkl')

model_path = "model.pkl"


print("...working directory")
print(os.listdir(path='.'))

# model_path = 'model_output'
# with open(model_path, 'wb') as f:
#     f.write(model)

try:
    model = Model(ws, model_name)
    acc_to_beat = float(model.properties["accuracy"])
except:
    acc_to_beat = 0

acc_to_beat = 0
print("accuracy to beat",acc_to_beat)
if model_accuracy > acc_to_beat:
    print("model is better, registering")
    model = parentrun.register_model(
                       model_name=model_name,                # Name of the registered model in your workspace.
                       model_path=model_path,  # Local file to upload and register as a model.
                       model_framework=Model.Framework.SCIKITLEARN,  # Framework used to create the model.
                       model_framework_version=sklearn.__version__,  # Version of scikit-learn used to create the model.
                       #sample_input_dataset=dataset,
                       #sample_output_dataset=output_dataset,
                       resource_configuration=ResourceConfiguration(cpu=1, memory_in_gb=0.5),
                       description='basic iris classification',
                       tags={'quality': 'good', 'type': 'classification'})
    model.add_properties({"accuracy":model_accuracy,"model_type":model_type})
else:
    print("model didn't perform better, not registering")


