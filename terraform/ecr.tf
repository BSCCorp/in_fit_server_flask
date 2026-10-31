resource "aws_ecr_repository" "flask_api" {
  name                 = "flask-infit-api"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name      = "flask-infit-api"
    ManagedBy = "Terraform"
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.flask_api.repository_url
}

