#include <iostream>
#include <typeinfo>
 #include <string>
using namespace std;
  
int main(int argc, char *argv[])
{
    cout << "You have entered " << argc
         << " arguments:" << "\n";
    int nx = atoi(argv[1]), ny = atoi(argv[2]), i, j, p, T = atoi(argv[3]), t;
    int nx1 = atoi(argv[4]), nx2 = atoi(argv[5]), ny1 = atoi(argv[6]), ny2 = atoi(argv[7]), ny3 = atoi(argv[8]);
    long double ax = atof(argv[9]), bx = atof(argv[10]), ay = atof(argv[11]), by = atof(argv[12]);
    long double **un;
    long double **un1;
    long double **un2;
    long double **unpred;
    int **g;
    long double **rn;
    long double hx = (bx - ax) / nx, hy = (by - ay) / ny,                                                               //// шаги сетки по х и у, высчитывается по известным размерам области и количеству узлов
        eps = atof(argv[13]), nrn, nrn0, ro1 = atof(argv[14]), ro2 = atof(argv[15]), mu1 = atof(argv[16]) * 1e-5, mu2 = atof(argv[17]) * 1e-3, tau, pn12, D = atof(argv[18]); ///// mu1, ro1 - вязкость и плотность воздуха, mu2, ro2 - вязкость и плотность воды, tau - шаг по времени, D - коэффициент диффузии
    // все что выше задается пользователем
    long double **pp, **tt, **nu, **rn0, **s;
    long double po, om, al, beta;

    long double scontotal, sconnow, conouttotal, conoutnow;

    long double ROb, Pa, Pb, Vvoz, Vin, Mass, Mdelta, Sq = atof(argv[19]);
    cout << nx << " " << eps;
    return 0;
    // int nx = 500, ny = 108, i, j, p, T = 4001, t;         //// nx, ny - количество узлов по х и у, T - количество шагов по времени
    // int nx1 = 89, nx2 = 93, ny1 = 14, ny2 = 28, ny3 = 28; //// nx1, nx2, ny1 - координаты перегородки, ny2 - координата уровня воды в волнопродукторе, ny3 - координата уровня воды в лотке
    // long double ax = 0.0, bx = 10.0, ay = 0.0, by = 2.16; //// размеры области, здесь (ах, ау) - координаты левой нижней точки, (bх, bу) - координаты правой верхней точки,

}