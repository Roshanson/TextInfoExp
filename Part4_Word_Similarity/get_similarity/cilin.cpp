#include "cilin.h"
#include "stdio.h"
#include <iostream>  
#include <fstream>  
#include <stdlib.h>  
#include <map>
#include <string>
#include <math.h>

#ifdef __WINDOWS__	
#include<ctime>
#else
#include <sys/time.h>  
#endif
cilin::cilin(void)
{
}


cilin::~cilin(void)
{
}

//计算词的相似度
float cilin::similarity(const string& w1,const string& w2){
	word_map_t::iterator it1 = m_word_code_map.find(w1);
	word_map_t::iterator it2 = m_word_code_map.find(w2);
	if(it1 == m_word_code_map.end() || it2 == m_word_code_map.end())
		return 0;

	//两个词可能对应多个编码
	vector<string>& code1_vec = it1->second;
	vector<string>& code2_vec = it2->second;

	float sim_max = 0;
	float sim_cur = 0;
	for (int i = 0; i < code1_vec.size(); ++i)
	{
		for (int j = 0; j < code2_vec.size(); ++j){
			sim_cur = sim_by_code(code1_vec[i],code2_vec[j]);
			if(sim_max < sim_cur)
				sim_max = sim_cur;
		}
	}
	return sim_max;
}

//读词文件，构建词集
bool cilin::read_cilin(const char* path){
	if(!path)
		return false;

	char buffer[8192];  
	ifstream in(path,ifstream::in);  
	if (! in.is_open()){ 
		cout << "Error opening file"; 
		exit (1); 
	}  

	vector<string> split_vec;
	split_vec.reserve(32);
	string delim = " ";
	int line_count = 0;

	while (!in.eof() ){  
		in.getline (buffer,sizeof(buffer));  
		string src(buffer);

		split_vec.clear();
		split(src,delim,split_vec);
		if(split_vec.size() < 2)			
			break;

		line_count++;
		/*word_map_t::iterator it = m_code_word_map.find(split_vec[0]);
		if(it == m_code_word_map.end())*/
			m_code_word_map[split_vec[0]].assign(split_vec.begin() + 1 ,split_vec.end());
		//else

		vector<string>::iterator it = split_vec.begin() + 1;
		for (; it != split_vec.end(); ++it)
		{
			string& w = *it;		
			m_word_code_map[w].push_back(split_vec[0]);
		}

		get_code_father_child(split_vec[0]);
	}  
	printf("end reading...\n");
	return true;
};

void cilin::split_code_layer(const string& code,vector<int>& layers,vector<string>& fathers){
	if(code.size() < 8){
		//error code;
		return;
	}
	layers.clear();
	fathers.clear();

	layers.push_back(code[0]);
	fathers.push_back(code.substr(0,1));

	layers.push_back(code[1]);
	fathers.push_back(code.substr(0,2));
	
	int l = atoi(code.substr(2,2).c_str());
	layers.push_back(l);
	fathers.push_back(code.substr(0,4));

	layers.push_back(code[4]);
	fathers.push_back(code.substr(0,5));

	l = atoi(code.substr(5,2).c_str());
	layers.push_back(l);	
}

//得到编码的第n层编码号,用于求k
int cilin::get_layer_by_no(const string& code,int n){
	if(code.size() < 8){
		//error code;
		return -1;
	}
	
	switch(n){
	case 0:
	case 1:
		return code[n];
		break;
	case 2:
		return atoi(code.substr(2,2).c_str());
		break;
	case 3:
		return code[4];
		break;
	case 4:
		return atoi(code.substr(5,2).c_str());
		break;
	}

	return -1;
}

//存父子关系，提高反复求n效率
void cilin::get_code_father_child(const string& code){
	vector<int> layer_vec;
	vector<string>father_key_vec;

	split_code_layer(code,layer_vec,father_key_vec);
	if(layer_vec.size() < 5 || father_key_vec.size() < 4)
		return;

	for (int i = 0; i < 4; ++i){
		string& key = father_key_vec[i];
		//m_code_word_map[key].insert(layer_vec[i+1]);

		relation_code_map_t::iterator it_fc = m_code_father_child_map.find(key);
		if(it_fc == m_code_father_child_map.end()){
			set<int> child_set;
			child_set.insert(layer_vec[i+1]);
			m_code_father_child_map.insert(make_pair(key,child_set));
		}
		else
			m_code_father_child_map[key].insert(layer_vec[i+1]);
	}
}

string& cilin::trim(string &s){  
	if (s.empty()){  
		return s;  
	}  

	s.erase(0,s.find_first_not_of(" "));  
	s.erase(s.find_last_not_of(" ") + 1);  
	return s;  
}  

void cilin::split(const string& s, const string& delim,vector<string >& ret)  
{  
	size_t last = 0;  
	size_t index=s.find_first_of(delim,last);  
	while (index!=std::string::npos)  
	{  
		ret.push_back(s.substr(last,index-last));  
		last=index+1;  
		index=s.find_first_of(delim,last);  
	}  
	if (index-last>0)  
	{  
		ret.push_back(s.substr(last,index-last));  
	}  
}  



