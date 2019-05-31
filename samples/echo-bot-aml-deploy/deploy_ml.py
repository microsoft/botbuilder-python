from azureml.core.compute import AksCompute
from azureml.core.model import Model, InferenceConfig
from azureml.core.webservice import AksWebservice

workspace_name = ""
subscription_id = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
resource_group = "XXXXXXXXXXXXXXXXX"
workspace_region = "eastus2"
https_cert = "XXXXX"
aks_name = "XXXXXXX"
aks_service_name = 'XXXXXXXXX'

ws = Workspace.create(name=workspace_name,
                      subscription_id=subscription_id,
                      resource_group=resource_group,
                      location=workspace_region,
                      exist_ok=True)

# Provision AKS cluster
prov_config = AksCompute.provisioning_configuration(vm_size="Standard_D14")
prov_config.enable_ssl(leaf_domain_label=https_cert)
# Create the cluster
aks_target = ComputeTarget.create(
    workspace=ws, name=aks_name, provisioning_configuration=prov_config
)

inference_config = InferenceConfig(runtime="python",
                                   entry_script="aml_app.py",
                                   conda_file="myenv.yml",
                                   extra_docker_file_steps='dockerfile'
                                   )


aks_python_bot = AksWebservice.deploy_configuration(autoscale_enabled=False,
                                                    num_replicas=3,
                                                    cpu_cores=2,
                                                    memory_gb=4,
                                                    auth_enabled=False)

aks_service = Model.deploy(ws,
                           models=['aml_app.py'],
                           inference_config=inference_config,
                           deployment_config=aks_python_bot,
                           deployment_target=aks_target,
                           name=aks_service_name)

aks_service.wait_for_deployment(show_output=True)
print(aks_service.state)
