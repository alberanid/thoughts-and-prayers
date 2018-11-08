FROM debian:stable-slim
LABEL \
	maintainer="Davide Alberani <da@mimante.net>"

RUN \
	apt-get update && \
	apt-get -y --no-install-recommends install \
		polygen && \
	rm -rf /var/lib/apt/lists/*

COPY tap.grm cry-a-lot /
RUN chmod +x /cry-a-lot

CMD [ "/cry-a-lot" ]
