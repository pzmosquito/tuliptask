# tuliptask
Simple task runner supports running multiple tasks in parallel.

## Installation
```sh
pip install tuliptask
```

## Basic Usage
- Create a tulip task file: `tulipfile.py`
- Add a simple task
```python
from tuliptask import TulipTask

@TulipTask.task("dev") # use decorator to define a task
class Dev:
    def run(self, args): # tuliptask will call `run()` function to run the task.
        print("start development")

TulipTask.start()
```
- run the command in terminal:
```sh
tulip dev
```

## add arguments to the task
```python
from tuliptask import TulipTask

@TulipTask.task("dev")
class Dev:
    def setup(self, parser): # tuliptask will call `setup()` function to add arguments.
        parser.add_argument("--container") # use Python built-in `argparse` to add arguments

    def run(self, args):
        print(f"start development for container: {args.container}")

TulipTask.start()
```

## run shell command
```python
def run(self, args):
    tulip.proc.run("docker build")
    # or use docker command shortcut
    tulip.proc.d("build")
```
available command shortcuts:
- `proc.d()` = `proc.run("docker")`
- `proc.dc()` = `proc.run("docker-compose")`
- `proc.k()` = `proc.run("kubectl")`
- `proc.mk()` = `proc.run("minikube")`

## extend base task
Tuliptask provides several base tasks for convenience.

```python
from tuliptask import TulipTask
from tuliptask.tasks import KubeTask

@TulipTask.task("dev")
class Dev(KubeTask):
    def setup(setup, parser):
        super().setup(parser)

    def run(self, args):
        super().run(args)
        print("start development")

TulipTask.start()
```
base task will add base `setup()`, `run()` and other convenient functions.

### KubeTask
- `setup(parser)`:
  - `--context`: kubernetes context
  - `--namespace`: kubernetes namespace
- `k(cmdstr, **kwargs)`: kubectl command shortcut with `--context` and `--namespace` args appended if available
- `kube_info()`: print namespace and context info

## multi-run
When we have multiple tasks or services that do not depend on each other, it's waste of time to run them in serial. For example, if you need to build backend and frontend images, they can be run in parallel to speed up the process.
```python
from tuliptask import TulipTask, MultiRun, proc

@TulipTask.task("dev")
class Dev:
    def run(self, args):
        mr = MultiRun()
        mr.add(proc.d, args=("build api", ))
        mr.add(proc.d, args=("build ui", ))
        mr.run()

TulipTask.start()
```

## WIP