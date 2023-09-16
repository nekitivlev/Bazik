#include <iostream>
#include <fstream>
#include <string>

int main() {
    
    std::ofstream outfile("../functionality_test/outputs/output.txt");
    
    if (!outfile.is_open()) {
        std::cerr << "Failed to open the file for writing.\n";
        return 1;
    }

    
    outfile << "compilation successful" << '\n';
    return 0;
}