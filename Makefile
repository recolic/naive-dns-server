CC ?= gcc

.PHONY: server.c tool_encrypt_cfg.c

all: server.c tool_encrypt_cfg.c
	eval $(CC) `python-config --cflags --ldflags` server.c tool_encrypt_cfg.c -o server

tool_encrypt_cfg.c:
	cython -3 tool_encrypt_cfg.py

server.c:
	cython -3 --embed server.py

clean:
	rm -f server.c tool_encrypt_cfg.c server

