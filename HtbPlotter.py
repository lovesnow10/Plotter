import RootCanvas as RC
import util
import logger as lg
import ROOT as rt


def PlotCompare(Config):
    rootfile = rt.TFile(Config.General['input'], 'READ')
    for cut in Config.CutList:
        lg.logging('Processing cut %s' % (cut))
        for var in Config.Vars[cut]:
            lg.logging('\tProcessing var %s' % (var))

            rt.gROOT.ProcessLine('SetAtlasStyle()')

            canvas = RC.HtbCompCanvas()
            canvas.canvas.Draw()
            canvas.pad1.Draw()
            canvas.pad2.Draw()
            canvas.pad1.cd()

            fHists = util.GetHists(Config, rootfile, cut, var)
            hStack = rt.THStack('hStack', 'hStack')
            h_tot = None
            g_tot = None

            xtitle = Config.fConfig[cut][var]['xname']
            ytitle = Config.fConfig[cut][var]['yname']

            h_data = None
            hasData = False

            if fHists.DATA:
                h_data = fHists.DATA
                hasData = True

            i_color = 2

            for _name, hist in fHists.STACK.items():
                if i_color == 5 or i_color == 8:
                    i_color += 1
                if i_color == 10:
                    i_color = 41
                hist.SetFillColor(i_color)
                hist.SetLineWidth(0)
                hist.SetLineColor(rt.kBlack)
                hStack.Add(hist)
                if h_tot is None:
                    h_tot = hist.Clone('allmc')
                else:
                    h_tot.Add(hist)
                i_color += 1

            b_ShowYields = Config.General['ShowYields']
            b_logy = False
            if 'logy' in Config.fConfig[cut][var]:
                b_logy = Config.fConfig[cut][var]['logy']
            rt.gStyle.SetEndErrorSize(4.0)
            h_dummy = h_tot.Clone('h_dummy')
            h_dummy.Scale(0)
            h_dummy.Draw('HIST')
            hStack.Draw('same HIST')

            g_tot = rt.TGraphAsymmErrors(h_tot)
            g_tot.SetFillStyle(3354)
            g_tot.SetFillColor(rt.kBlack)
            g_tot.SetLineColor(rt.kWhite)
            g_tot.SetLineWidth(0)
            g_tot.SetMarkerSize(0)
            g_tot.Draw('same E2')

            g_data = None
            if hasData:
                h_data.SetMarkerStyle(20)
                h_data.SetLineColor(rt.kBlack)
                h_data.SetLineWidth(2)
                h_data.SetMarkerSize(1.4)
                g_data = rt.TGraphAsymmErrors(h_data)
                g_data.SetMarkerSize(h_data.GetMarkerSize())
                g_data.SetMarkerColor(h_data.GetMarkerColor())
                g_data.SetMarkerStyle(h_data.GetMarkerStyle())
                g_data.SetLineWidth(h_data.GetLineWidth())
            else:
                h_data = h_tot.Clone('dummyData')
                h_data.SetTitle('Asimov Data')
                g_data = rt.TGraphAsymmErrors(h_data)

            if fHists.SINGLE:
                i_color = 2
                for _name, hist in fHists.SINGLE.items():
                    if i_color == 5:
                        i_color += 1
                    hist.SetLineColor(rt.TColor.GetColorBright(i_color))
                    hist.SetLineStyle(2)
                    hist.SetLineWidth(3)
                    ntotal = h_tot.Integral()
                    nhist = hist.Integral()
                    if nhist != 0:
                        hist.Scale(ntotal / nhist)
                    hist.Draw('same HIST')
                    i_color += 1

            if hasData:
                g_data.Draw('same Ep1')

            h_dummy.GetXaxis().SetTitle(xtitle)
            h_dummy.GetYaxis().SetTitle(ytitle)
