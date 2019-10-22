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
    tuliptask.proc.run("docker build")
    # or use docker command shortcut
    tuliptask.proc.d("build")
```
available command shortcuts:
- `proc.d()` = `proc.run("docker")`
- `proc.dc()` = `proc.run("docker-compose")`
- `proc.k()` = `proc.run("kubectl")`
- `proc.mk()` = `proc.run("minikube")`

## run task before/after another task
```python
@TulipTask.task("init")
class Init:
    def run(self, args):
        print("initializing...")

@TulipTask.task("cleanup")
class CleanUp:
    def run(self, args):
        print("cleaning up...")

@TulipTask.task("dev", pre=["init"], post=["cleanup"])
class Dev:
    def run(self, args):
        print("doing some dev task")
```

## run a task directly by passing in args
```python
from tulip import TulipTask, proc

@TulipTask.task("django_manage")
class DjangoManage:
    def setup(self, parser):
        parser.add_argument("--cmd")
    
    def run(self, args):
        proc.dc(f"run python3 ./manage.py {args.cmd}")

@TulipTask.task("migrate")
class Migrate:
    def run(self, args):
        TulipTask.run_task("django_manage", cmd="migrate") # pass in --cmd args to 'django_manage' task
```

## extend base task
Tuliptask provides several base tasks for convenience.  
base task will add base `setup()`, `run()` and other convenient functions.

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

## Utilities
### tuliptask.utils.GitUtil
  - `git_ts()`: get timestamp of current branch.
  - `git_hash()`: get hash of current branch.

### tuliptask.utils.TextUtil
  - `colored_text(str, color)`: add color to string, default color is 33. [more info](https://misc.flogisoft.com/bash/tip_colors_and_formatting).
  - `eval_file(file_path, vars_dict)`: replace placeholder (in ${} format) in a file with a dict.
    ```yaml
    # test.yaml
    data:
        name: ${dataname}
    ```
    ```python
    eval_file("test.yaml", {"dataname": "real name"})
    ```
