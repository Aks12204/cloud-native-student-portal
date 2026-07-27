variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project resource name prefix"
  type        = string
  default     = "student-portal"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}