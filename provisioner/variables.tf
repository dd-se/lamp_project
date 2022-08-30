variable "aws_region" {
  type        = string
  description = "Choose a AWS Region."
}
variable "ec2_instance_name" {
  type        = string
  description = "Supply a EC2 Instance Name"
  default     = "Server"
}

variable "ingress_ports" {
  type        = map(any)
  description = "Allow Rules"
}

variable "ssh_public_key" {
  type        = string
  description = "Path to ssh public key"
}

variable "host_count" {
  type        = number
  description = "host count"
}
