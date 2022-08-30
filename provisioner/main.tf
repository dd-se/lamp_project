# Use this key_pair
resource "aws_key_pair" "server_auth" {
  key_name   = "dd_key"
  public_key = file(var.ssh_public_key)

}

# ec2 instance and attaching it to my subnet

resource "aws_instance" "server_node" {
  count                  = var.host_count
  instance_type          = var.aws_region == "eu-west-1" ? "t2.micro" : "t3.micro"
  ami                    = data.aws_ami.server_ami.id
  key_name               = aws_key_pair.server_auth.id
  vpc_security_group_ids = [aws_security_group.allow_default.id]
  subnet_id              = aws_subnet.server_subnet.id

  root_block_device {
    volume_size = 8
  }

  tags = {
    Name = "gc_node"
  }

}
