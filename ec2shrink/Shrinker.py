import click
import os
import subprocess
import json
import time
import pexpect

#command line run

#TODO: need to spec AZ during instance creation

@click.group()
@click.version_option("1.0.0")
def main():
    """Shrink EC2 instance on AWS"""
    pass


@main.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

@main.command()
def viewinstances():
    """View EC2 instance IDs and AZs"""
    output = subprocess.check_output(['awscliv2', 'ec2', 'describe-instances',
                                      '--query', 'Reservations[0].Instances[*].{Instance:InstanceId,AZ:Placement.AvailabilityZone}'])
    d = json.loads(output)
    print(d)

@main.command()
@click.pass_context
@click.option("--id", default="i-3", required=True, help="EC2 instance ID")
@click.option("--size", default=9, required=True, help="desired size to change to")
def shrink(ctx, id, size):
    """Resize EC2 instance"""
    ctx.invoke(stop, id=id)

    instanceB = ctx.invoke(make, size=size)
    instanceC = ctx.invoke(make)

    volA = ctx.invoke(getvolume, id=id)
    volB = ctx.invoke(getvolume, id=instanceB)

    ctx.invoke(stop, id=instanceB)

    ctx.invoke(detach, volid=volA)
    ctx.invoke(detach, volid=volB)

    ctx.invoke(attach, volid=volA, instanceid=instanceC, device='/dev/xvdf')
    ctx.invoke(attach, volid=volB, instanceid=instanceC, device='/dev/xvdg')

    ctx.invoke(copy, id=instanceC)

    ctx.invoke(detach, volid=volA)
    ctx.invoke(detach, volid=volB)

    ctx.invoke(attach, volid=volB, instanceid=id, device='/dev/xvda')

    output = subprocess.check_output(['awscliv2', 'ec2', 'start-instances',
                                      '--instance-ids', id])
    d = json.loads(output)
    print(d)
    ctx.invoke(status, id=id, stat="running")






@main.command()
@click.pass_context
@click.option("--id", default="i-3", required=True, help="EC2 instance ID")
def stop(ctx, id):
    """stop instance"""
    output = subprocess.check_output(['awscliv2', 'ec2', 'stop-instances', '--instance-ids', id])
    d = json.loads(output)
    print(d)
    ctx.invoke(status, id=id, stat='stopped')


@main.command()
@click.option("--volid", default="vol-3", help="vol id to check status for")
@click.option("--stat", default="attached", help="desired status")
@click.option("--detach", is_flag=True, default=False, help="If true checks for detached instead of attached")
def volstatus(volid, stat, detach):
    """instance status"""
    while(True):
        output2 = subprocess.check_output(['awscliv2', 'ec2', 'describe-volumes', '--volume-ids', volid])
        r = json.loads(output2)

        if detach:
            istatus = r['Volumes'][0]['State']
        else:
            istatus = r['Volumes'][0]['Attachments'][0]['State']

        print(istatus)
        if (istatus == stat):
            break
        else:
            print(istatus)
            time.sleep(3)

@main.command()
@click.option("--id", default="i-3", help="ec2 instance id to check status for")
@click.option("--stat", default="running", help="desired status")
def status(id, stat):
    """instance status"""
    while(True):
        output2 = subprocess.check_output(['awscliv2', 'ec2', 'describe-instances', '--instance-id', id])
        r = json.loads(output2)
        istatus = r['Reservations'][0]['Instances'][0]['State']['Name']
        print(istatus)
        if (istatus == stat):
            break
        else:
            print(istatus)
            time.sleep(3)


@main.command()
@click.pass_context
@click.option("--volid", default="vol-3", help="volume id")
def detach(ctx, volid):
    """detach volume"""
    output = subprocess.check_output(['awscliv2', 'ec2', 'detach-volume',
                                      '--volume-id', volid])
    d = json.loads(output)
    print(d)
    ctx.invoke(volstatus, volid=volid, stat="available", detach=True)

