# Compute generalized stacking fault energy using LAMMPS MS simulations.  new goal
#Test  dsss
import numpy as np
import subprocess as sp
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
# hi divyesh you can do it
lammps_exe = "lmp_daily"

latconst_in  = "lat_const.in"
latconst_out = "lat_const.out"

lammps_in  = "elastic_energy.in"
lammps_out = "misfit_energy.out"

def compute_lattice_constant(lat_const_ref, 
							 crystal_type, elt_name, lat_const_0, 
							 lammps_pair_style, lammps_potl):
	f_in = open(lammps_in, "w")
	
	with open(lat_const_ref, "r") as f_ref:
		for line in f_ref:
			if "CRYSTALTYPE" in line:
				line = line.replace("CRYSTALTYPE", crystal_type)
			
			if "LATCONST0" in line:
				line = line.replace("LATCONST0", str(lat_const_0))
				
			if "ELTNAME" in line:
				line = line.replace("ELTNAME", elt_name)
				
			if "PAIRSTYLE" in line:
				line = line.replace("PAIRSTYLE", lammps_pair_style)
				
			if "POTENTIAL" in line:
				line = line.replace("POTENTIAL", lammps_potl)
				
			f_in.write(line)
		
	f_in.close()
	
	lammps_out_str = sp.check_output([lammps_exe, "-in", lammps_in])
	
	with open(lammps_out, "wb") as fout:
		fout.write(lammps_out_str)
	#ds
	lat_const = 0.0
	
	with open(lammps_out, "r") as fl:
		for line in fl:
			if "Lattice constant (Angstroms) = " in line:
				lat_const = float(line.split()[4][:-1])
				
	return lat_const

def generate_gsfe_data(crystal_type, elt_name, lat_const, 
					   x_dir, y_dir, z_dir, 
					   nx, ny, nz, 
					   bx, by, bz, 
					   lammps_ref, 
					   lammps_pairstyle, lammps_potential, 
					   n_samples_x, n_samples_y,
					   f_gsfe_data):
	Lx = nx*bx
	Ly = ny*by
	Lz = nz*bz

	surf_area = nx*ny*bx*by

	init_bot = "crystal_bot.xyz"
	init_top = "crystal_top.xyz"

	## Create initial halves of perfect crystal
	sp.check_output(["atomsk", "--create", crystal_type, str(lat_const), elt_name, \
		"orient", x_dir, y_dir, z_dir, "-duplicate", str(nx), str(ny), str(nz), \
		init_bot, "-ow"])

	sp.check_output(["atomsk", "--create", crystal_type, str(lat_const), elt_name, \
		"orient", x_dir, y_dir, z_dir, "-duplicate", str(nx), str(ny), str(nz), \
		init_top, "-ow"])

	## Store atom coordinates
	xb = []
	yb = []
	zb = []

	xt = []
	yt = []
	zt = []

	f_bot = open(init_bot, "r")

	line = f_bot.readline()
	n_atoms_bot = int(line.split()[0])

	line = f_bot.readline()

	for line in f_bot:
		words = line.split()
		xb.append(float(words[1]))
		yb.append(float(words[2]))
		zb.append(float(words[3]))

	f_bot.close()

	f_top = open(init_top, "r")

	line = f_top.readline()
	n_atoms_top = int(line.split()[0])

	line = f_top.readline()

	for line in f_top:
		words = line.split()
		xt.append(float(words[1]))
		yt.append(float(words[2]))
		zt.append(float(words[3]))

	f_top.close()
	
	sp.check_output(["rm", init_bot])
	sp.check_output(["rm", init_top])

	dx = np.zeros(n_samples_x + 1)
	dy = np.zeros(n_samples_y + 1)

	for i_sample in range(n_samples_x + 1):
		dx[i_sample] = i_sample*bx/n_samples_x

	for i_sample in range(n_samples_y + 1):
		if n_samples_y == 0:
			dy[i_sample] = 0.0
		else:
			dy[i_sample] = i_sample*by/n_samples_y
		
	## Create lmp files with upper and lower halves deformed, 
	## and glued together, for each sample.
	## Compute the surface energy using lammps by computing the total energy
	## of the two halves together, and subtracting the initial energy.

	E_init = 0.0
	misfit_energy = np.zeros(((n_samples_x + 1), (n_samples_y + 1)))

	for i_sample in range(n_samples_x + 1):
		for j_sample in range(n_samples_y + 1):
			## Write deformed configuration to file
			f_def = open("crystal_deformed.xyz", "w")

			f_def.write("{}\n".format(n_atoms_bot + n_atoms_top))
			f_def.write("Deformed crystal: sample {}\n".format(i_sample))

			for i_atom in range(n_atoms_bot):
				f_def.write("{}\t{}\t{}\t{}\n".format(elt_name,
					(xb[i_atom] - 0.5*dx[i_sample]), 
					(yb[i_atom] - 0.5*dy[j_sample]), zb[i_atom]))

			for i_atom in range(n_atoms_top):
				f_def.write("{}\t{}\t{}\t{}\n".format(elt_name,
					(xt[i_atom] + 0.5*dx[i_sample]), 
					(yt[i_atom] + 0.5*dy[j_sample]), (Lz + zt[i_atom])))

			f_def.close()

			sp.check_output(["atomsk", "crystal_deformed.xyz", "lmp", "-ow"])
			sp.check_output(["rm", "crystal_deformed.xyz"])

			### Reset box size
			def_in = "deformed_crystal.lmp"
			fm_def = open(def_in, "w")

			with open("crystal_deformed.lmp", "r") as fd:
				for line in fd:
					if "xhi" in line:
						line = line.replace(line.split()[1], str(Lx))

					elif "yhi" in line:
						line = line.replace(line.split()[1], str(Ly))

					elif "zhi" in line:
						line = line.replace(line.split()[1], str(2*Lz))

					fm_def.write(line)

			fm_def.close()

			#sp.check_output(["rm", "crystal_deformed.lmp"])

			## Compute misfit energy using lammps

			E_full = 0.0
			E_mf = 0.0

			## Compute elastic energy of upper + lower halves
			f_in = open(lammps_in, "w")

			with open(lammps_ref, "r") as fl:
				for line in fl:
					if "INFILE" in line:
						line = line.replace("INFILE", def_in)

					if "PAIRSTYLE" in line:
						line = line.replace("PAIRSTYLE", lammps_pairstyle)

					if "POTENTIAL" in line:
						line = line.replace("POTENTIAL", lammps_potential)

					if "ELTNAME" in line:
						line = line.replace("ELTNAME", elt_name)

					f_in.write(line)

			f_in.close()

			lammps_out_str = sp.check_output([lammps_exe, "-in", lammps_in])
			with open(lammps_out, "wb") as fout:
				fout.write(lammps_out_str)
			
			with open(lammps_out, "r") as fl:
				for line in fl:
					if "%% Total Energy" in line:
						words = line.split()
						E_full = float(words[5])
						
			if i_sample == 0 and j_sample == 0:
				E_init = E_full

			E_mf = (E_full - E_init)/surf_area
			misfit_energy[i_sample, j_sample] = E_mf

			print("Sample ({},{}) of ({},{}): ".format(i_sample, j_sample, n_samples_x, n_samples_y))
			print("Misfit energy         = {} eV/A^2".format(E_mf))

	print("Writing GSFE data to file...")
			
	with open(f_gsfe_data, "w") as fm:
		for i_sample in range(n_samples_x + 1):
			for j_sample in range(n_samples_y + 1):
				gsfe = misfit_energy[i_sample,j_sample] - misfit_energy[0,0]
				fm.write("{}\t{}\t{}\n".format(dx[i_sample], dy[j_sample], gsfe))

			if n_samples_y > 0:
				fm.write("\n")
				
