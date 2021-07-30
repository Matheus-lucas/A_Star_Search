#include <algorithm>  
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <iomanip>
#include <time.h>

using std::cout;
using std::setw;
using std::ifstream;
using std::istringstream;
using std::sort;
using std::string;
using std::vector;
using std::abs;
using std::find;

#define max_it  500000

// Estrutura dos nós
struct No
{
    No(){}
    No(int a, int b) : i(a), j(b){}
    No(int a, int b, float c) : i(a), j(b), custo(c){} 
    No(int a, int b, float c, No *n): i(a), j(b),custo(c),anterior(n){}

    int i;
    int j;
    float custo;
    No *anterior;

};

// Compara se é a mesma posição
bool operator==(No a, No b){
    return a.i == b.i && a.j == b.j;
}

// Vizinhos do nó(norte, oeste, sul, leste)
const vector<vector<int>> delta{{-1, 0}, {0, -1}, {1, 0}, {0, 1}};

vector<vector<int>> LeMapa(string nome_arquivo) {
  ifstream arquivo (nome_arquivo);
  vector<vector<int>> mapa{};
  if (arquivo.is_open()) {
    string linha_str;
    while (getline(arquivo, linha_str)) {
        istringstream linha(linha_str);
        vector<int> linha_int{};
        int no;
        while(linha >> no){
            linha.ignore(); // para ignorar a virgula
            linha_int.push_back(no);
        }
      mapa.push_back(linha_int);
    }
  }
  return mapa;
}

char ConverterParaSimbolo(int e)
{
    switch(e){
        case 1: return 	(char)254u;
        case 2: return 'P';
        case 3: return 'D';
        case 4: return '-';
        default: return 'x';;
    }
}

void ImprimirMapa(const vector<vector<int>> mapa) 
{
  for (auto linha : mapa) {
    for (auto elemento : linha) {
      cout <<  ConverterParaSimbolo(elemento) << "  ";
    }
    cout << "\n";
  }
}

bool VerificarLimites(int i, int j, vector<vector<int>> &mapa)
{
    bool limite_i = i>=0 and i<mapa.size();
    bool limite_j = j>=0 and j<mapa[0].size();
    return limite_i and limite_j;
}

bool CelulaVazia(int i, int j, vector<vector<int>> &mapa){
    return mapa[i][j] == 0;
}

vector<No> BuscarVizinhos(No no, vector<vector<int>> &mapa)
{
    vector<No> vizinhos{};
    for(auto posicao : delta){
        int novo_i = no.i + posicao[0];
        int novo_j = no.j + posicao[1];
        if(VerificarLimites(novo_i, novo_j,mapa) and CelulaVazia(novo_i,novo_j,mapa)){
            vizinhos.push_back(No{novo_i,novo_j});
        } 
    }
    return vizinhos;
}

float Heuristica(No atual, No destino){
    return abs(atual.i - destino.i) + abs(destino.j - atual.j);
}

bool CompararCusto(No a, No b){
    return a.custo > b.custo;
}

void MarcarCaminho(vector<vector<int>> &mapa, vector<No> &caminho, No inicio, No destino){
    No no = caminho.back();
    while(no.anterior != nullptr){
        mapa[no.i][no.j] = 4;
        no = *no.anterior;
    }
    mapa[inicio.i][inicio.j] = 2;
    mapa[destino.i][destino.j] = 3;
}


