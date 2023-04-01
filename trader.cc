#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
#include <cpr/cpr.h>

using namespace std;
using namespace cpr;

struct Node
{
    int volume;
    int price;
    
};


int main(int argc, char const *argv[])
{
    Response r = Get(Url{"http://192.168.1.101:3000/getAllPairs"});
    cout << r.text << endl;
    return 0;
}