//计算相似度的公式，不同的层系数不同
float cilin::sim_formula(float coeff,int n,int k){
	return coeff * cos(n * PI / CILIN_DEGREE) * ((n - k + 1) / float(n));
}

//根据编码计算相似度
float cilin::sim_by_code(const string& c1,const string& c2){
	if(c1.empty() || c2.empty())
		return .0f;

	char c1_last_ch = c1[c1.length() - 1];
	char c2_last_ch = c2[c2.length() - 1];

	// 如果有一个编码以'@'结尾，那么表示自我封闭，这个编码中只有一个词，直接返回f
	if(c1_last_ch == '@' || c2_last_ch == '@')
		return CILIN_F;

	string common_str = get_common_str(c1,c2);
	if(common_str.empty())
		return .0f;

	int len_common = common_str.length();
	// 如果前面七个字符相同，则第八个字符也相同，要么同为'='，要么同为'#''
	if(len_common >= 7){
		if(c1_last_ch != c2_last_ch)
			return .0f;

		if(c1_last_ch == '=')
			return 1.0f;

		if(c1_last_ch == '#')
			return CILIN_E;
	}

	int k = get_k(c1,c2,common_str);
	int n = get_n(common_str);

	//printf("  %s,%s,n = %d,k = %d  ",c1.c_str(),c2.c_str(),n,k);
	switch(len_common){
	case 0://若两个义项不在同一棵树上
		return CILIN_F;
	case 1:
		return sim_formula(CILIN_A, n, k);
	case 2:	
		return sim_formula(CILIN_B, n, k);
	case 4:	
		return sim_formula(CILIN_C, n, k);
	case 5:	
		return sim_formula(CILIN_D, n, k);
	}

	return .0f;
}

//计算所在分支层的分支数
//即计算分支的父节点总共有多少个子节点
//两个编码的common_str决定了它们共同处于哪一层
//例如，它们的common_str为前两层，则它们共同处于第三层，则我们统计前两层为common_str的第三层编码个数就好了
int  cilin::get_n(const string& common_str){

	if(common_str.empty())
		return 0;

	relation_code_map_t::iterator it = m_code_father_child_map.find(common_str);
	if(it != m_code_father_child_map.end()){
		return it->second.size();
	}
	return 0;
}

//返回两个编码对应分支的距离，相邻距离为1
int cilin::get_k(const string&c1,const string& c2, const string& common_str){
	if(c1.empty() || c2.empty() || common_str.empty())
		return -1;
	int len_common = common_str.size();
	int cur_layer_no = 0;
	
	if(len_common == 1 || len_common == 2)
		cur_layer_no = len_common;
	else if(len_common == 4)
		cur_layer_no = 3;
	else if(len_common == 5)
		cur_layer_no = 4;
	else if(len_common == 7)
		cur_layer_no = 5;
	else return -1;

	int c1_layer_no = get_layer_by_no(c1,cur_layer_no);
	int c2_layer_no = get_layer_by_no(c2,cur_layer_no);
	return abs(c1_layer_no - c2_layer_no);
}

string cilin::get_common_str(const string& c1,const string& c2){
	string common_str;
	for (int i = 0; i < c1.length(); ++i)
	{
		if(c1[i] == c2[i])
			common_str.push_back(c1[i]);
		else{
			if(i == 3 || i == 6)
				//common_str.pop_back();
				common_str.erase(common_str.size() - 1,1);

			break;
		}
	}
	return common_str;
}

long cilin::get_ms_time()    
{    
#ifdef __WINDOWS__	
	return clock();
#else
	struct timeval tv;    
	gettimeofday(&tv,NULL);    
	return tv.tv_sec * 1000 + tv.tv_usec / 1000;
#endif
}  



int test () {
#ifdef __WINDOWS__
	char* path = "F:\\chatbot\\CilinSimilarity-master\\data\\cilin.txt";
#else
	char* path = "cilin.txt";
#endif

	cilin cl;
	long t1 = cl.get_ms_time();
	cl.read_cilin(path);
	long t2 = cl.get_ms_time();

	string words[]={ "国民","群众","党群","良民","同志","成年人","市民","亲属","志愿者","先锋"};
	string w1 = "人民";

	float score = .0f;
	int length = sizeof(words) / sizeof(words[0]);
	for (int i = 0; i < length; ++i)
	{
		score = cl.similarity(w1,words[i]);
		printf("%s,%s,%.4f\n",w1.c_str(),words[i].c_str(),score);
	}
	long t3 = cl.get_ms_time();

	printf("\n cost =%ld,%ld",t2-t1,t3-t2);
	return 0;
}

int main(){
	return test();	
}

extern "C" {  
	cilin cl;
	void read_cilin(const char* path) {  
		cl.read_cilin(path);
	}  

	float similarity(const char* w1,const char* w2) {  
		if(!w1 || !w2){
			printf("error para\n");
			return .0f;
		}
		
		float score = cl.similarity(w1,w2);
		//printf("w1=%s,w2=%s score = %.3f",w1,w2,score);
		
		return  score; 
	} 
	long get_ms_time(){
		return cl.get_ms_time();
	}
	int test_cilin(){
		return test();
	}

}  