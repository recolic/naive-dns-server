CC ?= gcc
CYTHON ?= cython

.PHONY: server.c tool_encrypt_cfg.c

all: server.c tool_encrypt_cfg.c
	eval $(CC) server.c tool_encrypt_cfg.c -o server `python3-config --cflags --ldflags`

tool_encrypt_cfg.c:
	$(CYTHON) -3 tool_encrypt_cfg.py

server.c:
	$(CYTHON) -3 --embed server.py

clean:
	rm -f server.c tool_encrypt_cfg.c server

