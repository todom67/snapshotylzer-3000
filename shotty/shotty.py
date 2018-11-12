import boto3
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def filter_instances(project):
    instances = []

    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """Shotty manages snapshots"""

@cli.group('instances')
def instances():
    """Commands for instances"""

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@instances.command('list')
@click.option('--project', default=None,
    help = 'Only instances for project (tag Project:<name>)')
def list_instances(project):
    "List EC2 instances"
    instances = filter_instances(project)
    
    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        print(', '.join((
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project','<no project>'))))
    
    return  

@instances.command('stop')
@click.option('--project', default=None,
    help = 'Only instances for project (tag Project:<name>)')
def stop_instances(project):
    "Stop EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Stopping %s" % i.id)
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,
    help = 'Only instances for project (tag Project:<name>)')
def start_instances(project):
    "Start EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        print("Starting %s" % i.id)
        i.start()

    return

@instances.command('snapshot',
    help="Create snapshots fo all volumes")
@click.option('--project', default=None,
    help = 'Only instances for project (tag Project:<name>)')
def create_snapshots(project):
    "Create snapshots for EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print("Creating snapshot of %s" % v.id)
            v.create_snapshot(Description="Create by SnapshotAlyser 3000")

    return

@volumes.command('list')
@click.option('--project', default=None,
    help = 'Only volumes for project (tag Project:<name>)')
def list_volumes(project):
    "List EC2 volumes"
    instances = filter_instances(project)
    
    for i in instances:
       for v in i.volumes.all():
           print(", ".join((
               v.id,
               i.id,
               v.state,
               str(v.size) + "GiB",
               v.encrypted and "Encrypted" or "Not Encrypted"
           )))
    
    return  

@snapshots.command('list')
@click.option('--project', default=None,
    help = 'Only snapshots for project (tag Project:<name>)')
def list_snapshots(project):
    "List EC2 snapshots"
    instances = filter_instances(project)
    
    for i in instances:
       for v in i.volumes.all():
           for s in v.snapshots.all():
                print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                )))
        
    return  


if __name__ == '__main__':
    cli()
    