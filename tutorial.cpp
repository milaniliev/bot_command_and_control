using namespace std;
#include <iostream>
#include <string>

typedef string[2] Name

void increase(int x ){
  x = x + 1;
  cout << x << endl;
}

int main(int argc, char** argv){
  int your_grades[20];

  int i =0;
  while( i < 20){
    your_grades[i] = i + 1;
    i++;
  }
  
  int my_grades[20];
  
  for(int i =0; i < 20; i++){
    my_grades[i] = your_grades[i];
  }

  if(my_grades == your_grades){
    cout << "YEAH!";
  }
  
  string your_names[20];
  your_names[0] = "Morgan";
  your_names[1] = "Kevin";
  
  cout << your_grades[0];
  cout << your_names[0];
  
  your_grades[0] = 5;
  increase(your_grades[0]);
  cout << your_grades[0] << endl;
  
  return 0;
}

