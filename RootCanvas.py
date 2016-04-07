import ROOT as rt


class HtbCanvasBase(object):
    '''Base class for canvas'''
    def __init__(self):
        self.InitCanvas()

    def InitCanvas(self):
        self.canvas = rt.TCanvas('canvas', 'canvas', 1000, 1000)

    def ClearCanvas(self):
        self.canvas.Clear()

    def SavePrint(self, filename):
        self.canvas.Print(filename)

    def DrawText(self, textObj):
        lex = rt.TLatex()
        lex.SetTextSize(textObj['size'])
        lex.SetNDC()
        lex.SetTextColor(textObj['color'])
        lex.SetTextFont(42)
        lex.DrawLatex(textObj['xPos'], textObj['yPos'], textObj['text'])


class HtbCompCanvas(HtbCanvasBase):
    '''Canvas class for comparision plots'''
    def __init__(self):
        HtbCanvasBase.__init__(self)
        self.InitPads()

    def InitPads(self):
        self.pad1 = rt.TPad('pad1', 'pad1', 0, 0.20, 1, 1, 0, 0, 0)
        self.pad2 = rt.TPad('pad2', 'pad2', 0, 0, 1, 0.28, 0, 0, 0)

        self.pad1.SetTickx(False)
        self.pad1.SetTicky(False)
        self.pad1.SetTopMargin(0.05)
        self.pad1.SetBottomMargin(0.13)
        self.pad1.SetLeftMargin(0.14)
        self.pad1.SetRightMargin(0.08)
        self.pad1.SetFrameBorderMode(0)
        self.pad1.SetFillStyle(0)

        self.pad2.SetTickx(False)
        self.pad2.SetTicky(False)
        self.pad2.SetTopMargin(0)
        self.pad2.SetBottomMargin(0.37)
        self.pad2.SetLeftMargin(0.14)
        self.pad2.SetRightMargin(0.08)
        self.pad2.SetFrameBorderMode(0)
        self.pad2.SetFillStyle(0)


ColorPalette1 = [
    rt.kRed, rt.kBlue, rt.kViolet, rt.kGreen, rt.kCyan, rt.kOrange, rt.kGray, rt.kRed - 7, rt.kPink - 7, rt.kBlue - 7, rt.kGreen - 7, rt.kMagenta - 7, rt.kViolet - 7, rt.kCyan - 7, rt.kSpring - 7, rt.kOrange - 7, rt.kAzure - 7, rt.kTeal - 7]
