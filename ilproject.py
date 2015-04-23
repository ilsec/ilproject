# -*- coding: utf-8 -*-
import sys, os, json, zipfile, shutil

Makevars = '''
# 全局配置选项
PLATFORM := $(shell uname | sed -e 's/_.*//')

# tools
ifndef COPY
COPY=cp
endif

ifndef RM
RM=rm
endif

ifndef MAKE
MAKE=make
endif

ifndef CXX
CXX = g++
AR = ar
endif

# 编译选项
ifndef CXXFLAGS
CXXFLAGS = -fpermissive
endif

# 全局OBJECTS
global_OBJECTS = 

# 全局SOURCES
global_SOURCES = 

# set custom
ifeq ($(dll),)
project := lib{0}_$(arch)
CXXFLAGS += -fPIC
endif

ifeq ($(lib),)
project := lib{0}_$(arch)
endif

ifeq ($(all),)
project := {0}_$(arch)
endif

# INCLUDE HEADERS
CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:{1}
export CPLUS_INCLUDE_PATH

ifeq ($(platform), android)

INCLUDE := {2}

ifeq ($(arch),x86)
CXX :={3}
AR :={4}
global_OBJECTS += {5}
endif

ifeq ($(arch),arm)
CXX := {6}
AR := {7}
global_OBJECTS += {8}
endif

else
INCLUDE := {9}
global_OBJECTS += {10}
LDADD += -lpthread
LDADD += -ldl
endif

# 交叉工具
objdump: $(OBJDUMP)
	$(OBJDUMP) $(CMD)

objcopy: $(OBJCOPY)
	$(OBJCOPY) $(CMD)

readelf: $(READELF)
	$(READELF) $(CMD)

nm: $(NM)
	$(NM) $(CMD)

# 自动确定
ifneq ($(findstring $(firstword $(CXX)),g++),)
USE_GNUC ?= 1
endif

'''
# unzip a file
def unzip(i, o):
    os.mkdir(o)
    zfile = zipfile.ZipFile(i)
    for name in zfile.namelist():
        (dirname, filename) = os.path.split(name)
        if filename == '':
            # directory
            if not os.path.exists(dirname):
                os.mkdir(o + "/" + dirname)
        else:
            # file
            fd = open(o+"/"+name, 'w')
            fd.write(zfile.read(name))
            fd.close()
    zfile.close()
    
def load(n):
    #打开文件
    with open(n, 'rb') as f:
        c = json.load(f)

    #格式化内容
    return Makevars.format(c["project"],#0
                           c["platform"]["global"]["include"],#1
                           c["platform"]["android"]["include"],#2
                           c["platform"]["android"]["x86"]["cxx"],#3
                           c["platform"]["android"]["x86"]["ar"],#4
                           c["platform"]["android"]["x86"]["libs"],#5
                           c["platform"]["android"]["armeabi"]["cxx"],#6
                           c["platform"]["android"]["armeabi"]["ar"],#7
                           c["platform"]["android"]["armeabi"]["libs"],#8
                           c["platform"]["pc"]["include"],#9
                           c["platform"]["pc"]["libs"])#10

def create(c, i, o):
    unzip(i,o)
    s = load(c)
    with open(o + "/Makevars.global", "wb+") as f:
        f.write(s)


if __name__ == "__main__":
    
    create(sys.argv[1], "ilproject.zip", sys.argv[2])
    
