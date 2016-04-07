#!/usr/bin/env python
import HtbPlotter
import HtbPlotConfig
import util
import logger as lg
import ROOT as rt
import sys
import os


if __name__ == '__main__':
    data_path = os.environ['MYANALYSIS'] + '/Plotter/data'
    rt.gROOT.SetMacroPath(data_path)
    rt.gROOT.LoadMacro('atlasstyle/AtlasStyle.C')
    rt.gROOT.SetBatch(True)

    Config = HtbPlotConfig.HtbPlotConfig(sys.argv[1])

    PlotFunc = Config.General['TYPE']

    if not hasattr(HtbPlotter, PlotFunc):
        lg.logging('CANNOT FIND FUNCTION!!!', 'WARN')
        sys.exit(1)
    Run = getattr(HtbPlotter, PlotFunc)
    Run(Config)
