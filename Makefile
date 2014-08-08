all: clean test

clean: 
	vagrant destroy --force

.PHONY: test
test: 
	vagrant up && \
	vagrant ssh --command \
	  'temp=$$(mktemp --directory) && \
	   rsync --recursive /vagrant/* --exclude=".*" $$temp && \
	   cd $$temp && \
	   nosetests --verbose'
