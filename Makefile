LIBRARY := SUHH2VLQToHiggsAndLepton
USERLDFLAGS := -lSUHH2core -lSUHH2common -lGenVector -lSUHH2VLQSemiLepPreSel
# enable par creation; this is necessary for all packages containing AnalysisModules
# to be loaded from by AnalysisModuleRunner.
PAR := 1
include ../Makefile.common
