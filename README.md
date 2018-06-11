# kubesdb
A tool to create databases inside an existing MySQL, like for example

* AWS RDS Aurora
* helm install stable/mysql
* Any other MySQL

This is published as a Docker image [polarn/kubesdb](https://hub.docker.com/r/polarn/kubesdb/).

## Why?
Well, our problem was that we decided to have one RDS Aurora cluster on a private subnet and share it between all our micro services, by creating MySQL databases for each service inside it. We wanted to do this in an "infrastructure as code" way but it proved a bit difficult using SSH tunnels to a bastion host, etc...

So the idea is to use a Kubernetes pod to create the databases by listening on (watching) the Kubernetes API for secrets that match a certain label. Once a secret is created, a database and username/grant will be created.

We can now create the RDS, Kubernetes secrets, etc using Terraform. We're happy!

## Usage

### Create RDS cluster
Create the RDS cluster using your favourite tool (we use [Terraform](https://www.terraform.io/)) or using the UI.

### RDS Endoint, Username and password as Kubernetes Secret
We add them using the terraform kubernetes plugin

### Kubernetes Secret
We put the following in our Secrets:

* `database` : Database name
* `username` : The username of the grant to be created
* `password` : And the password to that grant
* `url` : The JDBC URL (this is not needed for kubesdb but our micro service use it to connect to the database)

Examples:

[kubernetes/secret.yaml](kubernetes/secret.yaml)

or using `kubectl`:

```
kubectl create secret generic kubesdb-secret --from-literal=database=test --from-literal=username=testuser --from-literal=password=$(openssl rand -hex 8) --from-literal=url=jdbc:mysql://examplerds.randomstring.region.rds.amazonaws.com:3306/test?useSSL=false
kubectl label secret kubesdb-secret kubesdb=true
```

### Kubernetes deployment
In the repo there is an example file of how we use it: [kubernetes/deployment.yaml](kubernetes/deployment.yaml)

test2
