CC       = gcc
CXX      = g++
CFLAGS   = -g
CXXFLAGS = $(CFLAGS)

#LIBPATH = /home/levy/apps/CH_HCNetSDK9/lib
#-Wl,-rpath=/home/levy/apps/CH_HCNetSDK9/lib:/home/levy/apps/CH_HCNetSDK9/lib/HCNetSDKCom 
#LIBS =  -lhcnetsdk
SRC = ./dxf.cpp
TARGET = ./dxf_test

all: 
	$(CXX) $(OPTI) $(CXXFLAGS) $(SRC) -o $(TARGET) 

.PHONY: clean
clean:
	rm -f $(TARGET)

