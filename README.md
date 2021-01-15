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

Put your code into the bin dir and fit it to your needs.
The tests have to be in the test dir.

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

## Contributing
Make a feature branch from dev (git flow feature start MYFEATURE ) and do a merge request with dev. If the code is reviewed by another person it will be pushed into
dev. At the end of the sprint we merge dev if we all agree into main.

To able to do a pull request the code should be according to the code quality chapter.
