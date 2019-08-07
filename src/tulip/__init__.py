import sys
import argparse
import threading


class TaskNode:
    def __init__(self, name, task, pre, post, description):
        self.name = name
        self.task = task
        self.pre = pre
        self.post = post
        self.description = description


class TulipTask:
    _task_node_list = []

    @staticmethod
    def task(name, **kwargs):
        """
        decorate task class to create new task node.
        """
        def wrapper(TaskCls):
            task_node = TaskNode(
                name=name,
                task=TaskCls(),
                pre=kwargs.get("pre", []),
                post=kwargs.get("post", []),
                description=kwargs.get("description"),
            )
            TulipTask._task_node_list.append(task_node)
        return wrapper

    @classmethod
    def start(cls):
        """
        start tulip to process task.
        """
        try:
            if len(sys.argv) == 1:
                print('\n'.join([
                    f"{task.name}"
                    for task in cls._task_node_list
                ]))
                sys.exit(0)

            task_node = cls._get_task_node(sys.argv[1])
            parser = cls._setup_task(task_node)
            cls._run_task(task_node, parser=parser)

            sys.exit(0)
        except Exception as e:
            print(f"tulip-error: {e}")
            sys.exit(1)

    @classmethod
    def run_task(cls, name, **kwargs):
        """
        call a task without setup, pass args directly.
        """
        args = argparse.Namespace(**kwargs)
        task_node = cls._get_task_node(name)
        cls._run_task(task_node, args=args)

    @classmethod
    def _get_task_node(cls, name):
        """
        get a task node with given name.
        """
        for task_node in cls._task_node_list:
            if task_node.name == name:
                return task_node
        raise cls.TaskNotFound(f"task '{name}' is not found.")

    @classmethod
    def _get_task_nodes(cls, names):
        """
        get list of task nodes with give names
        """
        return [
            task_node
            for task_node in cls._task_node_list
            if task_node.name in names
        ]

    @classmethod
    def _setup_task(cls, task_node):
        """
        call the setup function of a task.
        """
        parser = argparse.ArgumentParser()
        if hasattr(task_node.task, "setup"):
            task_node.task.setup(parser)
        return parser

    @classmethod
    def _run_task(cls, task_node, parser=None, args=None):
        """
        call the run function of a task.
        """
        # pre-tasks
        for pre_task_node in cls._get_task_nodes(task_node.pre):
            cls._run_task(pre_task_node, parser)

        # task
        run_args = args or parser.parse_args(sys.argv[2:])
        task_node.task.run(run_args)

        # post tasks
        for post_task_node in cls._get_task_nodes(task_node.post):
            cls._run_task(post_task_node, parser)

    class TaskNotFound(Exception):
        pass


class MultiRun:
    threads = []

    def add(self, target, args=(), kwargs={}):
        self.threads.append(threading.Thread(target=target, args=args, kwargs=kwargs))
    
    def run(self, join=False):
        for t in self.threads:
            t.start()
        
        if join:
            for t in self.threads:
                t.join()