if __name__ == '__main__':
	### Crystal structure and orientation
	crystal_type = "fcc"
	elt_name = "Cu"

	x_dir = "[110]"
	y_dir = "[-112]"
	z_dir = "[1-11]"

	## LAMMPS potential
	lammps_pair_style = "eam/fs"
	lammps_potl = "Mendelev_Cu2_2012.eam.fs"

	## Compute lattice constant
	lat_const_0 = 3.0 # Initial guess for lattice constant
	lat_const_ref = "lat_const_ref.in"

	print("Computing lattice constant using LAMMPS...")

	lat_const = compute_lattice_constant(lat_const_ref, crystal_type, elt_name, lat_const_0, lammps_pair_style, lammps_potl)

	print("Lattice constant = {}".format(lat_const))

	## Generate data for GSFE surface
	gsfe_lammps_ref = "energy_config_relax_ref.in"

	gsfe_nx = 2
	gsfe_ny = 2
	gsfe_nz = 6

	gsfe_bx = lat_const/np.sqrt(2)
	gsfe_by = lat_const*np.sqrt(3)/np.sqrt(2)
	gsfe_bz = lat_const*np.sqrt(3)

	gsfe_nsamples_x = 20
	gsfe_nsamples_y = 40
	
	f_gsfe_data = "gsfe_surface.dat"
	
	print("Generating GSFE data using LAMMPS...")	

	generate_gsfe_data(crystal_type, elt_name, lat_const, 
					   x_dir, y_dir, z_dir, 
					   gsfe_nx, gsfe_ny, gsfe_nz, 
					   gsfe_bx, gsfe_by, gsfe_bz, 
					   gsfe_lammps_ref, 
					   lammps_pair_style, lammps_potl, 
					   gsfe_nsamples_x, gsfe_nsamples_y, 
					   f_gsfe_data)
	
	print("Plotting  surface...")
	
	sx = []
	sy = []
	Esf = []
	
	with open(f_gsfe_data, "r") as f:
		for line in f:
			if not line == '\n':
				words = line.split()
				sx.append(float(words[0]))
				sy.append(float(words[1]))
				Esf.append(float(words[2]))
				
	sx = np.asarray(sx)
	sy = np.asarray(sy)
	Esf = np.asarray(Esf)
	
#	sx, sy = np.meshgrid(sx, sy)
#	Esf = Esf.reshape(sx.shape)
	
	fig = plt.figure()
	ax =fig.add_subplot(111, projection='3d')
	
	ax.plot_trisurf(sx, sy, Esf, cmap=cm.jet, edgecolor='none')
	ax.set_title(r'$\$-surface')
	ax.set_xlabel(r'$s_x$')
	ax.set_ylabel(r'$s_y$')
	ax.set_zlabel(r'$E_{sf}$')
	
	plt.show()
	
	print("All done!")
