# Makefile for source rpm: acpid
# $Id$
NAME := acpid
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
