Formula characterizer, automates the following:

### Phase 1 - conduct experiments
- Run binaries of SAT solvers with input formulas
 (or any other program that produces output; generic)
- Saves 'formula.out' files to disk (by the actual program, or by script)
- Repeat the process

* Can feed: directories with formulas, text file of paths (line by line), or individual files
* Proccesses can work in parallel
* Ability to resume
* Set solvers by config files
* Set experiments by config files (multiple solvers)
* Plot graphs by config files
* Saves track: some record of the current instance

### Phase 2 - Collect and organize data
- Gets current track from 1st phase
- Collect data from disk
- Organize by experiments config
- Update track

### Phase 3 - Manipulate data
- Gets current track from 2nd phase
- Make some data manipulation (in my case: compute entropy) 
 (to one of the solvers series of outputs)
- Saves all instances to ONE csv file (pandas?)
 (Each line is an instance)
- Update track

### Phase 4 - Plot graphs
- Gets track from 3rd phase
- Plot
- Update track



