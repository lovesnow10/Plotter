import ROOT as rt
import logger as lg


class HtbHistStore(object):
    '''Class to storage hists'''
    def __init__(self):
        self.DATA = None
        self.STACK = {}
        self.SINGLE = {}

    def SetHists(self, hist, TYPE):
        if TYPE == 'DATA':
            self.DATA = hist
        elif TYPE == 'STACK':
            self.STACK[hist.GetName()] = hist
        elif TYPE == 'SINGLE':
            self.SINGLE[hist.GetName()] = hist
        else:
            lg.logging('CANNOT FIND TYPE %s' % (TYPE), 'WARN')

    def Clean(self):
        self.DATA = None
        self.STACK = {}
        self.SINGLE = {}
