output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.flask_api.id
}

output "public_ip" {
  description = "Static Elastic IP address"
  value       = aws_eip.flask_api.public_ip
}

output "ssh_command" {
  description = "SSH command for connecting to the instance"
  value       = "ssh -o IdentitiesOnly=yes -i ~/.ssh/flask-terraform ubuntu@${aws_eip.flask_api.public_ip}"
}

output "security_group_id" {
  description = "EC2 security group ID"
  value       = aws_security_group.flask_api.id
}

output "instance_profile_name" {
  description = "EC2 IAM instance profile"
  value       = aws_iam_instance_profile.flask_api.name
}

