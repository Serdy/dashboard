import boto3
from collections import defaultdict
ec2 = boto3.resource('ec2')



def aws_instanses_filter(*args):

	filters = [
		{
			'Name':'tag:Name', 
			'Values':['eCommerce*']
			}
			]
	if args:
		filters = [
		{
			'Name':'tag:Name', 
			'Values':['eCommerce*'+ args[0] +'*']
			}
			]
		
	instances = ec2.instances.filter(Filters=filters)
	
	ec2info = []
	for instance in instances:
		for tag in instance.tags:
			if 'Name' == tag['Key']:
				instanse_name = tag['Value']
				
		# Add instance info to a dictionary         
		info = {
			'Name': instanse_name,
			'Type': instance.instance_type,
			'State': instance.state['Name'],
			'Private_IP': instance.private_ip_address,
			'Public_IP': instance.public_ip_address,
			'ID': instance.id,
			}
		# print(info)
		ec2info.append(dict(info))
	return ec2info
