output "loadbalancer" {
  value = aws_instance.load_balancer.public_ip
}
output "database" {
  value = aws_instance.database.public_ip
}
output "doctor" {
  value = aws_instance.doctor.public_ip
}
output "backends" {
  value = aws_instance.backends[*].public_ip
}
