if [[ -n "$VIRTUAL_ENV" ]]; then
	python build_dist.py
	./make_multiple.sh
	python build_readme.py
else
	source ./myenv/bin/activate
	python build_dist.py
	./make_multiple.sh
	python build_readme.py
fi


