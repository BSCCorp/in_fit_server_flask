# Find the account's default VPC.
data "aws_vpc" "default" {
  default = true
}

# Find subnets belonging to that VPC.
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Find the latest official Ubuntu 24.04 LTS AMD64 image.
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Register our SSH public key with AWS.
resource "aws_key_pair" "flask_api" {
  key_name   = var.ssh_key_name
  public_key = file(pathexpand(var.ssh_public_key_path))
}

# Define which inbound connections are allowed.
resource "aws_security_group" "flask_api" {
  name        = "flask-api-terraform"
  description = "Network access for the Flask API demo"
  vpc_id      = data.aws_vpc.default.id

  # SSH from your specified IP address only.
  ingress {
    description = "SSH administration"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_allowed_cidr]
  }

  # HTTP for Nginx and initial testing.
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS for the eventual public API.
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow outbound traffic for updates and image pulls.
  egress {
    description = "Outbound IPv4 traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "flask-api-terraform"
  }
}

# Create the Ubuntu server.
resource "aws_instance" "flask_api" {
  user_data_replace_on_change = true

  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnets.default.ids[0]
  associate_public_ip_address = true

  vpc_security_group_ids = [
    aws_security_group.flask_api.id
  ]

  key_name = aws_key_pair.flask_api.key_name

  root_block_device {
    volume_size = 8
    volume_type = "gp3"
    encrypted   = true
  }

  user_data = file("${path.module}/scripts/setup-host.sh")

  tags = {
    Name = "flask-api-demo"
  }
}

# GitHub Actions key
resource "aws_key_pair" "github_actions" {
  key_name   = "flask-api-github-actions"
  public_key = var.github_actions_public_key

  tags = {
    Name      = "flask-api-github-actions"
    ManagedBy = "Terraform"
  }
}

