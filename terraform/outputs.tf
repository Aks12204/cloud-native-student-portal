output "s3_website_url" {
  description = "URL for the S3 Static Website Hosting"
  value       = aws_s3_bucket_website_configuration.frontend.website_endpoint
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket hosting static website"
  value       = aws_s3_bucket.frontend.id
}

output "api_gateway_endpoint" {
  description = "Public URL endpoint for the Amazon API Gateway"
  value       = aws_apigatewayv2_api.http_api.api_endpoint
}

output "alb_dns_name" {
  description = "DNS Name of the Application Load Balancer (ALB)"
  value       = aws_lb.alb.dns_name
}

output "vpc_id" {
  description = "Custom Amazon VPC ID"
  value       = aws_vpc.main.id
}

output "dynamodb_table_name" {
  description = "Amazon DynamoDB Table Name"
  value       = aws_dynamodb_table.student_data.name
}