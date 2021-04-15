# ec2shrink
An easier way to reduce the storage size for EC2

Soon to be a PyPI package!

## AWS Pre-Req

login to AWS cloud shell with Administrator Priviledges 

Find the cloud shell ip and add it to your security group for the relevant EC2 instances

Use this command to determine IP:
```
curl http://checkip.amazonaws.com

```
#### Install Dependencies
```
pip3 install pexpect awscli click
```

In your cloud shell, upload the Shrinker.py file

## Usage

```
python3 Shrinker.py shrink --id <your-ec2-instance-id> --size <desired-new-size-in-GiB>
```



