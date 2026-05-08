output "rds_endpoint" {
  description = "RDS endpoint"
  value       = "postgresql://${aws_db_instance.postgres.endpoint}"
}

output "redis_endpoint" {
  description = "Redis endpoint"
  value       = aws_elasticache_cluster.redis.cache_nodes[0].address
}

output "alb_dns_name" {
  description = "ALB DNS name"
  value       = "aws_lb.main.dns_name"
}

output "cloudfront_domain_name" {
  description = "CloudFront domain name"
  value       = "aws_cloudfront_distribution.main.domain_name"
}
