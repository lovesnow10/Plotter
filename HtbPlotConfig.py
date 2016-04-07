import HtbJsonBase as HJB
import logger as lg


class HtbPlotConfig(HJB.HtbJsonBase):
    def __init__(self, _inputF):
        lg.logging(
            'Start Initialing %s' % (self.__class__.__name__), 'SPECIAL'
        )
        HJB.HtbJsonBase.__init__(self, _inputF)
        self.MAIN = None
        self.STACK = []
        self.SINGLE = []
        self.DecorateConfig()
        self.General = self.fConfig['General']
        del self.fConfig['General']
        self.CutList = self.fConfig.keys()
        self.Text = {}
        self.Vars = {}
        for cut in self.CutList:
            self.Text[cut] = self.fConfig[cut]['TEXT']
            self.Vars[cut] = self.fConfig[cut].keys()
            self.Vars[cut].remove('TEXT')

    def DecorateConfig(self):
        for _key, _val in self.fConfig.items():
            if _key == 'General' or _key == 'VARSET':
                continue
            elif _key == 'SAMPLESET':
                if 'MAIN' in _val:
                    self.MAIN = _val['MAIN']
                if 'STACK' in _val:
                    self.STACK = _val['STACK']
                if 'SINGLE' in _val:
                    self.SINGLE = _val['SINGLE']
                del self.fConfig[_key]
            else:
                if 'VARSET' not in _val:
                    if 'varlist' in _val:
                        for _var, _set in _val['varlist'].items():
                            self.fConfig[_key][_var] = _set
                        del self.fConfig[_key]['varlist']
                    continue
                else:
                    _varset = _val['VARSET']
                    for _var, _set in self.fConfig['VARSET'][_varset].items():
                        self.fConfig[_key][_var] = _set
                    if 'varlist' in _val:
                        for _var, _set in _val['varlist'].items():
                            self.fConfig[_key][_var] = _set
                        del self.fConfig[_key]['varlist']
                    del self.fConfig[_key]['VARSET']
        del self.fConfig['VARSET']
