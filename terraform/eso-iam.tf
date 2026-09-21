resource "aws_iam_policy" "external_secrets" {
  name        = "external-secrets-policy"
  description = "Allow external secret operator to read backend secret"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
        ]
        Resource = ["arn:aws:secretsmanager:ap-south-1:370613533967:secret:eks/backend/db-*","arn:aws:secretsmanager:ap-south-1:370613533967:secret:eks/backend/api-*"]
      }
    ]
  })

}

data "aws_iam_policy_document" "external_secrets_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type = "Federated"
      identifiers = [
        "arn:aws:iam::370613533967:oidc-provider/oidc.eks.ap-south-1.amazonaws.com/id/DCA588B5FC3370DE27BF8C276AE8F980"
      ]
    }

    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      variable = "oidc.eks.ap-south-1.amazonaws.com/id/DCA588B5FC3370DE27BF8C276AE8F980:sub"
      values   = ["system:serviceaccount:external-secrets:external-secrets"]
    }

    condition {
      test     = "StringEquals"
      variable = "oidc.eks.ap-south-1.amazonaws.com/id/DCA588B5FC3370DE27BF8C276AE8F980:aud"
      values   = ["sts.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "external_secrets" {
  name               = "external-secrets-role"
  assume_role_policy = data.aws_iam_policy_document.external_secrets_assume_role.json
}

resource "aws_iam_role_policy_attachment" "external_secrets_policy_attachment" {
  role       = aws_iam_role.external_secrets.name
  policy_arn = aws_iam_policy.external_secrets.arn
}