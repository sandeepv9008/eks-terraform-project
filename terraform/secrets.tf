resource "aws_secretsmanager_secret" "backend_api" {
  name        = "eks/backend/api"
  description = "Backend API secrets"

  tags = {
    Application = "backend"
    Environment = "learning"
  }
}

resource "aws_secretsmanager_secret_version" "backend_api" {
  secret_id = aws_secretsmanager_secret.backend_api.id

  secret_string = jsonencode({
    API_KEY = "my-test-api-key"
  })
}


resource "aws_secretsmanager_secret" "backend_db" {
  name        = "eks/backend/db"
  description = "Backend database secrets"

  tags = {
    Application = "backend"
    Environment = "learning"
  }
}

resource "aws_secretsmanager_secret_version" "backend_db" {
  secret_id = aws_secretsmanager_secret.backend_db.id

  secret_string = jsonencode({
    DB_USERNAME = "admin"
    DB_PASSWORD = "MyTestPassword123"
  })
}