/* Realiza o a_star search
    tipo:
    0: A star normal
    1: A star search ponderado com w=0.9(melhor resultado nos testes) p/ f = g+w*h
    2: A star search ponderado com w=0.9(melhor resultado nos testes) p/ f = (1-w)*g+w*h
    3: A star search ponderado com w=0.9 puWU
    4: A star search ponderado com w=0.9 puWD
*/
void a_star_search(vector<vector<int>> &mapa, No inicio, No destino, int tipo)
{
    

    No inicio_ass = inicio;
    No destino_ass = destino;
    vector<vector<int>> mapa_ass = mapa;

    inicio_ass.custo = Heuristica(inicio_ass,destino_ass);
    inicio_ass.anterior = nullptr;

    No atual;
    vector<No> fronteira{};
    vector<No> caminho{};
    int custo_g = 0;
    int w=0.9;

    //cout << "\n============Mapa Original=========\n\n";
    //ImprimirMapa(mapa_ass);

    string metodo;

    fronteira.push_back(inicio_ass);
    int count=0;
    while(!fronteira.empty())
    {
        atual = fronteira.back();
        fronteira.pop_back();
        caminho.push_back(atual);

        if((atual == destino_ass) or count==max_it) break;

        auto vizinhos = BuscarVizinhos(atual, mapa_ass);
        custo_g++;
        for(auto& vizinho : vizinhos){
            float h = Heuristica(atual, destino_ass);
            float custo = 0.0;

            
            switch (tipo)
            {
                
                default : 
                    custo = custo_g+h;
                    metodo = "Normal";
                    break;

                case 1: 
                    custo = custo_g + w*Heuristica(vizinho,destino_ass);
                    metodo = "Pesos 1";
                    break;
                    

                case 2: 
                    custo = (1-w)*custo_g + w*Heuristica(vizinho,destino_ass);
                    metodo = "Pesos 2";
                    break;

                case 3: 
                    custo = custo_g < (2*w - 1) *h ? custo_g / (2*w - 1) +h: custo_g + h / w;
                    metodo = "puWU";
                    break;

                case 4: 
                    custo = custo_g < h ? custo_g +h: (custo_g + h*(2*w-1)) / w;
                    metodo = "puWD";
                    break;
            }
            
            auto it = find(caminho.begin(), caminho.end(),vizinho);
            if (it == caminho.end() or custo < it->custo){
                vizinho.custo = custo;
                vizinho.anterior = new No{atual.i,atual.j,atual.custo,atual.anterior};
                if(it != caminho.end()) caminho.erase(it);
                fronteira.push_back(vizinho);
            }
        }
        sort(fronteira.begin(), fronteira.end(),CompararCusto);
        count++;
    }
    
    cout << "\n\n==========Caminho "<<metodo<<"==========\n\n";
    MarcarCaminho(mapa_ass,caminho,inicio_ass,destino_ass);
    ImprimirMapa(mapa_ass);
    cout<<"\nNumero células percorridas puWD: "<<count<<"\n";
}


int main()
{

    time_t start, end;

    No inicio{0, 0};
    

    auto mapa = LeMapa("D:\\TCC\\src\\mapas\\mapas_filtrados\\mapa_11x18.csv");
    
    if (mapa.size()==0)
    {
        cout<<"Arquivo inválido"<<"\n";
        return 0;
    }

    No destino{(int)mapa.size()-1,(int)mapa[0].size()-1,0.0};
    cout << "\n============Mapa Original=========\n\n";
    ImprimirMapa(mapa);

    if(!CelulaVazia(inicio.i, inicio.j, mapa) or !VerificarLimites(inicio.i,inicio.j, mapa))
    {
        cout<<"\nPartida Inválida";
        return 0;
    }


    if(!CelulaVazia(destino.i, destino.j, mapa) or !VerificarLimites(destino.i, destino.j, mapa))
    {
        cout<<"\nDestino Inválido";
        return 0;
    }

    /*time(&start);
    a_star_search(mapa, inicio, destino, 0);
    time(&end);
    cout<<"\nTempo de Execucao: "<<double(end-start)<<std::setprecision(5)<<" s\n";
    */
    /*time(&start);
    a_star_search(mapa, inicio, destino, 1);
    time(&end);
    cout<<"\nTempo de Execucao com pesos 1: "<<double(end-start)<<std::setprecision(5)<<" s\n";

    time(&start);
    a_star_search(mapa, inicio, destino,2);
    time(&end);
    cout<<"\nTempo de Execucao com pesos 2: "<<double(end-start)<<std::setprecision(5)<<" s\n";
    */
    time(&start);
    a_star_search(mapa, inicio, destino,3);
    time(&end); 
    cout<<"\nTempo de Execucao com puWu: "<<double(end-start)<<std::setprecision(5)<<" s\n";

    time(&start);
    a_star_search(mapa, inicio, destino,4);
    time(&end);
    cout<<"\nTempo de Execucao com puWD: "<<double(end-start)<<std::setprecision(5)<<" s\n";

return 0;
}