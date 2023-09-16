# Bazik
#### Bazik is a simple build tool written on Python.
Bazik can execute tasks of two types: 
- executables
- python functions
 
### Python functions
Python functions that can be executed by Bazik must be written to some python file. This allows multi-line functions to be executed, which would not be possible otherwise.

### Test graph
We use Test graph to describe tasks and their dependencies among themselves.

#### Task graph tags used to describe tasks:
- func
- func_file
- exec
- is_executable
- dependencies
- inputs
- outputs
#### Rules of task graph files:
- Task graph should be a yaml file.
- inputs, outputs are mandatory tags that must be in the description of any task.
- dependencies, inputs, outputs must be arrays.
- The inputs tag is used to specify the input files of the task.
- The outputs tag is used to specify the output files of the task.
- The dependencies tag is used to specify the dependencies of a given task.
- The func, func_file tags are used to describe a task that is a python function.
- The func tag is used to specify the name of the function we want to run.
- The func_file tag is used to specify the path to the file that contains the function we want to run.
- The exec, is_executable tags are used to describe a task that is an executable file.
- The exec tag is used to specify the executable we want to run.
- The is_executable tag is used to indicate that a task is executable. (Used to generalize the logic of Bazik)
- The task description uses either the task's python-function tags or the executable's tags. (Made to make task descriptions more readable) 
- In the description of a task that is an executable file, the is_executable tag should be set to true. (Made to make task descriptions look more consistent.)
- The paths for inputs, outputs, func_file are specified relative to the location of the task graph. (It is made for easy paths indication.)
- Paths to executables should be specified full or as paths relative to the location of bazik.py (Made because it was impossible to make relative paths, as some executables (compilers for example) are not suitable for specifying relative paths.
- Path to task graph should be specified full or as paths relative to the location of bazik.py.
#### Example of correct task which is python function:
```
remove_comments:
  func: remove_comments
  func_file: tasks.py
  dependencies: []
  inputs:
    - utilities/main_with_comments.cpp
  outputs:
    - outputs/main_without_comments.cpp
```

#### Example of correct task which is executable:
```
remove_comments_check:
  exec: ../functionality_test/testers/tester1.sh
  is_executable: true
  dependencies: [remove_comments]
  inputs:
    - outputs/main_without_comments.cpp
    - oracles/main_without_comments_oracle.cpp
  outputs: []

```

### Bazik additional functionalities:
- Check for cyclic dependencies (implemented with check_for_cycles function)
- Check that the function with the name specified in func exists in the file specified in func_file. 
- Logging of execution of tasks.
- Check that the task graph matches the specialization.

## Running of Bazik
```
cd src
python bazik.py your_task --task-graph=your_task_graph.yaml
```
--task-graph=task_graph.yaml by default.

## Functionality test
If you want to see an example of how Bazik works, run the tests in functionality_test using the `python3 bazik.py run_all_tests --task-graph=../functionality_test/task_graph.yaml 
` command (you need to be in the `src` folder), you can also read the tests in the folder for a better understanding of how Bazik works.

## Bonus tasks
### First task
- All tests located in `Bazik_test/`
- Some of the tests are implemented in one way, the other in another way to additionally show all the possibilities of Bazik.
- To run the build graph, which is built and tested by Bazik himself : 
```
cd src
python3 bazik.py bazik_run --task-graph=../Bazik_tests/task_graph_run_bazik.yaml
```

### Second task
- The answer to the second task is located in `Second_bonus_task.md` 