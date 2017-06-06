.PHONY: docs

index = ./index.html

serve: $(index)
	((sleep 2 && sensible-browser http://localhost:25000) &) && \
		python3 -m http.server 25000
