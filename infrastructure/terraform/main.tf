# OpsPilot AI - Terraform Infrastructure as Code
# Author: Nivesh Kumar Meena
# Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.

terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project   = "OpsPilot-AI"
      Author    = "Nivesh Kumar Meena"
      ManagedBy = "Terraform"
    }
  }
}

# VPC Configuration
resource "aws_vpc" "opspilot_vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "opspilot-vpc"
  }
}

# EKS Cluster
resource "aws_eks_cluster" "opspilot_cluster" {
  name     = var.cluster_name
  role_arn = aws_iam_role.eks_role.arn
  version  = "1.29"

  vpc_config {
    subnet_ids = [aws_subnet.subnet_a.id, aws_subnet.subnet_b.id]
  }

  depends_on = [aws_iam_role_policy_attachment.eks_policy]
}

# PostgreSQL RDS Instance with pgvector support
resource "aws_db_instance" "opspilot_rds" {
  identifier          = "opspilot-db-prod"
  engine              = "postgres"
  engine_version      = "16.1"
  instance_class      = "db.t4g.medium"
  allocated_storage   = 50
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true

  tags = {
    Name = "opspilot-postgres-pgvector"
  }
}

resource "aws_subnet" "subnet_a" {
  vpc_id            = aws_vpc.opspilot_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "${var.aws_region}a"
}

resource "aws_subnet" "subnet_b" {
  vpc_id            = aws_vpc.opspilot_vpc.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "${var.aws_region}b"
}

resource "aws_iam_role" "eks_role" {
  name = "opspilot-eks-cluster-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "eks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_policy" {
  role       = aws_iam_role.eks_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}
