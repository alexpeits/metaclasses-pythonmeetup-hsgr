.PHONY: docs

index = ./notes.html

serve: $(index)
	cp notes.html docs/index.html && \
		cd docs && \
		((sleep 2 && sensible-browser http://localhost:25000) &) && \
		python3 -m http.server 25000
