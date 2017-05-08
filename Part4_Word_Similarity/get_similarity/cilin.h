#pragma once
#include <map>
#include <vector>
#include <string>
#include <set>

#define __LINUX__


using namespace std;

const float CILIN_A = 0.65;
const float CILIN_B = 0.8;
const float CILIN_C = 0.9;
const float CILIN_D = 0.96;
const float CILIN_E = 0.5;
const float CILIN_F = 0.1;
const float PI = 3.1416;
const int   CILIN_DEGREE = 180;

typedef map<string,vector<string> > word_map_t;
typedef map<string,set<int> > relation_code_map_t;
class cilin
{
public:
	cilin(void);	
	~cilin(void);
	
	bool read_cilin(const char* path);
	float similarity(const string& w1,const string& w2);
	long get_ms_time();
	
private:
	float sim_by_code(const string& c1,const string& c2);
	int   get_n(const string&);
	int   get_k(const string&,const string&, const string& common_str);
	float sim_formula(float coeff,int n,int k);
	void  split_code_layer(const string& code,vector<int>& layers,vector<string>& fathers);
	void  get_code_father_child(const string& code);
	int   get_layer_by_no(const string& code,int no);
	string get_common_str(const string& c1,const string& c2);
	static void split(const string& s, const string& delim,vector<string >& ret);
	static string& trim(std::string &s);
		
private:
	word_map_t m_code_word_map; //编码：词项
	word_map_t m_word_code_map;//词项：编码
	
	relation_code_map_t m_code_father_child_map;//父编码,子编码，用于求n

};

