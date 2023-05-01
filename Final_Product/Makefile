# Makefile for the email client project

# Compiler
CC = python3

# Directories
SRC_DIR = src
BIN_DIR = bin

# Files
CLIENT_GUI = $(SRC_DIR)/Client_GUI.py
GMAIL_API = $(SRC_DIR)/GMail_API.py
GMAIL_GUI = $(SRC_DIR)/GMail_GUI.py
HOST_GUI = $(SRC_DIR)/Host_GUI.py
MAIN_LOGIN = $(SRC_DIR)/Main_Login.py
WELCOME_PAGE = $(SRC_DIR)/Welcome_Page.py

# Targets
all: $(BIN_DIR)/client

$(BIN_DIR)/client: $(CLIENT_GUI) $(GMAIL_API) $(GMAIL_GUI) $(HOST_GUI) $(MAIN_LOGIN) $(WELCOME_PAGE)
	$(CC) -o $@ $^

clean:
	rm -f $(BIN_DIR)/client

.PHONY: all clean
