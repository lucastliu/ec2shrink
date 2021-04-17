# ec2shrink
An easier way to reduce the storage size for EC2


## Prerequisites 

Login to [AWS CloudShell](https://aws.amazon.com/cloudshell/) with Administrator Priviledges

Find the CloudShell ip and add it to your security group for the relevant EC2 instances

Use this command inside Cloud Shell to determine its IP:
```
curl http://checkip.amazonaws.com

```

This ip is not static unfortunately, and so you may need to update the security rules from time to time if you find you cannot reach your EC2 instances.

## Install Package

Install ec2shrink
```
pip3 install ec2shrink

```

## Usage

```
ec2shrink shrink --id <your-ec2-instance-id> --size <desired-new-size-in-GiB>
```



