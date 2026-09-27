# OpsPilot AI - Terraform Variables & Outputs
# Author: Nivesh Kumar Meena
# Copyright (c) 2026 Nivesh Kumar Meena. All Rights Reserved.

variable "aws_region" {
  description = "AWS deployment region"
  type        = string
  default     = "us-west-2"
}

variable "cluster_name" {
  description = "EKS Cluster Name"
  type        = string
  default     = "opspilot-ai-cluster"
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "db_username" {
  description = "PostgreSQL Administrator Username"
  type        = string
  default     = "opspilot_admin"
}

variable "db_password" {
  description = "PostgreSQL Administrator Password"
  type        = string
  sensitive   = true
  default     = "OpsPilotPass2026!Secure"
}
