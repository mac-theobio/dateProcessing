#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <algorithm>

//Files need to have spaces between commas, working on not needing this.
//Read a csv file, grab only the rows and columns we want, and then spit it back out.
int nice_csv(std::string fn, std::vector<int> rows, std::vector<int> cols){
    //create a vector of <string, int vector> pairs to store the result
    std::vector<std::vector<std::string > > result;
    //representation in the array.
    std::vector<std::string> row; 
    //to read into.
    std::string val, line;
    // i counts the row and j counts the columns.
    int i = 0;
    std::ifstream theFile(fn);
    while (std::getline(theFile, line)){ 
        std::stringstream ss(line);
        row.clear();
        int j = 0; 
        // Grab the data stored in each row and store it in a string variable, 'entry'
        while (ss >> val) {
            // If the next token is a comma, ignore it and move on
            if(ss.peek() == ',') ss.ignore();
                if (cols.empty()){
                    row.push_back(val);
                }
                else{
                    bool colcheck = std::find(cols.begin(), cols.end(), j)  != cols.end();
                    if (colcheck){
                        row.push_back(val);
                    }
                    else{
                    }
                }
            j++;
        }
        if (rows.empty()){
            result.push_back(row);
        }
        else{
            bool rowcheck = std::find(rows.begin(), rows.end(), i) != rows.end();
            if (rowcheck){
                result.push_back(row);
            }
            else{
            }
        }
        i++;
    }
    //Make a csv again.
    std::ofstream out("nice.csv");
    for (auto& row : result) {
        for (auto col : row)
            out << col;
            out << '\n';
        }
        return 0;
}

int main(){
    //Leave either empty to select all.
    std::vector<int> rows = {};
    std::vector<int> cols = {};
    nice_csv("trial.csv", rows, cols);
    return 0;
}

