# OpsPilot AI - Terraform Outputs
# Author: Nivesh Kumar Meena
# Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.

output "eks_cluster_name" {
  description = "Deployed EKS Cluster Name"
  value       = aws_eks_cluster.opspilot_cluster.name
}

output "eks_cluster_endpoint" {
  description = "EKS Cluster Control Plane Endpoint"
  value       = aws_eks_cluster.opspilot_cluster.endpoint
}

output "rds_endpoint" {
  description = "PostgreSQL pgvector RDS Endpoint"
  value       = aws_db_instance.opspilot_rds.endpoint
}

output "project_author" {
  description = "Author and Owner"
  value       = "Nivesh Kumar Meena"
}