@main.command()
@click.pass_context
@click.option("--volid", default="vol-3", help="volume id")
@click.option("--instanceid", default="i-3", help="volume id")
@click.option("--device", default="/dev/xvda", help="device name")
def attach(ctx, volid, instanceid, device):
    """attach volumes"""
    output = subprocess.check_output(['awscliv2', 'ec2', 'attach-volume',
                                      '--volume-id', volid,
                                      '--instance-id', instanceid,
                                      '--device', device])
    d = json.loads(output)
    print(d)
    ctx.invoke(volstatus, volid=volid)

@main.command()
@click.pass_context
@click.option("--id", default="i-3", help="ec2 instance id")
def getvolume(ctx, id):
    """get volume id of ec2 instance"""
    output = subprocess.check_output(['awscliv2', 'ec2', 'describe-instances',
                                      '--instance-ids', id,
                                      '--query',
                                      'Reservations[0].Instances[0].BlockDeviceMappings[0].Ebs.VolumeId'])
    d = json.loads(output)
    print(d)
    return d

@main.command()
@click.pass_context
@click.option("--size", default=10, help="ec2 storage size in GiB")
@click.option("--instancetype", default="t2.micro", help="desired status")
def make(ctx, size, instancetype):
    """make ec2 instance"""
    output = subprocess.check_output(['awscliv2', 'ec2', 'run-instances',
                                      '--image-id', 'ami-0742b4e673072066f',
                                      '--instance-type', instancetype,
                                      '--placement',
                                      'AvailabilityZone=us-east-1d', # need this to be consistent
                                      '--block-device-mappings',
                                      'DeviceName=/dev/xvda,Ebs={VolumeSize=' + str(size) + '}'])
    d = json.loads(output)
    print(d)
    idarg = d['Instances'][0]['InstanceId']
    print(idarg)
    ctx.invoke(status, id=idarg, stat="running")
    return idarg

#TODO: security group rules need to be expansive to allow mssh need to figure out policy
#TODO: run past the yes prompt, but only one time?
#get subprocess.run outputs
@main.command()
@click.pass_context
@click.option("--id", default="i-3", help="hosting ec2 instance id to use for copy")
def copy(ctx, id):
    """copy volumes"""

    child = pexpect.spawn('mssh ' + id)
    time.sleep(3)
    index = child.expect(['Are you sure you want to continue connecting',
                        'Amazon Linux 2 AMI', pexpect.EOF, pexpect.TIMEOUT])
    print(index)
    if index == 0:
        print('confirm')
        child.sendline('yes')
    elif index == 1:
        print('no confirm')
    elif index == 2:
        print("EOF")
    elif index == 3:
        print("TIMEOUT")

    child.expect("ec2")
    child.sendline("sudo mkdir /source /target")
    child.expect("ec2")
    child.sendline("sudo mount -t xfs -o nouuid /dev/xvdf1 /source")
    child.expect("ec2")
    child.sendline("sudo mount -t xfs -o nouuid /dev/xvdg1 /target")
    child.expect("ec2")
    print("syncing")
    child.sendline("sudo rsync -axSHAX /source/ /target")
    child.expect("ec2", timeout=None)
    child.sendline("sudo umount /target")
    child.expect("ec2")
    child.sendline("sudo umount /source")
    child.expect("ec2")
    time.sleep(2)
    child.sendline("exit")
    print("done with copy")

    # sshProcess.stdin.write("sudo mkdir /source /target \n")
    # sshProcess.stdin.write("sudo mount -t xfs -o nouuid /dev/xvdf1 /source \n")
    # sshProcess.stdin.write("sudo mount -t xfs -o nouuid /dev/xvdg1 /target \n")
    # sshProcess.stdin.write("sudo rsync -vaxSHAX /source/ /target \n")
    # sshProcess.stdin.write("sudo umount /target \n")
    # sshProcess.stdin.write("sudo umount /source \n")
    # sshProcess.stdin.write("exit \n")
    # sshProcess.stdin.close()
  # TODO: figure out if this actually runs or not - the mount stuff definitely does (maybe use fabric or something)
  # TODO: terminate things afterwards
  # TODO: put an actual file in and see if it really transfers
  # maybe just make the user run the rsync themselves?


if __name__ == '__main__':
    main()
