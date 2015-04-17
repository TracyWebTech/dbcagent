# -*- mode: ruby -*-
# vi: set ft=ruby :

require 'yaml'

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = ENV.fetch("VAGRANT_BOX", 'trusty64')
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

  ips = YAML.load_file('config/development/ips.yaml')

  config.vm.define 'replica1' do |replica1|
    replica1.vm.hostname = 'vagrant-replica1'
    replica1.vm.network 'private_network', ip: ips['replica1']

	replica1.vm.provision "shell", path:"config/development/environment.sh" , args: "10.10.10.3"
	replica1.vm.provision "shell", path:"config/development/config_master.sh" , args: ["dbexample", "replicator", "123456"]
    replica1.vm.provider "virtualbox" do |v|
      v.memory = 512
    end
  end

  config.vm.define 'replica2' do |replica2|
    replica2.vm.hostname = 'vagrant-replica2'
    replica2.vm.network 'private_network', ip: ips['replica2']
	replica2.vm.provision "shell", path:"config/development/environment.sh" , args: [ips['replica2']]
	replica2.vm.provision "shell", path:"config/development/config_master.sh" , args: ["dbexample", "replicator", "123456"]
    replica2.vm.provider "virtualbox" do |v|
      v.memory = 512
    end
  end

  config.vm.define 'replica3' do |replica3|
    replica3.vm.hostname = 'vagrant-replica3'
    replica3.vm.network 'private_network', ip: ips['replica3']
	replica3.vm.provision "shell", path:"config/development/environment.sh" , args: [ips['replica3']]
	replica3.vm.provision "shell", path:"config/development/config_master.sh" , args: ["dbexample", "replicator", "123456"]
    replica3.vm.provider "virtualbox" do |v|
      v.memory = 512
    end
  end

end

