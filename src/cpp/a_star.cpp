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

string ConverterParaSimbolo(int e)
{
    switch(e){
        case 1: return "1";
        case 2: return "P";
        case 3: return "D";
        case 4: return "-";
        default: return "0";;
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

int main(){

    time_t start, end;

	time(&start);

    No inicio{0, 0};
    No destino{38, 35, 0};

    inicio.custo = Heuristica(inicio,destino);
    inicio.anterior = nullptr;

    No atual;
    vector<No> fronteira{};
    vector<No> caminho{};
    int custo_g = 0;

    auto mapa = LeMapa("D:\\TCC\\Codigos\\mapas\\mapas_filtrados\\mapa_39x36.csv");
    //cout << "\n============Mapa Original=========\n\n";
    //ImprimirMapa(mapa);
    
    if(!CelulaVazia(inicio.i, inicio.j, mapa))
    {
        cout<<"\nPartida Bloqueada";
        return 0;
    }


    if(!CelulaVazia(destino.i, destino.j, mapa))
    {
        cout<<"\nDestino Bloqueado";
        return 0;
    }

    fronteira.push_back(inicio);
    int count=0;
    while(!fronteira.empty())
    {
        atual = fronteira.back();
        fronteira.pop_back();
        caminho.push_back(atual);

        if((atual == destino) or count==50000) break;

        auto vizinhos = BuscarVizinhos(atual, mapa);
        custo_g++;
        for(auto& vizinho : vizinhos){
            float custo = custo_g + Heuristica(vizinho,destino);
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
    

    //cout << "\n\n==========Caminho==========\n\n";
    //MarcarCaminho(mapa,caminho,inicio,destino);
    //ImprimirMapa(mapa);
    time(&end);
    cout<<"\nNumero de Buscas: "<<count<<"\n";
    cout<<"\nTempo de Execucao: "<<double(end-start)<<std::setprecision(5)<<"\n";
}