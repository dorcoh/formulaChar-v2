init:
	pip install -r requirements.txt

test:
	nosetests tests --nologcapture

testshow:
	nosetests tests --nologcapture -s