#            h_dummy.GetYaxis().SetTitleOffset(2.3)
            if b_logy:
                h_dummy.SetMinimum(0.1)
            else:
                h_dummy.SetMinimum(0)
            if hasData:
                ymax = rt.TMath.Max(
                    h_tot.GetMaximum(),
                    h_data.GetMaximum()
                )
                if fHists.SINGLE:
                    for _name, hist in fHists.SINGLE.items():
                        if hist.Integral() != 0:
                            hist_max = hist.GetMaximum() * h_tot.Integral() / hist.Integral()
                            if ymax < hist_max:
                                ymax = hist_max
                if b_logy:
                    h_dummy.SetMaximum(800 * ymax)
                    canvas.pad1.SetLogy(True)
                else:
                    h_dummy.SetMaximum(1.5 * ymax)
            else:
                ymax = h_tot.GetMaximum()
                if not fHists.SINGLE == {}:
                    for _name, hist in fHists.SINGLE.items():
                        hist_max = hist.GetMaximum() * h_tot.Integral() / hist.Integral()
                        if ymax < hist_max:
                            ymax = hist_max
                if b_logy:
                    h_dummy.SetMaximum(500 * ymax)
                    canvas.pad1.SetLogy(True)
                else:
                    h_dummy.SetMaximum(1.5 * ymax)

            canvas.pad1.RedrawAxis()
            canvas.pad1.SetTickx()
            canvas.pad1.SetTicky()

            legX1 = 1 - 0.41 * (596.0 / canvas.pad1.GetWw()) - 0.08
            legX2 = 0.91
            legXmid = legX1 + 0.5 * (legX2 - legX1)

            if b_ShowYields:
                legXmid = legX1 + 0.6 * (legX2 - legX1)
                leg = rt.TLegend(legX1,
                                 0.93 - (
                                     len(fHists.STACK) +
                                     len(fHists.SINGLE) + 2) * 0.04,
                                 legXmid,
                                 0.93)
                leg1 = rt.TLegend(legXmid, leg.GetY1(), legX2, leg.GetY2())

                leg.SetFillStyle(0)
                leg.SetBorderSize(0)
                leg.SetTextAlign(32)
                leg.SetTextFont(rt.gStyle.GetTextFont())
                leg.SetTextSize(rt.gStyle.GetTextSize() * 0.6)
                leg.SetMargin(0.22)

                leg1.SetFillStyle(0)
                leg1.SetBorderSize(0)
                leg1.SetTextAlign(32)
                leg1.SetTextFont(rt.gStyle.GetTextFont())
                leg1.SetTextSize(rt.gStyle.GetTextSize() * 0.6)
                leg1.SetMargin(0.0)

                if hasData:
                    leg.AddEntry(h_data, 'DATA', 'lep')
                    leg1.AddEntry(
                        None,
                        str('%.1f' % (h_data.Integral())),
                        ''
                    )
                if fHists.SINGLE:
                    for _name, hist in fHists.SINGLE.items():
                        leg.AddEntry(hist, _name, 'f')
                        leg1.AddEntry(
                            None,
                            str('%.1f' % (hist.Integral())),
                            ''
                        )
                if fHists.STACK:
                    for _name, hist in fHists.STACK.items():
                        leg.AddEntry(hist, _name, 'f')
                        leg1.AddEntry(
                            None,
                            str('%.1f' % (hist.Integral())),
                            ''
                        )
                leg.AddEntry(None, 'Total', '')
                leg1.AddEntry(None, str('%.1f' % (h_tot.Integral())), '')
                leg.AddEntry(g_tot, 'Uncertainty', 'f')
                leg1.AddEntry(None, '  ', '')
                leg.Draw()
                leg1.Draw()
            else:
                leg = rt.TLegend(legX1,
                                 0.93 -
                                 (
                                     (len(fHists.STACK) +
                                      len(fHists.SINGLE) + 2) / 2
                                 ) * 0.06,
                                 legX2,
                                 0.93)
                leg.SetNColumns(2)
                leg.SetFillStyle(0)
                leg.SetBorderSize(0)
                leg.SetTextAlign(32)
                leg.SetTextFont(rt.gStyle.GetTextFont())
                leg.SetTextSize(rt.gStyle.GetTextSize() * 0.55)
                leg.SetMargin(0.22)

                if hasData:
                    leg.AddEntry(h_data, 'DATA', 'lep')
                if fHists.SINGLE:
                    for _name, hist in fHists.SINGLE.items():
                        leg.AddEntry(hist, _name, 'f')
                if fHists.STACK:
                    for _name, hist in fHists.STACK.items():
                        leg.AddEntry(hist, _name, 'f')
                leg.AddEntry(g_tot, 'Uncertainty', 'f')
                leg.Draw()

            for textObj in Config.Text[cut]:
                canvas.DrawText(textObj)
            sqrts = {"text": "#sqrt{s} = 13TeV", "xPos": 0.18, "yPos": 0.82, "size": 0.035, "color": 1}
            atlas = {"text": "#bf{#it{ATLAS}} Work in Progress", "xPos": 0.16, "yPos": 0.89, "size": 0.06, "color": 1}
            lumi = {"text": "#intLdt =" + Config.General['lumi'] + " pb^{-1}", "xPos": 0.32, "yPos": 0.82, "size": 0.035, "color": 1}
            canvas.DrawText(sqrts)
            canvas.DrawText(atlas)
            canvas.DrawText(lumi)
            canvas.pad2.cd()
            canvas.pad2.GetFrame().SetY1(2)
            h_dummy2 = h_tot.Clone('h_dummy2')
            h_dummy2.Scale(0)
            h_dummy2.Draw('HIST')
