# ec2shrink
An easier way to reduce the storage size for EC2


## AWS CloudShell
Login to [AWS CloudShell](https://aws.amazon.com/cloudshell/) with Administrator Priviledges

Find the CloudShell ip and add it to your security group for the relevant EC2 instances

Use this command inside Cloud Shell to determine its IP:
```
curl http://checkip.amazonaws.com

```

This ip is not static unfortunately, and so you may need to update the security rules from time to time if you find you cannot reach your EC2 instances.

### Install Package


```
sudo pip3 install ec2shrink==1.0.0

```

## Other Linux devices

You will need to [configure credentials for the awscli](https://github.com/aws/aws-cli) before using ec2shrink

### Install Package


```
pip3 install ec2shrink==1.1.0

```

## Usage


Shrink an EC2 Instance Running Amazon Linux:
```
ec2shrink shrink --id <your-ec2-instance-id> --size <desired-new-size-in-GiB>
```

To see full list of functions:
```
ec2shrink --help
```

## Notes

Make sure to be aware of what region and availablity zone is currently set for AWS in the browser, the EC2 instance, and locally on AWSCLI

ec2shrink is currently configured to run on EC2 instances running Amazon Linux. It has been tested with the base t2.micro free tier eligible configuration.

Always be sure to backup any critical data before running ec2shrink.