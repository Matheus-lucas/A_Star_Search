#include <iostream>
#include <cstdlib>
#include <ctime>
#include <fstream>
#include <vector>
#include <string>
#include <chrono>
#include <thread>


using namespace std::this_thread;     // sleep_for, sleep_until
using namespace std::chrono_literals; // ns, us, ms, s, h, etc.
using std::chrono::system_clock;

using namespace std;


void create(const vector<vector<int>> B, int row, int col)
{
    // file pointer
    fstream fout;
    cout<<"Criando\n";
    string pasta="D:\\TCC\\src\\mapas\\mapas_aleatorios\\";
    auto filename =  pasta+"mapa_"+to_string(row)+"x"+to_string(col)+".csv";
    cout<<filename;
    remove(filename.c_str());
    // opens an existing csv file or creates a new file.
    fout.open(filename, ios::out | ios::app);
    // Read the input
    for (int i = 0; i < B.size(); i++)
     {
  
        for (int j = 0; j < B[i].size();j++)
        {
             // Insert the data to file
            fout << B[i][j] << "; ";
        }
            
             fout << "\n";
             
    }
}

int main()
{
    for (int a = 1; a<100;a++){
        for(int m=0; m<=100;m++)
        {
            int x, y;
            srand((unsigned)time(0));
            x = (rand() % 10) + 10*a;
            cout << "Rows: "<< x << endl;

            y = (rand() % 10) + 10*a;
            cout << "Columns: "<< y << endl;
            cout << endl;
            int count = 0;
            count = rand() % 2;
            vector<vector<int>> mat{};

            for(int i = 0; i < x; i++)
            {
                vector<int> rows;
                for(int j = 0; j < y; j++)
                {
                    if (( i==0 && j==0) || (i==x-1 && j==y-1) || count%4==0)
                    {
                        rows.push_back(0);
                    }

                    else
                    {
                        rows.push_back(rand() % 2);
                    }
                    count++;

                }
                mat.push_back(rows);
            }
            create(mat, x, y);
            sleep_for(10ns);
            sleep_until(system_clock::now() + 0.1s);
        }
    }
    return 0;
}