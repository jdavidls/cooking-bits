#include <string>
#include <iostream>

using namespace std;

bool check_value = true;

struct Check
{
	const string name;

	Check(const string& name):
		name(name)
	{
		cout << name << " has been constructed" << endl;
	}

	~Check()
	{
		cout << name << " has been destructed" << endl;
	}

	operator bool()
	{
		return check_value;
 	}
};

void check_if()
{
	cout << "before if" << endl;
	if(auto if_check = Check("if-statement"))
	{
		cout << "enter into if body " << endl;
		cout << "leave if body " << endl;
	}
	else
	{
		cout << "enter into else body " << endl;
		cout << "leave else body " << endl;
	}
	cout << "before if" << endl;
}

int main()
{
	cout << "checking if for true cheecks" << endl;
	check_value = true;
	check_if();

	cout << "checking if for false cheecks" << endl;
	check_value = false;
	check_if();

	return 0;
}
