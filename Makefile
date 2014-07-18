all: clean test

clean: 
	vagrant destroy --force

.PHONY: test
test: 
	vagrant up && \
	vagrant ssh --command \
	  "temp=$(mktemp --directory) && \
	   rsync -r /vagrant/* $temp --exclude='.*' && \
	   cd $temp && nosetests"
