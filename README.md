# Process Confromance Checking and Discovery with passages

This is a university intership with the goal to extend the pm4py lib

## Installation

### Create Environment

In the project execute the following command to activate the python environment

```bash
./pcc/Scripts/activate
```

After this install the packages that are needed for the project

```bash
pip install -r requirements.txt
```

## Usage

Import the functions from the passage_decomp folder and have fun!

```python
import pm4py
from pccip.passage_decomp.algorithm.process_discovery import passage_process_discovery
from pccip.passage_decomp.algorithm.conformance_checking import passage_conformance_checking
from pccip.passage_decomp.cc.import_model import import_petri_net
from pccip.passage_decomp.pd.import_log import import_log

log_path = 'example_log.xes'
model_path = 'example_model.pnml'


# Process Discovery
new_net, new_im, new_fm = passage_process_discovery(log_path)
pm4py.view_petri_net(new_net, new_im, new_fm)

# Conformance Checking
net, im, fm = import_petri_net(model_path)
log = import_log(log_path)

local_fitness, global_fitness = passage_conformance_checking(log, net, im, fm)

for k in local_fitness:
    print(f'Passage {k+1}: with local alignment transition costs of: {local_fitness[k]["costs"]}')

print(f'Global fitness: {global_fitness["fitness"]}')
print(f'Perfectly fitting traces %age: {global_fitness["percFitTraces"]*100}%')

```

For more information on the code and to see exactly what each step of the algorithm does, feel free to take a look at the tutorial notebook found under the **tutorial** folder.

## Code quality

The test are written with the pytest framework
And are executed with the following command at the project level
And will be only accepted if the coverage is 100%

```bash
pytest -v --cov=test/
```

The code quality wil be evaluated with the flake8 linter in the CircleCI pipeline.
You can check if the quality is sufficcient with the following command.

```bash
flake8 --statistics
```
## Documentation
The documentation can be found in https://kamineedyou.github.io/
## Contributing

Make a feature branch from dev (git flow feature start MYFEATURE ) and do a merge request with dev. If the code is reviewed by another person it will be pushed into
dev. At the end of the sprint we merge dev if we all agree into main.

To able to do a pull request the code should be according to the code quality chapter.
