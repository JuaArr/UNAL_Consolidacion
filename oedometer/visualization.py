import numpy as np
import numpy.typing as npt
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import font_manager
from .processing import semilog_model, linear_model
from .utils import ceil_multiple, floor_multiple

# --- Load Ancizar font ---

font_path = './assets/fonts/AncizarSans-Regular_02042016.otf'
font_manager.fontManager.addfont(font_path)
font_name = font_manager.FontProperties(fname=font_path).get_name()

# --- Initialize figure ---

def init_plot(scl_a4=1, aspect_ratio=[3,2], page_lnewdth_cm=15, fnt=font_name, mrksze=2, 
			  lnewdth=1, fontsize=10, labelfontsize=9, tickfontsize=8, dpi=300) -> None:

	# --- Calculate figure size in inches ---
	# scl_a4=2: Half page figure
	if scl_a4 == 2:     
		fac = page_lnewdth_cm/(2.54*aspect_ratio[0]*2) #2.54: cm --> inch
		figsze = [aspect_ratio[0]*fac, aspect_ratio[1]*fac]

	# scl_a4=1: Full page figure
	elif scl_a4 == 1:
		fac = page_lnewdth_cm/(2.54*aspect_ratio[0]) #2.54: cm --> inch
		figsze = [aspect_ratio[0]*fac, aspect_ratio[1]*fac]

	# --- Initialize defaults ---
	plt.rcdefaults()

	# --- General plot setup ---
	# font
	plt.rcParams['font.family'] = fnt

	# figure
	plt.rcParams['figure.facecolor'] = 'white'
	plt.rcParams['figure.figsize'] = figsze
	plt.rcParams['figure.dpi'] = dpi

	# axes
	plt.rcParams['axes.labelsize'] = labelfontsize
	plt.rcParams['axes.linewidth'] = 0.5
	plt.rcParams['axes.titlesize'] = fontsize
	plt.rcParams['axes.axisbelow'] = True
	plt.rcParams['axes.grid'] = True
	plt.rcParams['axes.grid.which'] = 'both'

	# lines
	plt.rcParams['lines.markersize'] = mrksze
	plt.rcParams['lines.linewidth'] = lnewdth

	# hatch
	plt.rcParams['hatch.linewidth'] = lnewdth/2

	# ticks
	plt.rcParams['xtick.labelsize'] = tickfontsize
	plt.rcParams['xtick.direction'] = 'inout'
	plt.rcParams['ytick.labelsize'] = tickfontsize
	plt.rcParams['ytick.direction'] = 'inout'

	# legend
	plt.rcParams['legend.fontsize'] = fontsize
	plt.rcParams['legend.fancybox'] = True
	plt.rcParams['legend.facecolor'] = 'white'
	plt.rcParams['legend.shadow'] = False
	plt.rcParams['legend.edgecolor'] = 'black'
	plt.rcParams['legend.handletextpad'] = 0.2
	plt.rcParams['legend.handlelength'] = 1
	plt.rcParams['legend.borderpad'] = 0.2
	plt.rcParams['legend.labelspacing'] = 0.2
	plt.rcParams['legend.columnspacing'] = 0.2

	#grid
	plt.rcParams['grid.linewidth'] = 0.5

	# mathtext
	plt.rcParams['mathtext.fontset'] = 'cm'

# --- Compressibility curve ---

def save_compressibility(s: npt.NDArray, vr: npt.NDArray, params: dict, 
						 export_dir: Path, language: str='es') -> None:
	
	if language == 'es':
		title = 'Curva de compresibilidad'
		x_label = 'Esfuerzo efectivo [kPa], escala logarítmica'
		y_label = 'Relación de vacíos [-]'
		curve_label = 'Curva de compresibilidad'
		cc_label = 'Línea de consolidación primaria'
		cr_label = 'Línea de descarga/recarga'
	elif language == 'en':
		title = 'Compressibility curve'
		x_label = 'Effective stress [kPa], log scale'
		y_label = 'Void relation [-]'
		curve_label = 'Compressibility curve'
		cc_label = 'Primary consolidation line'
		cr_label = 'Unloading/reloading line'

	slice_cc = params['slice_cc']
	slice_cr = params['slice_cr']

	fig, ax = plt.subplots()
	
	ax.plot(s, vr, color='black', marker='^', linestyle='-', zorder=1, label=curve_label)
	ax.plot(s[slice_cc], semilog_model(s[slice_cc], params['params_cc']),
			color='red', alpha=0.6, zorder=2, label=cc_label)
	ax.plot(s[slice_cr], semilog_model(s[slice_cr], params['params_cr']),
			color='green', alpha=0.6, zorder=2, label=cr_label)

	ax.set_title(title)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	last_xtick = 10.0**np.floor(np.log10(np.max(s)))
	ax.set_xlim(left=1.0, right=ceil_multiple(np.max(s), last_xtick))
	ax.set_ylim(bottom=floor_multiple(np.min(vr)/1.005, 0.1), top=ceil_multiple(np.max(vr)*1.005, 0.1))
	ax.set_xscale('log')
	ax.legend()

	fig.tight_layout()
	fig.savefig(export_dir/'compressibility.png')

def save_strain_energy(s: npt.NDArray, w: npt.NDArray, params: dict, 
					   export_dir: Path, language: str='es') -> None:
	
	if language == 'es':
		title = 'Curva de energía de deformacion'
		x_label = 'Esfuerzo efectivo [kPa]'
		y_label = 'Energía [kN-m] por unidad de volumen'
		curve_label = 'Curva de energía de deformacion'

	elif language == 'en':
		title = 'Strain energy curve'
		x_label = 'Effective stress [kPa]'
		y_label = 'Energy [kN-m] per unit volume'
		curve_label = 'Strain energy curve'

	slice_w = slice(-2)
	slice_w1 = params['slice_w1']
	slice_w2 = params['slice_w2']

	fig, ax = plt.subplots()

	ax.plot(s[slice_w], w[slice_w], color='black', marker='s', linestyle='-', zorder=1, label=curve_label)
	ax.plot(s[slice_w1], linear_model(s[slice_w1], params['params_w1']),
			color='red', alpha=0.6, zorder=2)
	ax.plot(s[slice_w2], linear_model(s[slice_w2], params['params_w2']),
			color='green', alpha=0.6, zorder=2)
	
	ax.set_title(title)
	ax.set_xlabel(x_label)
	ax.set_ylabel(y_label)
	x_ticks = ax.get_xticks()
	y_ticks = ax.get_yticks()
	ax.set_xlim(left=0.0, right=ceil_multiple(np.max(s)*1.005, x_ticks[1]-x_ticks[0]))
	ax.set_ylim(bottom=0.0, top=ceil_multiple(np.max(w)*1.005, y_ticks[1]-y_ticks[0]))
	ax.legend(loc='upper left')

	fig.tight_layout()
	fig.savefig(export_dir/'strain_energy.png')