#            h_dummy2.GetYaxis().SetTitleOffset(
#                1.0 * h_dummy.GetYaxis().GetTitleOffset()
#            )
            h_ratio = h_data.Clone('h_ratio')
            h_tot_noerr = h_tot.Clone('h_tot_noerr')
            for i_bin in range(1, h_tot_noerr.GetNbinsX() + 1):
                h_tot_noerr.SetBinError(i_bin, 0)
            g_ratio2 = g_tot.Clone('g_ratio2')
            for i_bin in range(1, h_tot_noerr.GetNbinsX() + 1):
                if h_tot_noerr.GetBinContent(i_bin) == 0:
                    continue
                g_ratio2.SetPoint(
                    i_bin - 1,
                    g_ratio2.GetX()[i_bin - 1],
                    g_ratio2.GetY()[i_bin - 1] /
                    h_tot_noerr.GetBinContent(i_bin)
                )
                g_ratio2.SetPointEXlow(
                    i_bin - 1,
                    g_ratio2.GetEXlow()[i_bin - 1]
                )
                g_ratio2.SetPointEXhigh(
                    i_bin - 1,
                    g_ratio2.GetEXhigh()[i_bin - 1]
                )
                g_ratio2.SetPointEYlow(
                    i_bin - 1,
                    g_ratio2.GetEYlow()[i_bin - 1] /
                    h_tot_noerr.GetBinContent(i_bin)
                )
                g_ratio2.SetPointEYhigh(
                    i_bin - 1,
                    g_ratio2.GetEYhigh()[i_bin - 1] /
                    h_tot_noerr.GetBinContent(i_bin))

            h_dummy2.SetTitle('Data/MC')
            h_dummy2.GetYaxis().CenterTitle()
            h_dummy2.GetYaxis().SetTitle('Data/Bkg.')
#            h_dummy2.GetYaxis().SetLabelSize(
#                1.0 * h_ratio.GetYaxis().GetLabelSize()
#            )
            h_dummy2.GetYaxis().SetLabelOffset(0.02)
            h_dummy.GetYaxis().SetLabelOffset(0.02)
            h_dummy2.GetYaxis().SetNdivisions(504, False)
            rt.gStyle.SetEndErrorSize(4.0)
            canvas.pad1.SetTicky()

            h_ratio.Divide(h_tot_noerr)
            h_ratio.SetMarkerStyle(20)
            h_ratio.SetMarkerSize(1.4)
            h_ratio.SetMarkerColor(rt.kBlack)
            h_ratio.SetLineWidth(2)
            g_ratio = rt.TGraphAsymmErrors(h_ratio)
            g_ratio.SetMarkerStyle(h_ratio.GetMarkerStyle())
            g_ratio.SetMarkerSize(h_ratio.GetMarkerSize())
            g_ratio.SetMarkerColor(h_ratio.GetMarkerColor())
            g_ratio.SetLineWidth(h_ratio.GetLineWidth())
            g_ratio.SetLineColor(h_ratio.GetLineColor())
            g_ratio.SetLineStyle(h_ratio.GetLineStyle())

            hline = rt.TLine(
                h_dummy2.GetXaxis().GetXmin(),
                1,
                h_dummy2.GetXaxis().GetXmax(),
                1
                )
            hline.SetLineColor(rt.kRed)
            hline.SetLineWidth(2)
            hline.SetLineStyle(2)
            if hasData:
                g_ratio.Draw('Ep1 same')
            hline.Draw()

            h_dummy2.SetMinimum(0.5)
            h_dummy2.SetMaximum(1.5)
            h_dummy2.GetXaxis().SetTitle(h_dummy.GetXaxis().GetTitle())
#            h_dummy2.GetXaxis().SetTitleOffset(5.0)
            h_dummy.GetXaxis().SetTitle('')
            h_dummy.GetXaxis().SetLabelSize(0)

            labelsize = h_dummy.GetYaxis().GetLabelSize()
            titlesize = h_dummy.GetYaxis().GetTitleSize()
            titleoffset = h_dummy.GetYaxis().GetTitleOffset()

            h_dummy.GetYaxis().SetLabelSize(0.7 * labelsize)
            h_dummy2.GetYaxis().SetLabelSize(1.5 * labelsize)
            h_dummy.GetYaxis().SetTitleSize(0.75 * titlesize)
            h_dummy2.GetYaxis().SetTitleSize(1.7 * titlesize)
            h_dummy2.GetXaxis().SetTitleSize(2.0 * titlesize)
            h_dummy2.GetXaxis().SetLabelSize(1.7 * labelsize)
            h_dummy2.GetYaxis().SetTitleOffset(0.45 * titleoffset)
            h_dummy.GetYaxis().SetTitleOffset(1.1 * titleoffset)
            h_dummy2.GetXaxis().SetLabelOffset(0.02)

            g_ratio2.Draw('same E2')
            canvas.pad2.RedrawAxis()
            plotname = var + '.png'
            outDir = util.checkDir(Config.General['plotdir'])
            outDir = outDir + cut + '/'
            util.MakeDir(outDir)
            canvas.SavePrint(outDir + plotname)
            lg.logging('\t%s Done' % (var), 'SUCCESS')
            del canvas
        lg.logging('%s Done' % (cut), 'SUCCESS')
    rootfile.Close()


def PlotNormal(Config):
    pass

