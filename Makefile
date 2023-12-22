dev:
	@bots/dev.sh

release:
	@bots/builder.sh

run:
	@bots/runner.sh

build-spec:
	@bots/spec-builder.sh