output "instance_id" {
  description = "ID of the Flask API EC2 instance"
  value       = aws_instance.flask_api.id
}

output "public_ip" {
  description = "Public IPv4 address of the Flask API server"
  value       = aws_instance.flask_api.public_ip
}

output "ssh_command" {
  description = "Command to connect to the instance"
  value       = "ssh -o IdentitiesOnly=yes -i ~/.ssh/flask-terraform ubuntu@${aws_instance.flask_api.public_ip}"
}

