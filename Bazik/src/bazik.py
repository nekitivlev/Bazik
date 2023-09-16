import os
import subprocess
import yaml
import argparse
from logging import getLogger, basicConfig


def execute_task_executable(executable, inputs, outputs):
    subprocess.run([executable, *inputs])
    return outputs


def execute_task_function(func, inputs, outputs):
    func(*inputs, *outputs)
    return outputs


def check_for_cycles(task_name, task_graph, path=None, visited=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(task_name)
    path.append(task_name)

    for neighbor in task_graph[task_name].get('dependencies', []):
        if neighbor not in visited:
            if check_for_cycles(neighbor, task_graph, path, visited):
                return True
        elif neighbor in path:
            path.append(neighbor)  # Add the neighbor to show the cycle
            cycle_str = ' -> '.join(path)
            raise ValueError(f"Cyclic dependency detected: {cycle_str}")

    path.pop()
    return False


class Bazik:
    # Configure logging
    basicConfig(level='INFO')
    logger = getLogger(__name__)

    # Task registry to hold task functions and dependencies
    TASK_REGISTRY = {}
    EXECUTED_TASKS = set()

    @staticmethod
    def parse_arguments():
        parser = argparse.ArgumentParser(description='Execute a specified task and its dependencies.')
        parser.add_argument('task', type=str, help='The name of the task to execute')
        parser.add_argument('--task-graph', dest='task_graph_path', default='task_graph_run_bazik.yaml',
                            help='Path to the task graph file')

        return parser.parse_args()

    # I use this to figure out what functions are in a given python file
    @staticmethod
    def exec_python_file(filepath):
        with open(filepath) as f:
            code = compile(f.read(), filepath, 'exec')
            exec(code, globals())

    @classmethod
    def load_task_graph(cls, filepath):
        base_dir = os.path.dirname(os.path.abspath(filepath))
        with open(filepath, 'r') as file:
            try:
                graph = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                raise ValueError(f"Failed to load task graph: {exc}")

            for task_name, task_info in graph.items():
                if not isinstance(task_name, str):
                    raise ValueError(f"Task name '{task_name}' must be a string.")

                if not isinstance(task_info, dict):
                    raise ValueError(f"Task info for '{task_name}' must be a dictionary.")

                required_keys = ["inputs", "outputs"]

                for key in required_keys:
                    if key not in task_info:
                        raise ValueError(f"Task '{task_name}' is missing required key: '{key}'")

                if 'inputs' in task_info and not isinstance(task_info['inputs'], list):
                    raise ValueError(f"'inputs' field in task '{task_name}' must be a list.")

                if 'outputs' in task_info and not isinstance(task_info['outputs'], list):
                    raise ValueError(f"'outputs' field in task '{task_name}' must be a list.")

                if 'dependencies' in task_info and not isinstance(task_info['dependencies'], list):
                    raise ValueError(f"'dependencies' field in task '{task_name}' must be a list.")

                if 'is_executable' in task_info and not isinstance(task_info['is_executable'], bool):
                    raise ValueError(f"'is_executable' field in task '{task_name}' must be a boolean.")

                if 'is_executable' in task_info and ('func' in task_info or 'func_file' in task_info):
                    raise ValueError(f"functional and executable tags together in  {task_name}")

                if task_info.get('func_file'):
                    task_info['func_file'] = os.path.join(base_dir, task_info['func_file'])
                    cls.exec_python_file(task_info['func_file'])
                    try:
                        func = eval(task_info['func'])
                    except NameError as exc:
                        raise ValueError(
                            f"Function '{task_info['func']}' not defined in file '{task_info['func_file']}': {exc}")
                else:
                    func = task_info['exec']
                task_info['inputs'] = [os.path.join(base_dir, i) for i in task_info['inputs']]
                task_info['outputs'] = [os.path.join(base_dir, o) for o in task_info['outputs']]
                cls.TASK_REGISTRY[task_name] = {
                    "func": func,
                    "is_executable": task_info.get('is_executable', False),
                    "dependencies": task_info.get('dependencies', []),
                    "inputs": task_info.get('inputs', []),
                    "outputs": task_info.get('outputs', [])
                }
            for task_name in cls.TASK_REGISTRY:
                check_for_cycles(task_name, cls.TASK_REGISTRY)

    @classmethod
    def execute(cls, task_name):
        if task_name in cls.EXECUTED_TASKS:
            cls.logger.info(f"Skipping '{task_name}' - already executed")
            return

        if task_name not in cls.TASK_REGISTRY:
            raise ValueError(f"No task named '{task_name}' found.")

        task = cls.TASK_REGISTRY[task_name]

        for dep in task["dependencies"]:
            cls.execute(dep)

        inputs = task.get('inputs', [])
        outputs = task.get('outputs', [])

        if task['is_executable']:
            execute_task_executable(task['func'], inputs, outputs)
        else:
            execute_task_function(task['func'], inputs, outputs)

        cls.EXECUTED_TASKS.add(task_name)

    def main(self):
        args = self.parse_arguments()
        self.load_task_graph(args.task_graph_path)
        self.execute(args.task)


if __name__ == "__main__":
    bazik = Bazik()
    bazik.main()
