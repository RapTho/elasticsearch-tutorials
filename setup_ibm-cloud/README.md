# Setup Elasticsearch and Kibana on IBM Cloud

## Create Database for Elasticsearch service

Create an instance of this service: [https://cloud.ibm.com/databases/databases-for-elasticsearch/create](https://cloud.ibm.com/databases/databases-for-elasticsearch/create)

## Deploy Kibana on IBM Code Engine

Use the following instructions to deploy Kibana as a container on IBM Code Engine:<br />
[https://cloud.ibm.com/docs/databases-for-elasticsearch?topic=databases-for-elasticsearch-kibana-code-engine-icd-elasticsearch](https://cloud.ibm.com/docs/databases-for-elasticsearch?topic=databases-for-elasticsearch-kibana-code-engine-icd-elasticsearch)

If you want to use a specific resource group for your Kibana deployment, do the following changes to the terraform script.

```bash
echo "variable "resource_group" {}" >> /path/to/variables.tf
```

Copy the below main.tf file

```terraform
terraform {
  required_providers {
    ibm = {
      source  = "IBM-Cloud/ibm"
      version = ">= 1.58.1"
    }
  }
}

provider "ibm" {
  ibmcloud_api_key = var.ibmcloud_api_key
  region           = var.region
}
```

Modify the codeengine.tf file to read the resource_group_id value and use it. The rest of the script can remain as is

```
data "ibm_resource_group" "rg" {
  name = var.resource_group
}

resource "ibm_code_engine_project" "kibana_code_engine" {
  name              = "kibana-code-engine-project2"
  resource_group_id = data.ibm_resource_group.rg.id

}
```

Add the `resource_group` key-value pair in the terraform.tfvars file

Then `terraform plan` and `terraform apply` as described

## Add users to Kibana

### Optional: Create virtual environment

```bash
python3 -m venv ansible-env
source ansible-env/bin/activate  # On Windows: ansible-env\Scripts\activate
pip install ansible
```
