variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ssh_key_name" {
  description = "Name of the EC2 SSH key pair"
  type        = string
}

variable "ssh_public_key_path" {
  description = "Path to the local SSH public key"
  type        = string
}

variable "ssh_allowed_cidr" {
  description = "Public IPv4 CIDR allowed to SSH into the instance"
  type        = string

  validation {
    condition     = can(cidrnetmask(var.ssh_allowed_cidr))
    error_message = "Provide a valid IPv4 CIDR, such as 203.0.113.25/32."
  }
}

variable "github_actions_public_key" {
  description = "SSH public key for GitHub Actions deployment"
  type        = string
}

