#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Apl1 Spectrum Analyzer
# Author: Codrina Lisaru
# Copyright: Codrina Lisaru
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import osmosdr
import time

from gnuradio import qtgui

class Apl1_spectrum_analyzer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Apl1 Spectrum Analyzer")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Apl1 Spectrum Analyzer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Apl1_spectrum_analyzer")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.uiselect = uiselect = 0
        self.samp_rate = samp_rate = 2000000
        self.bits_per_sample = bits_per_sample = 8
        self.RF_Gain = RF_Gain = 22.9
        self.Center_frequency = Center_frequency = 22.93e6
        self.Bandwidth = Bandwidth = 4000

        ##################################################
        # Blocks
        ##################################################
        self.tab_widget = Qt.QTabWidget()
        self.tab_widget_widget_0 = Qt.QWidget()
        self.tab_widget_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_widget_0)
        self.tab_widget_grid_layout_0 = Qt.QGridLayout()
        self.tab_widget_layout_0.addLayout(self.tab_widget_grid_layout_0)
        self.tab_widget.addTab(self.tab_widget_widget_0, 'No data record')
        self.tab_widget_widget_1 = Qt.QWidget()
        self.tab_widget_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_widget_1)
        self.tab_widget_grid_layout_1 = Qt.QGridLayout()
        self.tab_widget_layout_1.addLayout(self.tab_widget_grid_layout_1)
        self.tab_widget.addTab(self.tab_widget_widget_1, 'Record data')
        self.top_grid_layout.addWidget(self.tab_widget, 0, 0, 1, 4)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._uiselect_options = (0, 1 , )
        # Create the labels list
        self._uiselect_labels = ("Don't record data", 'Record data', )
        # Create the combo box
        self._uiselect_tool_bar = Qt.QToolBar(self)
        self._uiselect_tool_bar.addWidget(Qt.QLabel('Options' + ": "))
        self._uiselect_combo_box = Qt.QComboBox()
        self._uiselect_tool_bar.addWidget(self._uiselect_combo_box)
        for _label in self._uiselect_labels: self._uiselect_combo_box.addItem(_label)
        self._uiselect_callback = lambda i: Qt.QMetaObject.invokeMethod(self._uiselect_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._uiselect_options.index(i)))
        self._uiselect_callback(self.uiselect)
        self._uiselect_combo_box.currentIndexChanged.connect(
            lambda i: self.set_uiselect(self._uiselect_options[i]))
        # Create the radio buttons
        self.tab_widget_grid_layout_1.addWidget(self._uiselect_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tab_widget_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab_widget_grid_layout_1.setColumnStretch(c, 1)
        self._samp_rate_range = Range(1, 2.4e6, 1e3, 2000000, 200)
        self._samp_rate_win = RangeWidget(self._samp_rate_range, self.set_samp_rate, 'Sample rate', "counter_slider", float)
        self.top_grid_layout.addWidget(self._samp_rate_win, 5, 3, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._bits_per_sample_options = (8, 16, 32, 64, )
        # Create the labels list
        self._bits_per_sample_labels = ('8 bits', '16 bits', '32 bits', '64 bits', )
        # Create the combo box
        self._bits_per_sample_tool_bar = Qt.QToolBar(self)
        self._bits_per_sample_tool_bar.addWidget(Qt.QLabel('Bits per sample - wav' + ": "))
        self._bits_per_sample_combo_box = Qt.QComboBox()
        self._bits_per_sample_tool_bar.addWidget(self._bits_per_sample_combo_box)
        for _label in self._bits_per_sample_labels: self._bits_per_sample_combo_box.addItem(_label)
        self._bits_per_sample_callback = lambda i: Qt.QMetaObject.invokeMethod(self._bits_per_sample_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._bits_per_sample_options.index(i)))
        self._bits_per_sample_callback(self.bits_per_sample)
        self._bits_per_sample_combo_box.currentIndexChanged.connect(
            lambda i: self.set_bits_per_sample(self._bits_per_sample_options[i]))
        # Create the radio buttons
        self.tab_widget_grid_layout_1.addWidget(self._bits_per_sample_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.tab_widget_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab_widget_grid_layout_1.setColumnStretch(c, 1)
        self._RF_Gain_range = Range(0, 50, 1, 22.9, 200)
        self._RF_Gain_win = RangeWidget(self._RF_Gain_range, self.set_RF_Gain, 'RF Gain in dB', "counter_slider", float)
        self.top_grid_layout.addWidget(self._RF_Gain_win, 5, 1, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Center_frequency_range = Range(22.93e6, 1760e6, 12.5e3, 22.93e6, 200)
        self._Center_frequency_win = RangeWidget(self._Center_frequency_range, self.set_Center_frequency, 'Center frequency in Hz', "counter_slider", float)
        self.top_grid_layout.addWidget(self._Center_frequency_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Bandwidth_range = Range(1, 100e6, 1, 4000, 200)
        self._Bandwidth_win = RangeWidget(self._Bandwidth_range, self.set_Bandwidth, 'Bandwidth in Hz', "counter_slider", float)
        self.top_grid_layout.addWidget(self._Bandwidth_win, 5, 2, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(Center_frequency, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(RF_Gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
        self.qtgui_waterfall_sink_x_0_0 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            Center_frequency, #fc
            Bandwidth, #bw
            'Waterfall (Spectrogram)', #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_1.addWidget(self._qtgui_waterfall_sink_x_0_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.tab_widget_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab_widget_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            Center_frequency, #fc
            Bandwidth, #bw
            'Waterfall (Spectrogram)', #name
            1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.tab_widget_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab_widget_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            'Time Domain', #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', 'time')

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.tab_widget_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab_widget_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            'Time Domain', #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', 'time')

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.tab_widget_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab_widget_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            Center_frequency, #fc
            Bandwidth, #bw
            'Spectrum Analyzer', #name
            1
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.01)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.tab_widget_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab_widget_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            Center_frequency, #fc
            Bandwidth, #bw
            'Spectrum Analyzer', #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.01)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.tab_widget_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.tab_widget_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            1024, #size
            'Constellation', #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_1.addWidget(self._qtgui_const_sink_x_0_0_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.tab_widget_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab_widget_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            'Constellation', #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_0.addWidget(self._qtgui_const_sink_x_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.tab_widget_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.tab_widget_grid_layout_0.setColumnStretch(c, 1)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink('M:\\OneDrive\\02_Master\\2_2\\02_Disertatie\\GNU Radio implementation\\Aplicatia 1 - Analizor spectral\\SavedData.wav', 2, samp_rate, bits_per_sample)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, 3.2e6,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, 3.2e6,True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,uiselect)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_wavfile_sink_0, 1))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.qtgui_waterfall_sink_x_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_selector_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Apl1_spectrum_analyzer")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_uiselect(self):
        return self.uiselect

    def set_uiselect(self, uiselect):
        self.uiselect = uiselect
        self._uiselect_callback(self.uiselect)
        self.blocks_selector_0.set_output_index(self.uiselect)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_bits_per_sample(self):
        return self.bits_per_sample

    def set_bits_per_sample(self, bits_per_sample):
        self.bits_per_sample = bits_per_sample
        self._bits_per_sample_callback(self.bits_per_sample)

    def get_RF_Gain(self):
        return self.RF_Gain

    def set_RF_Gain(self, RF_Gain):
        self.RF_Gain = RF_Gain
        self.rtlsdr_source_0.set_gain(self.RF_Gain, 0)

    def get_Center_frequency(self):
        return self.Center_frequency

    def set_Center_frequency(self, Center_frequency):
        self.Center_frequency = Center_frequency
        self.qtgui_freq_sink_x_0.set_frequency_range(self.Center_frequency, self.Bandwidth)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.Center_frequency, self.Bandwidth)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.Center_frequency, self.Bandwidth)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(self.Center_frequency, self.Bandwidth)
        self.rtlsdr_source_0.set_center_freq(self.Center_frequency, 0)

    def get_Bandwidth(self):
        return self.Bandwidth

    def set_Bandwidth(self, Bandwidth):
        self.Bandwidth = Bandwidth
        self.qtgui_freq_sink_x_0.set_frequency_range(self.Center_frequency, self.Bandwidth)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.Center_frequency, self.Bandwidth)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.Center_frequency, self.Bandwidth)
        self.qtgui_waterfall_sink_x_0_0.set_frequency_range(self.Center_frequency, self.Bandwidth)





def main(top_block_cls=Apl1_spectrum_analyzer, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
