# Second BONUS task
### A way to avoid re-running tasks between separate invocations of Bazik.
To avoid re-running of tasks between separate invocations of Bazik, we need to maintain a persistent state 
that can track which tasks have been run and what inputs they used. 
We can do this in this way:
- For each task, create a signature for each task based on its inputs, the source code of the task function, and any other parameters that affect its output. 
- Also, we need to track outputs. We can do this using last their modification timestamps.
- We will store task signatures and output information in state files.
- During each call, we will check the state file to determine if the task needs to be restarted. If the task signature matches the signature in the status file and the output files have not been modified by external processes, skip the task. Otherwise, restart the task and update the state file. 
### Necessary Conditions and Assumptions
- Tasks should be deterministic, on the same inputs they should return the same outputs.
- The system we are working in must correctly display metadata such as timestamps for example.
- Also, the system should not affect the execution of files, because otherwise, even deterministic tasks may stop producing the same outputs with the same inputs.
### When it is possible?
- So my way of avoiding re-running tasks will be possible in systems that do not affect task execution and support correct metadata display.
