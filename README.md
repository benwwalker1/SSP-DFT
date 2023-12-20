# Density Functional Theory Examples

## Description

A set of four quantum espresso simulation configurations to solve for various material/chemical properties.

## Table of Contents

### diamond-scf Contents

#### Input Files - Diamond Self-Consistent Field

* `e-cutoff.py` - Python script which tests various energy cutoff values, and plots/tests for convergence for diamond
* `k-points.py` - Python script which tests various k-lattice configurations, and plots/tests for convergence for diamond
* `lattice.py` - Python script which tests various lattice constants for diamond, and calculates its bulk modulus
* `diamond-scf.in` - Quantum Espresso (QE) input file modified by above python scripts for testing
* `C.UPF` - Atomic orbital data for carbon to use as initial SCF guess

#### Output Files/Directories - Diamond Self-Consistent Field

* `e-cutoff.out` - csv-like file for energy cutoff and lattice energy in Rydberg
* `k-outputs.out` - csv-like file for k-points and lattice energy in Rydberg
* `lattice_outputs.out` - csv-like file for lattice constant and lattice energy in Rydberg
* `e_cutoff-run_files` - All QE files related to energy cutoff
* `k_points-run_files` - All QE files related to k-points
* `lattice-run_files` - All QE files related to lattice
* `tmp` - Temporary directory which stores the solved e-density

### diamond-bands Contents

#### Input Files - Diamond Bands

* `diamond-bands.py` - Python script which runs the scf to generate e-density, then tests various points in K space, and plots the bands
* `diamond-scf.in` - QE input file with diamond lattice parameters, which is run by `diamond-bands.py` to generate e-density  in `tmp`
* `diamond-bands-make.in` - QE input file which defines which points to calculate bands in k-space
* `diamond-gnu.in` - QE file which processes the bands from `diamond-bands-make.in` to generate `bandsdata.gnu`
* `C.UPF` - Atomic orbital data for carbon to use as initial SCF guess

#### Output Files/Directories - Diamond Bands

* `bandsdata.gnu` - GNU file which contains all the band data generated from `diamond-bands-make.in` and is parsed by `diamond-bands.py` to graph the band structure
* `diamond-band-make.out` - QE output file from `diamond-bands-make.in`
* `diamond-gnu.out` - QE output file from `diamond-gnu.in`
* `diamond-scf.out` QE output file from the SCF method
* `tmp` - Temporary directory which stores the solved e-density
* `bandsdata` - Contains band data but not parsed by `diamond-bands.py`
* `input_tmp.in` - Autogenerated, not used
* `bandsdata.rap` - Autogenerated, not used

### graphene-bands Contents

#### Input Files - Graphene

* `graphene-bands.py` - Python script which runs the scf to generate e-density, then tests various points in K space, and plots the bands
* `graphene-scf.in` - QE input file with graphene lattice parameters, which is run by `graphene-bands.py` to generate e-density  in `tmp`. The primitive cell (PC) is set to be large enough in Z such that the graphene is modeled as a sheet
* `graphene-bands-make.in` - QE input file which defines which points to calculate bands in k-space
* `graphene-gnu.in` - QE file which processes the bands from `graphene-bands-make.in` to generate `bandsdata.gnu`
* `C.UPF` - Atomic orbital data for carbon to use as initial SCF guess

#### Output Files/Directories - Graphene

* `bandsdata.gnu` - GNU file which contains all the band data generated from `graphene-bands-make.in` and is parsed by `graphene-bands.py` to graph the band structure
* `graphene-band-make.out` - QE output file from `graphene-bands-make.in`
* `graphene-gnu.out` - QE output file from `graphene-gnu.in`
* `graphene-scf.out` QE output file from the SCF method
* `tmp` - Temporary directory which stores the solved e-density
* `bandsdata` - Contains band data but not parsed by `graphene-bands.py`
* `input_tmp.in` - Autogenerated, not used
* `bandsdata.rap` - Autogenerated, not used

### methane Contents

#### Input Files - Methane

* `initial-positions.py` - Simple python script which generates initial guesses for the hydrogen positions based on known methane geometry
* `methane.in` - QE input file for methane, set to use Hellmann-Feynman theorem to iterate ion positions to solve methane. Lattice is large to prevent methane/methane interaction
* `C.UPF` - Atomic orbital data for carbon to use as initial SCF guess
* `H.UPF` - Atomic orbital data for hydrogen to use as initial SCF guess

#### Output Files/Directories - Methane

* `methane.out` - QE output file giving final methane binding energy and atomic positions
* `tmp` - Temporary directory which stores the solved e-density

## Installation

Install the latest Python and Quantum Espresso (QE) versions, and ensure the QE binaries `pw.x` and `bands.x` are your `$PATH` variable.

## Usage

### diamond-scf Usage

Run the `e-cutoff.py`,`k-points.py`, and `lattice.py` scripts in the `diamond-scf` directory, and modify the QE input file `diamond-scf.in` as necessary to maintain convergence

### diamond-bands Usage

Run the `diamond-bands.py` script in the `diamond-bands` directory to automatically calculate the self-consistent field electron density, and to calculate the band structure across the various k-points defined in `diamond-bands-make.in`.

### graphene-bands Usage

Run the `graphene-bands.py` script in the `graphene-bands` directory to automatically calculate the self-consistent field electron density, and to calculate the band structure across the various k-points defined in `graphene-bands-make.in`.

### methane Usage

Simply run the command `rw.x < methane.in > methane.out` to have Quantum Espresso optimize the methane structure! To change the initial guess, generate new hydrogren positions via `initial-positions.py` and copy/paste them into the `ATOMIC_POSITIONS` in the `methane.in` file. To visualize the data, load the output file into XCrysgen