from bazik import Bazik

import filecmp


def run_test_for_load_graph(func_input, output):
    bazik_instance = Bazik()
    with open(output, "w") as outfile:
        try:
            bazik_instance.load_task_graph(func_input)
        except Exception as e:
            outfile.write(str(e))


def compare_files(file1, file2, output):
    are_files_identical = filecmp.cmp(file1, file2, shallow=False)

    if are_files_identical:
        print("Test passed")
        with open(output, 'w') as res_file:
            res_file.write("passed")
    else:
        print("Test failed")
        with open(output, 'w') as res_file:
            res_file.write("failed")
