# Sprint 1: Monitoring Website Health

The project is build using AWS CDK with other functionalities to publish cloudwatch metrics for checking latency and availability of four urls and sending SNS notifications to subscribers once, the alarm is triggered.


## Authors

- [@sameer2021skipq](https://www.github.com/https://github.com/sameer2021skipq)




## Getting Started

The instructions and details regarding deployment using AWS CDK  are given below

To manually create a virtualenv on MacOS and Linux:

```bash
  cd project-folder
  python -m venv .venv
```
Creates a new CDK project in the current directory from a specified template

```bash
  cdk init
```

After the init process completes and the virtualenv is created, you can use the following step to activate your virtualenv.

```bash
  python -m venv .venv
```
Activate your virtualenv.

```bash
  source .venv/bin/activate
```
Install all the required python packages 

```bash
  pip3 install -r requirements.txt
```
You can now synthesize the CloudFormation template for this code

```bash
  cdk synth
```

You can now deploy the CloudFormation template for this code

```bash
  cdk deploy
```
