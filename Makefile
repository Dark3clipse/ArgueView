argueview.egg-info build/:argueview
	docker build . -t argueview:local
	docker run --cidfile ./.cid -v /var/run/docker.sock:/var/run/docker.sock argueview:local /bin/bash /argueview/build.sh
	docker cp $(cat ./.cid):/argueview/argueview.egg-info ./argueview.egg-info
	rm .cid
