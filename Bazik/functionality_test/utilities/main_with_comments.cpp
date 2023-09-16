#include <iostream>
#include <fstream>
#include <string>
/*
big
comment
*/
int main() {
    // comment
    std::ofstream outfile("../functionality_test/outputs/output.txt");
    // Check if the file is opened successfully
    if (!outfile.is_open()) {
        std::cerr << "Failed to open the file for writing.\n";
        return 1;
    }

    // Write the string \to the file
    outfile << "compilation successful" << '\n';
    return 0;
}