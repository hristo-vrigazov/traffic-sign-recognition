import click

@click.command()
@click.option(
	'--image', 
	prompt='Path to the image:',
	help='The path to the image')
@click.option(
	'--model',
	prompt='Path to the serialized neural network pickle',
	help='The path to the model')
def recognize_traffic_sign(image, model):
	pass