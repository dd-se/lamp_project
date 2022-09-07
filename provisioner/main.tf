# Use this key pair
resource "aws_key_pair" "server_auth" {
  key_name   = "dd_key"
  public_key = file(var.ssh_public_key)

}

# create ec2 instances and attach it to the subnet
resource "aws_instance" "load_balancer" {
  instance_type          = var.aws_region == "eu-west-1" ? "t2.micro" : "t3.micro"
  ami                    = data.aws_ami.server_ami.id
  key_name               = aws_key_pair.server_auth.id
  vpc_security_group_ids = [aws_security_group.allow_default.id]
  subnet_id              = aws_subnet.server_subnet.id
  root_block_device {
    volume_size = 8
  }
  tags = {
    Name = "gc_loadbalancer"
  }
}
resource "aws_instance" "database" {
  instance_type          = var.aws_region == "eu-west-1" ? "t2.micro" : "t3.micro"
  ami                    = data.aws_ami.server_ami.id
  key_name               = aws_key_pair.server_auth.id
  vpc_security_group_ids = [aws_security_group.allow_default.id]
  subnet_id              = aws_subnet.server_subnet.id

  root_block_device {
    volume_size = 8
  }
  tags = {
    Name = "gc_database"
  }
}

resource "aws_instance" "doctor" {
  instance_type          = var.aws_region == "eu-west-1" ? "t2.micro" : "t3.micro"
  ami                    = data.aws_ami.server_ami.id
  key_name               = aws_key_pair.server_auth.id
  vpc_security_group_ids = [aws_security_group.allow_default.id]
  subnet_id              = aws_subnet.server_subnet.id

  root_block_device {
    volume_size = 8
  }
  tags = {
    Name = "gc_doctor"
  }
}
resource "aws_instance" "backends" {
  count                  = var.backend_host_count
  instance_type          = var.aws_region == "eu-west-1" ? "t2.micro" : "t3.micro"
  ami                    = data.aws_ami.server_ami.id
  key_name               = aws_key_pair.server_auth.id
  vpc_security_group_ids = [aws_security_group.allow_default.id]
  subnet_id              = aws_subnet.server_subnet.id

  root_block_device {
    volume_size = 8
  }
  tags = {
    Name = "gc_backend_${count.index}"
  }

}
