variable "aws_region" {
  type        = string
  description = "Choose a AWS Region."
}
variable "ssh_public_key" {
  type        = string
  description = "Path to ssh public key"
}
variable "ingress_ports" {
  type        = map(any)
  description = "Specify allow rules"
}
variable "backend_host_count" {
  type        = number
  description = "Specify backend host count"
}
