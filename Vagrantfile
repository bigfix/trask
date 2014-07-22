# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "trask-dev"

  config.vm.provider "virtualbox" do |v, override|
    v.gui = false
    v.customize ["modifyvm", :id, "--memory", 512]
    v.customize ["modifyvm", :id, "--cpus", 1]

  $script = <<SCRIPT
touch /home/vagrant/.bash_aliases && \
echo "alias python=python3" > /home/vagrant/.bash_aliases

sudo apt-get update && sudo apt-get install --yes python3-pip

sudo pip3 install nose
SCRIPT

  config.vm.provision "shell", inline: $script
  end
end
