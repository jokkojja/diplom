#include <stdio.h>
#include <math.h>
#include <iostream>
#include <string>
#include <cstdio>

using namespace std;
void progonka(long double *A, long double *B, long double *C, long double *F, long double c0, long double d0, long double cn, long double dn, long double *x, int n1, int n2)
{
    FILE *ff;
    int i, j;
    long double *c, *d;
    c = new long double[n2 - n1];
    d = new long double[n2 - n1];

    c[0] = c0;
    d[0] = d0;

    for (i = n1 + 1; i < n2 - 1; i++)
    {

        c[i - n1] = -A[i] / (B[i] + C[i] * c[i - n1 - 1]);
        d[i - n1] = (F[i] - C[i] * d[i - n1 - 1]) / (B[i] + C[i] * c[i - n1 - 1]);
    }

    x[n2 - 1] = (dn + cn * d[n2 - n1 - 2]) / (1 - cn * c[n2 - n1 - 2]); //(c[n]*d[n-1]+d[n])/(1-c[n]*c[n-1]);

    for (i = n2 - 2; i >= n1; i--)
    {
        x[i] = c[i - n1] * x[i + 1] + d[i - n1];
    }
    delete[] c;
    delete[] d;
}

long double getf(int j, int ny)
{
    if (j < ny / 3)
        return 0;

    if (j < 2 * ny / 3)
        return -9.81;

    return 0;
}

long double dob_laplRo(long double **f, int nx, int ny, int i, int j, long double hx, long double hy)
{

    if (j < ny / 3)
    {

        long double a, b;

        a = (f[i + 1][j] - f[i][j] - f[i - 1][j] + f[i - 2][j]) / (2.0 * hx * hx);

        b = ((f[i][j + 1] - 2.0 * f[i][j] + f[i][j - 1]) / (hy * hy) + (f[i - 1][j + 1] - 2.0 * f[i - 1][j] + f[i - 1][j - 1]) / (hy * hy)) / 2.0;

        return a + b;
    }
    else if (j < 2 * ny / 3)
    {

        long double a, b;

        a = ((f[i + 1][j - ny / 3] - 2.0 * f[i][j - ny / 3] + f[i - 1][j - ny / 3]) / (hx * hx) + (f[i + 1][j - ny / 3 - 1] - 2.0 * f[i][j - ny / 3 - 1] + f[i - 1][j - ny / 3 - 1]) / (hx * hx)) / 2.0;
        b = (f[i][j - ny / 3 + 1] - f[i][j - ny / 3] - f[i][j - ny / 3 - 1] + f[i][j - ny / 3 - 2]) / (2.0 * hy * hy);

        return a + b;
    }
    else
    {

        return 0;
    }
}

long double div(long double **f, int **g, int nx, int ny, int i, int j, long double hx, long double hy)
{

    if (j < ny / 3)
    {

        long double a;

        a = (f[i][j + 2 * ny / 3] - f[i - 1][j + 2 * ny / 3]) / (hx);

        return a;
    }
    else if (j < 2 * ny / 3)
    {

        long double a;

        a = (f[i][j + ny / 3] - f[i][j + ny / 3 - 1]) / (hy);

        return a;
    }
    else
    {

        long double a, b;

        a = (f[i + 1][j - 2 * ny / 3] - f[i][j - 2 * ny / 3]) / (hx);
        b = (f[i][j - ny / 3 + 1] - f[i][j - ny / 3]) / (hy);

        return a + b;
    }
}

long double Pressoper(long double **f, long double **Ro, int nx, int ny, int i, int j, long double hx, long double hy)
{

    if (j < ny / 3)
    {

        long double a, b;

        a = 2.0 * ((f[i + 1][j] - f[i][j]) / (Ro[i + 1][j] + Ro[i][j]) - (f[i][j] - f[i - 1][j]) / (Ro[i][j] + Ro[i - 1][j])) / (hx * hx);

        b = 2.0 * ((f[i][j + 1] - f[i][j]) / (Ro[i][j + 1] + Ro[i][j]) - (f[i][j] - f[i][j - 1]) / (Ro[i][j] + Ro[i][j - 1])) / (hy * hy);

        return a + b;
    }
    else if (j < 2 * ny / 3)
    {

        return 0;
    }
    else
    {
        long double a, b;

        a = 2.0 * ((f[i + 1][j] - f[i][j]) / (Ro[i + 1][j - 2 * ny / 3] + Ro[i][j - 2 * ny / 3]) - (f[i][j] - f[i - 1][j]) / (Ro[i][j - 2 * ny / 3] + Ro[i - 1][j - 2 * ny / 3])) / (hx * hx);

        b = 2.0 * ((f[i][j + 1] - f[i][j]) / (Ro[i][j - 2 * ny / 3 + 1] + Ro[i][j - 2 * ny / 3]) - (f[i][j] - f[i][j - 1]) / (Ro[i][j - 2 * ny / 3] + Ro[i][j - 2 * ny / 3 - 1])) / (hy * hy);

        return a + b;
    }
}

long double scal2(long double **f1, long double **f2, int nx, int ny, long double hx, long double hy)
{
    int i, j;
    long double f = 0;
    for (i = 0; i < nx; i++)
    {
        for (j = 0; j < ny; j++)
        {
            f = f + f1[i][j] * f2[i][j];
        }
    }
    return f * hx * hy;
}

void exptc(long double **un, long double **cc, int **g, int nx, int ny, long double hx, long double hy, int t, FILE *ff)
{
    int i, j;

    long double a, b, d, e;

    fprintf(ff, "ZONE T=\"ZONE %d\",I=%d,J=%d,F=POINT\n", t, nx - 1, ny - 1);

    for (j = 1; j < ny; j++)
        for (i = 1; i < nx; i++)
        {
            a = (un[i][j] + un[i][j - 1]) / 2.0;

            b = (un[i][j + ny] + un[i - 1][j + ny]) / 2.0;

            d = (un[i][j + 2 * ny] + un[i - 1][j + 2 * ny] + un[i][j + 2 * ny - 1] + un[i - 1][j + 2 * ny - 1]) / 4.0;

            e = (cc[i][j] + cc[i - 1][j] + cc[i][j - 1] + cc[i - 1][j - 1]) / 4.0;

            fprintf(ff, "%e,%e,%e,%e,%e,%e\n", (double)((i - 1) * hx), (double)((j - 1) * hy), (double)a, (double)b, (double)d, (double)e);
        }
}

void expmask(int **g, int **gcon, int nx, int ny, long double hx, long double hy, int t)
{
    int i, j;

    char c[20];
    sprintf(c, "data/mask%d.dat", t);

    FILE *ff;
    ff = fopen(c, "w");
    fprintf(ff, "TITLE = Test\n");
    fprintf(ff, "VARIABLES = X,Y,U,V,P,C\n");

    fprintf(ff, "ZONE T=Test,I=%d,J=%d,F=POINT\n", nx, ny);

    for (j = 0; j < ny; j++)
        for (i = 0; i < nx; i++)
        {

            fprintf(ff, "%e,%e,%d,%d,%d,%d\n", (double)((i - 1) * hx), (double)((j - 1) * hy), g[i][j], g[i][j + ny], g[i][j + 2 * ny], gcon[i][j]);
        }

    fclose(ff);
}

int main(int argc, char *argv[])

{   char concetrFileName[100];
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
        eps = atof(argv[13]), nrn, nrn0, ro1 = atof(argv[14]), ro2 = atof(argv[15]), mu1 = atof(argv[16]) * 1e-5, mu2 = atof(argv[17]) * 1e-3, tau = atof(argv[18]), pn12, D = atof(argv[19]); ///// mu1, ro1 - вязкость и плотность воздуха, mu2, ro2 - вязкость и плотность воды, tau - шаг по времени, D - коэффициент диффузии
    // // все что выше задается пользователем
    long double **pp, **tt, **nu, **rn0, **s;
    long double po, om, al, beta;

    long double scontotal, sconnow, conouttotal, conoutnow;

    long double ROb, Pa, Pb, Vvoz, Vin, Mass, Mdelta, Sq = atof(argv[20]);
    string calculationId = argv[21];
    long double y1, y2, y0, C0, C1, C2;

    long double **Mu;
    long double **Ro;

    long double **pn;
    long double **pn1;

    long double **con;
    long double **con1;
    long double **con2;
    int **gcon;
    int cstart, cend;

    long double c0, cn, d0, dn;

    long double u, v, mup, mum, ro;

    long double *A, *B, *C, *F, *x;

    int ii, jj, kk;

    nx = nx + 2;
    ax = ax - hx;
    bx = bx + hx;

    ny = ny + 2;
    ay = ay - hy;
    by = by + hy;

    A = new long double[nx];
    B = new long double[nx];
    C = new long double[nx];
    F = new long double[nx];
    x = new long double[nx];

    un = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        un[i] = new long double[3 * ny];
    }

    un1 = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        un1[i] = new long double[3 * ny];
    }

    un2 = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        un2[i] = new long double[3 * ny];
    }

    unpred = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        unpred[i] = new long double[3 * ny];
    }

    g = new int *[nx];
    for (i = 0; i < nx; i++)
    {
        g[i] = new int[3 * ny];
    }

    rn = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        rn[i] = new long double[ny];
    }

    pn = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        pn[i] = new long double[ny];
    }

    pn1 = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        pn1[i] = new long double[ny];
    }

    gcon = new int *[nx];
    for (i = 0; i < nx; i++)
    {
        gcon[i] = new int[ny];
    }

    con = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        con[i] = new long double[ny];
    }

    con1 = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        con1[i] = new long double[ny];
    }

    con2 = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        con2[i] = new long double[ny];
    }

    Mu = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        Mu[i] = new long double[ny];
    }

    Ro = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        Ro[i] = new long double[ny];
    }

    rn0 = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        rn0[i] = new long double[ny];
    }

    pp = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        pp[i] = new long double[ny];
    }

    tt = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        tt[i] = new long double[ny];
    }

    nu = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        nu[i] = new long double[ny];
    }

    s = new long double *[nx];
    for (i = 0; i < nx; i++)
    {
        s[i] = new long double[ny];
    }

    for (i = 0; i < nx; i++)
    {
        for (j = 0; j < 3 * ny; j++)
        {

            un[i][j] = 0;
            un1[i][j] = 0;
            un2[i][j] = 0;
            unpred[i][j] = 0;
            g[i][j] = 1;
        }
    }

    for (i = 0; i < nx; i++)
    {
        for (j = 0; j < ny; j++)
        {
            pn[i][j] = 0;
            pn1[i][j] = 0;
            rn[i][j] = 0;

            gcon[i][j] = 1;
            con[i][j] = 0;
            con1[i][j] = 0;
            con2[i][j] = 0;

            tt[i][j] = 0;
            pp[i][j] = 0;
            rn0[i][j] = 0;
            s[i][j] = 0;
            nu[i][j] = 0;
        }
    }

    Pa = 101325;
    Pb = Pa;

    for (i = 0; i <= nx1; i++)
    {

        un[i][3 * ny - 1] = Pb;
        un1[i][3 * ny - 1] = Pb;
        un2[i][3 * ny - 1] = Pb;
        unpred[i][3 * ny - 1] = Pb;
    }

    for (i = nx2; i < nx; i++)
    {

        un[i][3 * ny - 1] = Pa;
        un1[i][3 * ny - 1] = Pa;
        un2[i][3 * ny - 1] = Pa;
        unpred[i][3 * ny - 1] = Pa;
    }

    // ///////u

    // /////????-?????
    for (j = 0; j < ny; j++)
    {
        g[0][j] = 0;
        g[1][j] = 0;
        // 2;
        g[nx - 1][j] = 0;
        // 3;
    }

    // ////??????
    for (i = 2; i < nx - 1; i++)
    {
        g[i][0] = 11;
        g[i][ny - 1] = 12;
    }

    for (i = nx1; i <= nx2 + 1; i++)
        for (j = ny1 + 1; j < ny; j++)
        {
            g[i][j] = 0;
        }

    for (i = nx1 + 1; i < nx2 + 1; i++)
    {
        g[i][ny1 + 1] = 12;
    }

    ///////v
    ////??????
    for (i = 0; i < nx; i++)
    {
        g[i][ny] = 0;
        g[i][ny + 1] = 0;
        g[i][2 * ny - 1] = 4;
    }

    /////????-?????
    for (j = ny + 2; j < 2 * ny - 1; j++)
    {
        g[0][j] = 21;
        g[nx - 1][j] = 22;
    }

    for (i = nx1; i <= nx2; i++)
        for (j = ny + ny1 + 1; j < 2 * ny; j++)
        {
            g[i][j] = 0;
        }

    for (j = ny + ny1 + 2; j < 2 * ny; j++)
    {
        g[nx1][j] = 22;
    }

    for (j = ny + ny1 + 2; j < 2 * ny; j++)
    {
        g[nx2][j] = 21;
    }

    ///////p
    ////??????
    for (i = 0; i < nx; i++)
    {
        g[i][2 * ny] = 2;
        g[i][3 * ny - 1] = 0;
    }

    /////????-?????
    for (j = 2 * ny; j < 3 * ny; j++)
    {
        g[0][j] = 6;
        g[nx - 1][j] = 7;
    }

    for (i = nx1; i <= nx2; i++)
        for (j = 2 * ny + ny1 + 1; j < 3 * ny; j++)
        {
            g[i][j] = 0;
        }

    for (i = nx1 + 1; i < nx2; i++)
    {
        g[i][2 * ny + ny1 + 1] = 3;
    }

    for (j = 2 * ny + ny1 + 1; j < 3 * ny; j++)
    {
        g[nx1][j] = 7;
    }

    for (j = 2 * ny + ny1 + 1; j < 3 * ny; j++)
    {
        g[nx2][j] = 6;
    }

    g[nx1][2 * ny + ny1 + 1] = 13;
    g[nx2][2 * ny + ny1 + 1] = 16;

    // ///////c
    // ////?????
    for (i = 0; i < nx; i++)
        for (j = 0; j <= ny2; j++)
        {
            con[i][j] = 1.0;
        }

    for (i = 0; i <= nx1; i++)
        for (j = 0; j <= ny3; j++)
        {
            con[i][j] = 1.0;
        }

    for (i = nx1 + 1; i < nx2; i++)
        for (j = ny1 + 2; j < ny; j++)
        {
            con[i][j] = 1.0;
        }
                        
    // // ///////gcon

    // // ////??????
    for (i = 0; i < nx; i++)
    {
        gcon[i][0] = -1;
        gcon[i][ny - 1] = -2;
    }

    for (j = 0; j < ny; j++)
    {
        gcon[0][j] = -1;
        gcon[nx - 1][j] = -1;
    }

    for (i = nx1; i <= nx2; i++)
        for (j = ny1 + 1; j < ny; j++)
        {
            gcon[i][j] = 0;
        }

    // // ///////////////////////////////////////////////////////////

    expmask(g, gcon, nx, ny, hx, hy, 0);

    FILE *ff;
    sprintf(concetrFileName, "data/concetr_%s.dat", calculationId.c_str());
    ff = fopen(concetrFileName, "w");
    fprintf(ff, "TITLE = Test\n");
    fprintf(ff, "VARIABLES = X,Y,U,V,P,C\n");

    t = 1;
    exptc(un,con,g,nx,ny,hx,hy,0,ff);
    fclose(ff);

    for (i = 0; i < nx; i++)
    {
        for (j = 0; j < ny; j++)
        {

            Mu[i][j] = mu1 * mu2 / (con[i][j] * mu1 + (1.0 - con[i][j]) * mu2);
            Ro[i][j] = (1.0 - con[i][j]) * ro1 + con[i][j] * ro2;
        }
    }

    for (i = 0; i < nx; i++)
    {
        for (j = 0; j < ny; j++)
        {
            un1[i][j] = un[i][j];
            un1[i][j + ny] = un[i][j + ny];
            un1[i][j + 2 * ny] = un[i][j + 2 * ny];

            un2[i][j] = un[i][j];
            un2[i][j + ny] = un[i][j + ny];
            un2[i][j + 2 * ny] = un[i][j + 2 * ny];

            unpred[i][j] = un[i][j];
            unpred[i][j + ny] = un[i][j + ny];
            unpred[i][j + 2 * ny] = un[i][j + 2 * ny];
        }
    }
    for (i = 0; i < nx; i++)
    {

        unpred[i][3 * ny - 2] = unpred[i][3 * ny - 1] + hy * 9.81 * Ro[i][ny - 2] / 2.0;
    }

    for (i = 0; i < nx; i++)
    {
        for (j = ny - 3; j >= 1; j--)
        {
            unpred[i][j + 2 * ny] = unpred[i][j + 2 * ny + 1] + hy * 9.81 * (Ro[i][j + 1] + Ro[i][j]) / 2.0;
        }
    }

    for (i = 0; i < nx; i++)
    {

        unpred[i][2 * ny] = unpred[i][2 * ny + 1];
    }

    for (i = nx1; i <= nx2; i++)
    {
        for (j = 0; j <= ny1; j++)
        {
            unpred[i][j + 2 * ny] = unpred[nx2 + 2][j + 2 * ny];
        }
    }

    for (i = nx1 + 1; i < nx2; i++)
    {
        for (j = ny1; j < ny; j++)
        {
            unpred[i][j + 2 * ny] = Pa;
        }
    }

    ff = fopen(concetrFileName, "a");
    exptc(unpred, con, g, nx, ny, hx, hy, 0, ff);
    fclose(ff);
    //выше работает
    // tau = 1e-3;

    ff = fopen("data/press2d120.txt", "a");
    fprintf(ff, "%d %e\n", t, (double)Pb);
    fclose(ff);

    while (t < T)
    {

        //////////////////////////////////////////////////////////////////////////////////////
        //////////////// ???? ?????????

        Pb = Pa + 1000 * sin(M_PI * (double)t / 1000.0);

        for (i = 0; i <= nx1; i++)
        {

            un[i][3 * ny - 1] = Pb;
            un1[i][3 * ny - 1] = Pb;
            un2[i][3 * ny - 1] = Pb;
            unpred[i][3 * ny - 1] = Pb;
        }

        ff = fopen("data/press2d120.txt", "a");
        fprintf(ff, "%d %e\n", t, (double)Pb);
        fclose(ff);

        //////////////// I

        cstart = -1;
        cend = 1;

        ///// ??? ?????????
        //////////// ?? x

        for (j = 1; j < ny; j++)
            for (i = 1; i < nx; i++)
            {

                if (g[i][j] == 1 && cstart == -1)
                {

                    cstart = i - 1;
                    cend = -1;
                    if (g[i - 1][j] == 0)
                    {
                        c0 = 0;
                        d0 = 0;
                    }
                    else
                    {
                        c0 = -1;
                        d0 = 0;
                    }
                }
                if (g[i][j] != 1 && cend == -1)
                {

                    cend = i + 1;

                    // c0=1;
                    // d0=0;
                    // cn=1;
                    // dn=0;

                    if (g[i][j] == 0)
                    {
                        cn = 0;
                        dn = 0;
                    }
                    else
                    {
                        cn = -1;
                        dn = 0;
                    }

                    /// A - ???? ????? i+1
                    /// B - ???? ????? i
                    /// C - ???? ????? i-1
                    /// F - ?????? ?????
                    /// ???????? ???: A+B+C=F

                    for (p = cstart + 1; p < cend - 1; p++)
                    {

                        ro = (Ro[p][j] + Ro[p - 1][j]) / 2.0;

                        A[p] = tau * ((un[p][j] - fabsl(un[p][j])) / (2.0 * hx) - 2.0 * Mu[p][j] / (ro * hx * hx));

                        B[p] = 2.0 + tau * (fabsl(un[p][j]) / (hx) + 2.0 * (Mu[p][j] + Mu[p - 1][j]) / (hx * hx * ro));

                        C[p] = tau * (-(un[p][j] + fabsl(un[p][j])) / (2.0 * hx) - 2.0 * Mu[p - 1][j] / (ro * hx * hx));

                        F[p] = 2.0 * un[p][j];

                        if (fabsl(B[p]) < (fabsl(A[p]) + fabsl(C[p])))
                        {

                            ff = fopen("data/progonka2d120.txt", "a");
                            fprintf(ff, "ux %d %d %d %e %e %e\n", t, p, j, (double)fabsl(B[p]), (double)fabsl(A[p]), (double)fabsl(C[p]));
                            fprintf(ff, "A %e %e\n", (double)((un[p][j] - fabsl(un[p][j])) / (2.0 * hx)), (double)(2.0 * Mu[p][j] / (ro * hx * hx)));
                            fprintf(ff, "B %e %e %e\n", (double)(2.0 / tau), (double)(fabsl(un[p][j]) / (hx)), (double)(2.0 * (Mu[p][j] + Mu[p - 1][j]) / (hx * hx * ro)));
                            fprintf(ff, "C %e %e\n\n", (double)((un[p][j] + fabsl(un[p][j])) / (2.0 * hx)), (double)(2.0 * Mu[p - 1][j] / (ro * hx * hx)));

                            fclose(ff);
                        }
                    }

                    progonka(A, B, C, F, c0, d0, cn, dn, x, cstart, cend);

                    for (p = cstart; p < cend; p++)
                    {
                        un1[p][j] = x[p];
                    }

                    cstart = -1;
                }
            }

        for (i = 0; i < nx; i++)
            for (j = 0; j < ny; j++)
            {
                if (g[i][j] == 11)
                    un1[i][j] = -un1[i][j + 1];

                if (g[i][j] == 12)
                    un1[i][j] = -un1[i][j - 1];
            }

        for (j = 1; j < ny; j++)
            for (i = 1; i < nx; i++)
            {
                if (g[i][j + ny] == 1 && cstart == -1)
                {
                    cstart = i - 1;
                    cend = -1;
                    if (g[i - 1][j + ny] == 0)
                    {
                        c0 = 0;
                        d0 = 0;
                    }
                    else
                    {
                        c0 = -1;
                        d0 = 0;
                    }
                }
                if (g[i][j + ny] != 1 && cend == -1)
                {

                    cend = i + 1;

                    // c0=1;
                    // d0=0;
                    // cn=1;
                    // dn=0;

                    if (g[i][j + ny] == 0)
                    {
                        cn = 0;
                        dn = 0;
                    }
                    else
                    {
                        cn = -1;
                        dn = 0;
                    }

                    /// A - ???? ????? i+1
                    /// B - ???? ????? i
                    /// C - ???? ????? i-1
                    /// F - ?????? ?????
                    /// ???????? ???: A+B+C=F

                    for (p = cstart + 1; p < cend - 1; p++)
                    {

                        u = (un[p][j] + un[p + 1][j] + un[p][j - 1] + un[p + 1][j - 1]) / 4.0;

                        mup = (Mu[p][j] + Mu[p + 1][j] + Mu[p][j - 1] + Mu[p + 1][j - 1]) / 4.0;
                        mum = (Mu[p][j] + Mu[p - 1][j] + Mu[p][j - 1] + Mu[p - 1][j - 1]) / 4.0;

                        ro = (Ro[p][j] + Ro[p][j - 1]) / 2.0;

                        A[p] = tau * ((u - fabsl(u)) / (2.0 * hx) - mup / (ro * hx * hx));
                        B[p] = 2.0 + tau * (fabsl(u) / (hx) + (mup + mum) / (ro * hx * hx));
                        C[p] = tau * (-(u + fabsl(u)) / (2.0 * hx) - mum / (ro * hx * hx));

                        F[p] = 2.0 * un[p][j + ny];
                    }

                    progonka(A, B, C, F, c0, d0, cn, dn, x, cstart, cend);

                    for (p = cstart; p < cend; p++)
                    {
                        un1[p][j + ny] = x[p];
                    }

                    cstart = -1;
                }
            }

        for (i = 0; i < nx; i++)
        {

            un1[i][2 * ny - 1] = un1[i][2 * ny - 2];
        }

        ///////// ?? y

        for (i = 1; i < nx; i++)
            for (j = 1; j < ny; j++)
            {
                if (g[i][j] == 1 && cstart == -1)
                {
                    cstart = j - 1;
                    cend = -1;
                    if (g[i][j - 1] == 0)
                    {
                        c0 = 0;
                        d0 = 0;
                    }
                    else
                    {
                        c0 = -1;
                        d0 = 0;
                    }
                }
                if (g[i][j] != 1 && cend == -1)
                {
                    cend = j + 1;

                    if (g[i][j] == 0)
                    {
                        cn = 0;
                        dn = 0;
                    }
                    else
                    {
                        cn = -1;
                        dn = 0;
                    }

                    for (p = cstart + 1; p < cend - 1; p++)
                    {

                        v = (un[i][p + ny] + un[i][p + ny + 1] + un[i - 1][p + ny] + un[i - 1][p + ny + 1]) / 4.0;

                        mup = (Mu[i][p] + Mu[i][p + 1] + Mu[i - 1][p] + Mu[i - 1][p + 1]) / 4.0;
                        mum = (Mu[i][p] + Mu[i - 1][p] + Mu[i][p - 1] + Mu[i - 1][p - 1]) / 4.0;

                        ro = (Ro[i][p] + Ro[i - 1][p]) / 2.0;

                        A[p] = tau * ((v - fabsl(v)) / (2.0 * hy) - mup / (ro * hy * hy));
                        B[p] = 2.0 + tau * (fabsl(v) / (hy) + (mup + mum) / (ro * hy * hy));
                        C[p] = tau * (-(v + fabsl(v)) / (2.0 * hy) - mum / (ro * hy * hy));

                        F[p] = 2.0 * un1[i][p];
                    }

                    progonka(A, B, C, F, c0, d0, cn, dn, x, cstart, cend);

                    for (p = cstart; p < cend; p++)
                    {
                        un2[i][p] = x[p];
                    }

                    cstart = -1;
                }
            }

        for (i = 1; i < nx; i++)
            for (j = 1; j < ny; j++)
            {
                if (g[i][j + ny] == 1 && cstart == -1)
                {
                    cstart = j - 1;
                    cend = -1;
                    if (g[i][j + ny - 1] == 0)
                    {
                        c0 = 0;
                        d0 = 0;
                    }
                    else
                    {
                        c0 = -1;
                        d0 = 0;
                    }
                }
                if (g[i][j + ny] != 1 && cend == -1)
                {
                    cend = j + 1;

                    if (g[i][j + ny] == 0)
                    {
                        cn = 0;
                        dn = 0;
                    }
                    else
                    {
                        cn = -1;
                        dn = 0;
                    }

                    if (g[i][j + ny] == 4)
                    {
                        cn = 1;
                        dn = 0;
                    }

                    for (p = cstart + 1; p < cend - 1; p++)
                    {
                        ro = (Ro[i][p] + Ro[i][p - 1]) / 2.0;

                        A[p] = tau * ((un[i][p + ny] - fabsl(un[i][p + ny])) / (2.0 * hy) - 2.0 * Mu[i][p] / (ro * hy * hy));
                        B[p] = 2.0 + tau * (fabsl(un[i][p + ny]) / (hy) + 2.0 * (Mu[i][p] + Mu[i][p - 1]) / (ro * hy * hy));
                        C[p] = tau * (-(un[i][p + ny] + fabsl(un[i][p + ny])) / (2.0 * hy) - 2.0 * (Mu[i][p - 1]) / (ro * hy * hy));

                        F[p] = 2.0 * un1[i][p + ny];
                    }

                    progonka(A, B, C, F, c0, d0, cn, dn, x, cstart, cend);

                    for (p = cstart; p < cend; p++)
                    {
                        un2[i][p + ny] = x[p];
                    }

                    cstart = -1;
                }
            }

        for (i = 0; i < nx; i++)
            for (j = 0; j < ny; j++)
            {
                if (g[i][j + ny] == 21)
                    un2[i][j + ny] = -un2[i + 1][j + ny];

                if (g[i][j + ny] == 22)
                    un2[i][j + ny] = -un2[i - 1][j + ny];
            }

        /////////////////////// ���������

        for (i = 1; i < nx; i++)
            for (j = 1; j < ny; j++)
            {

                if (g[i][j] == 1)
                {

                    v = (un[i][j + ny] + un[i][j + ny + 1] + un[i - 1][j + ny] + un[i - 1][j + ny + 1]) / 4.0;

                    mup = (Mu[i][j] + Mu[i][j + 1] + Mu[i - 1][j] + Mu[i - 1][j + 1]) / 4.0;
                    mum = (Mu[i][j] + Mu[i - 1][j] + Mu[i][j - 1] + Mu[i - 1][j - 1]) / 4.0;

                    unpred[i][j] = un[i][j] + tau * (-(un[i][j] - fabsl(un[i][j])) * (un2[i + 1][j] - un2[i][j]) / (2.0 * hx) - (un[i][j] + fabsl(un[i][j])) * (un2[i][j] - un2[i - 1][j]) / (2.0 * hx) - (v - fabsl(v)) * (un2[i][j + 1] - un2[i][j]) / (2.0 * hy) - (v + fabsl(v)) * (un2[i][j] - un2[i][j - 1]) / (2.0 * hy) + 2.0 * (-D * dob_laplRo(Ro, nx, 3 * ny, i, j, hx, hy) * un2[i][j] + 2.0 * (Mu[i][j] * (un2[i + 1][j] - un2[i][j]) - Mu[i - 1][j] * (un2[i][j] - un2[i - 1][j])) / (hx * hx) + (mup * (un2[i][j + 1] - un2[i][j]) - mum * (un2[i][j] - un2[i][j - 1])) / (hy * hy) + (mup * (un2[i][j + ny + 1] - un2[i - 1][j + ny + 1]) - mum * (un2[i][j + ny] - un2[i - 1][j + ny])) / (hx * hy)) / (Ro[i][j] + Ro[i - 1][j]));
                }

                if (g[i][j + ny] == 1)
                {

                    u = (un[i][j] + un[i + 1][j] + un[i][j - 1] + un[i + 1][j - 1]) / 4.0;

                    mup = (Mu[i][j] + Mu[i + 1][j] + Mu[i][j - 1] + Mu[i + 1][j - 1]) / 4.0;
                    mum = (Mu[i][j] + Mu[i - 1][j] + Mu[i][j - 1] + Mu[i - 1][j - 1]) / 4.0;

                    unpred[i][j + ny] = un[i][j + ny] + tau * (-(u - fabsl(u)) * (un2[i + 1][j + ny] - un2[i][j + ny]) / (2.0 * hx) - (u + fabsl(u)) * (un2[i][j + ny] - un2[i - 1][j + ny]) / (2.0 * hx) - (un[i][j + ny] - fabsl(un[i][j + ny])) * (un2[i][j + ny + 1] - un2[i][j + ny]) / (2.0 * hy) - (un[i][j + ny] + fabsl(un[i][j + ny])) * (un2[i][j + ny] - un2[i][j + ny - 1]) / (2.0 * hy) + 2.0 * (-D * dob_laplRo(Ro, nx, 3 * ny, i, j + ny, hx, hy) * un2[i][j + ny] + (mup * (un2[i + 1][j + ny] - un2[i][j + ny]) - mum * (un2[i][j + ny] - un2[i - 1][j + ny])) / (hx * hx) + 2.0 * (Mu[i][j] * (un2[i][j + ny + 1] - un2[i][j + ny]) - Mu[i][j - 1] * (un2[i][j + ny] - un2[i][j + ny - 1])) / (hy * hy) + (mup * (un2[i + 1][j] - un2[i + 1][j - 1]) - mum * (un2[i][j] - un2[i][j - 1])) / (hx * hy)) / (Ro[i][j] + Ro[i][j - 1]) + getf(j + ny, 3 * ny));
                }
            }

        for (i = 0; i < nx; i++)
            for (j = 0; j < ny; j++)
            {
                if (g[i][j] == 11)
                    unpred[i][j] = -unpred[i][j + 1];

                if (g[i][j] == 12)
                    unpred[i][j] = -unpred[i][j - 1];

                if (g[i][j + ny] == 21)
                    unpred[i][j + ny] = -unpred[i + 1][j + ny];

                if (g[i][j + ny] == 22)
                    unpred[i][j + ny] = -unpred[i - 1][j + ny];

                if (g[i][j + ny] == 4)
                {
                    unpred[i][j + ny] = unpred[i][j + ny - 1];
                }
            }

        //////////////////////// II
        //////// bicgstab ??? ???????

        for (i = 0; i < nx; i++)
        {
            for (j = 0; j < ny; j++)
            {

                if (g[i][j + 2 * ny] == 1)
                    rn[i][j] = div(unpred, g, nx, 3 * ny, i, j + 2 * ny, hx, hy) / tau - Pressoper(unpred, Ro, nx, 3 * ny, i, j + 2 * ny, hx, hy);
                else
                    rn[i][j] = 0;

                rn0[i][j] = rn[i][j];
                pp[i][j] = rn[i][j];
            }
        }

        nrn = sqrt(scal2(rn, rn, nx, ny, hx, hy));

        nrn0 = nrn;

        po = scal2(rn, rn0, nx, ny, hx, hy);

        p = 1;

        while (nrn > eps)
        {

            for (i = 0; i < nx; i++)
            {
                for (j = 0; j < ny; j++)
                {

                    if (g[i][j + 2 * ny] == 1)
                    {
                        nu[i][j] = Pressoper(pp, Ro, nx, 3 * ny, i, j, hx, hy);
                    }
                }
            }

            al = po / scal2(nu, rn0, nx, ny, hx, hy);

            for (i = 0; i < nx; i++)
            {
                for (j = 0; j < ny; j++)
                {
                    if (g[i][j + 2 * ny] == 1)
                    {
                        s[i][j] = rn[i][j] - al * nu[i][j];
                    }
                }
            }

            for (i = 0; i < nx; i++)
            {
                for (j = 0; j < ny; j++)
                {

                    if (g[i][j + 2 * ny] == 1)
                    {
                        tt[i][j] = Pressoper(s, Ro, nx, 3 * ny, i, j, hx, hy);
                    }
                }
            }

            om = scal2(tt, s, nx, ny, hx, hy) / scal2(tt, tt, nx, ny, hx, hy);

            for (i = 0; i < nx; i++)
            {
                for (j = 0; j < ny; j++)
                {

                    if (g[i][j + 2 * ny] == 1)
                    {
                        unpred[i][j + 2 * ny] = unpred[i][j + 2 * ny] + al * pp[i][j] + om * s[i][j];
                        rn[i][j] = s[i][j] - om * tt[i][j];
                    }
                }
            }

            for (i = 0; i < nx; i++)
            {
                for (j = 0; j < ny; j++)
                {

                    if (g[i][j + 2 * ny] == 2)
                    {
                        unpred[i][j + 2 * ny] = unpred[i][j + 2 * ny + 1];
                    }

                    if (g[i][j + 2 * ny] == 3)
                    {
                        unpred[i][j + 2 * ny] = unpred[i][j + 2 * ny - 1];
                    }

                    if (g[i][j + 2 * ny] == 6)
                    {
                        unpred[i][j + 2 * ny] = unpred[i + 1][j + 2 * ny];
                    }

                    if (g[i][j + 2 * ny] == 7)
                    {
                        unpred[i][j + 2 * ny] = unpred[i - 1][j + 2 * ny];
                    }

                    if (g[i][j + 2 * ny] == 13)
                    {
                        unpred[i][j + 2 * ny] = (unpred[i][j + 2 * ny - 1] + unpred[i - 1][j + 2 * ny - 1] + unpred[i - 1][j + 2 * ny]) / 3.0;
                    }

                    if (g[i][j + 2 * ny] == 14)
                    {
                        unpred[i][j + 2 * ny] = (unpred[i][j + 2 * ny + 1] + unpred[i - 1][j + 2 * ny + 1] + unpred[i - 1][j + 2 * ny]) / 3.0;
                    }

                    if (g[i][j + 2 * ny] == 15)
                    {
                        unpred[i][j + 2 * ny] = (unpred[i][j + 2 * ny + 1] + unpred[i + 1][j + 2 * ny + 1] + unpred[i + 1][j + 2 * ny]) / 3.0;
                    }

                    if (g[i][j + 2 * ny] == 16)
                    {
                        unpred[i][j + 2 * ny] = (unpred[i][j + 2 * ny - 1] + unpred[i + 1][j + 2 * ny - 1] + unpred[i + 1][j + 2 * ny]) / 3.0;
                    }
                }
            }

            beta = po;

            po = scal2(rn, rn0, nx, ny, hx, hy);

            beta = po * al / (beta * om);

            for (i = 0; i < nx; i++)
            {
                for (j = 0; j < ny; j++)
                {

                    if (g[i][j + 2 * ny] == 1)
                    {
                        pp[i][j] = rn[i][j] + beta * (pp[i][j] - om * nu[i][j]);
                    }
                }
            }

            nrn = sqrt(scal2(rn, rn, nx, ny, hx, hy));

            if (p % 1000 == 0 || nrn < eps)
            {
                ff = fopen("data/pvr2d120.txt", "a");
                fprintf(ff, "%d %d %e %e\n", t, p, (double)nrn, (double)(nrn / nrn0));
                fclose(ff);
            }

            p++;
        }
        //////////// III

        for (i = 0; i < nx; i++)
        {
            for (j = 0; j < ny; j++)
            {

                if (g[i][j] == 1) //|| g[i][j][k]==2)
                    un[i][j] = unpred[i][j] - 2.0 * tau * div(unpred, g, nx, 3 * ny, i, j, hx, hy) / (Ro[i][j] + Ro[i - 1][j]);

                if (g[i][j + ny] == 1)
                    un[i][j + ny] = unpred[i][j + ny] - 2.0 * tau * div(unpred, g, nx, 3 * ny, i, j + ny, hx, hy) / (Ro[i][j] + Ro[i][j - 1]);

                un[i][j + 2 * ny] = unpred[i][j + 2 * ny];
            }
        }

        for (i = 0; i < nx; i++)
        {
            for (j = 0; j < ny; j++)
            {
                /////////////////u
                if (g[i][j] == 3)
                {
                    un[i][j] = un[i - 1][j];
                }

                if (g[i][j] == 2)
                {
                    un[i][j] = un[i + 1][j];
                }

                if (g[i][j] == 4)
                {
                    un[i][j] = un[i][j - 1];
                }
                ///////////////////////v

                if (g[i][j + ny] == 2)
                {
                    un[i][j + ny] = un[i + 1][j + ny];
                }

                if (g[i][j + ny] == 3)
                {
                    un[i][j + ny] = un[i - 1][j + ny];
                }

                if (g[i][j + ny] == 4)
                {
                    un[i][j + ny] = un[i][j + ny - 1];
                }
            }
        }

        for (i = 0; i < nx; i++)
        {
            for (j = 0; j < ny; j++)
            {

                ////u
                if (g[i][j] == 11)
                {
                    un[i][j] = -un[i][j + 1];
                }

                if (g[i][j] == 12)
                {
                    un[i][j] = -un[i][j - 1];
                }

                ////v

                if (g[i][j + ny] == 21)
                {
                    un[i][j + ny] = -un[i + 1][j + ny];
                }

                if (g[i][j + ny] == 22)
                {
                    un[i][j + ny] = -un[i - 1][j + ny];
                }
            }
        }

        //////////////////////////////////////////////////////////////////////////////////////

        //////////////////////////////////////////////////////////////////////////////////////
        //////////// ?????????-????????, ????? ?????????-?????????, 2 ??????? ???????? ?? ???????

        cstart = -1;
        cend = 1;

        ///// ??? ?????????
        //////////// ?? x

        for (j = 1; j < ny; j++)
            for (i = 1; i < nx; i++)
            {
                if (gcon[i][j] == 1 && cstart == -1)
                {
                    cstart = i - 1;
                    cend = -1;
                    if (gcon[i - 1][j] == -2)
                    {
                        c0 = 0;
                        d0 = 1;
                    }
                    else
                    {
                        c0 = 1;
                        d0 = 0;
                    }
                }
                if (gcon[i][j] != 1 && cend == -1)
                {

                    cend = i + 1;

                    // c0=1;
                    // d0=0;
                    // cn=1;
                    // dn=0;

                    if (gcon[i][j] == -2)
                    {
                        cn = 0;
                        dn = 1;
                    }
                    else
                    {
                        cn = 1;
                        dn = 0;
                    }

                    /// A - ???? ????? i+1
                    /// B - ???? ????? i
                    /// C - ???? ????? i-1
                    /// F - ?????? ?????
                    /// ???????? ???: A+B+C=F

                    for (p = cstart + 1; p < cend - 1; p++)
                    {
                        A[p] = (un[p][j] + un[p + 1][j] - fabsl(un[p][j] + un[p + 1][j])) / (4.0 * hx) - D / (hx * hx);
                        B[p] = 2.0 / tau + 2.0 * D / (hx * hx) + fabsl(un[p][j] + un[p + 1][j]) / (2.0 * hx);
                        C[p] = -(un[p][j] + un[p + 1][j] + fabsl(un[p][j] + un[p + 1][j])) / (4.0 * hx) - D / (hx * hx);

                        F[p] = 2.0 * con[p][j] / tau;
                    }

                    progonka(A, B, C, F, c0, d0, cn, dn, x, cstart, cend);

                    for (p = cstart; p < cend; p++)
                    {
                        con1[p][j] = x[p];
                    }

                    cstart = -1;
                }
            }

        for (i = 1; i < nx; i++)
            for (j = 1; j < ny; j++)
            {
                if (gcon[i][j] == 1 && cstart == -1)
                {
                    cstart = j - 1;
                    if (gcon[i - 1][j] != -2)
                        con1[i][cstart] = con1[i][cstart + 1];
                    cend = -1;
                }
                if (gcon[i][j] != 1 && cend == -1)
                {
                    cend = j + 1;
                    if (gcon[i][j] != -2)
                        con1[i][cend - 1] = con1[i][cend - 2];
                    cstart = -1;
                }
            }

        ///////// ?? y

        for (i = 1; i < nx; i++)
            for (j = 1; j < ny; j++)
            {
                if (gcon[i][j] == 1 && cstart == -1)
                {
                    cstart = j - 1;
                    cend = -1;
                    if (gcon[i][j - 1] == -2)
                    {
                        c0 = 0;
                        d0 = 1;
                    }
                    else
                    {
                        c0 = 1;
                        d0 = 0;
                    }
                }
                if (gcon[i][j] != 1 && cend == -1)
                {
                    cend = j + 1;

                    if (gcon[i][j] == -2)
                    {
                        cn = 0;
                        dn = 0;
                    }
                    else
                    {
                        cn = 1;
                        dn = 0;
                    }

                    for (p = cstart + 1; p < cend - 1; p++)
                    {
                        A[p] = (un[i][p + ny] + un[i][p + ny + 1] - fabsl(un[i][p + ny] + un[i][p + ny + 1])) / (4.0 * hy) - D / (hy * hy);
                        B[p] = 2.0 / tau + 2.0 * D / (hy * hy) + fabsl(un[i][p + ny] + un[i][p + ny + 1]) / (2.0 * hy);
                        C[p] = -(un[i][p + ny] + un[i][p + ny + 1] + fabsl(un[i][p + ny] + un[i][p + ny + 1])) / (4.0 * hy) - D / (hy * hy);

                        F[p] = 2.0 * con1[i][p] / tau;
                    }

                    progonka(A, B, C, F, c0, d0, cn, dn, x, cstart, cend);

                    for (p = cstart; p < cend; p++)
                    {
                        con2[i][p] = x[p];
                    }

                    cstart = -1;
                }
            }

        for (j = 1; j < ny; j++)
            for (i = 1; i < nx; i++)
            {
                if (gcon[i][j] == 1 && cstart == -1)
                {
                    cstart = i - 1;
                    if (gcon[i - 1][j] != -2)
                        con2[cstart][j] = con2[cstart + 1][j];
                    cend = -1;
                }
                if (gcon[i][j] != 1 && cend == -1)
                {
                    cend = i + 1;
                    if (gcon[i][j] != -2)
                        con2[cend - 1][j] = con2[cend - 2][j];
                    cstart = -1;
                }
            }

        /////// ??? ?????????

        for (i = 1; i < nx; i++)
            for (j = 1; j < ny; j++)
                if (gcon[i][j] == 1)
                    con[i][j] = con[i][j] + tau * D * ((con2[i + 1][j] - 2.0 * con2[i][j] + con2[i - 1][j]) / (hx * hx) + (con2[i][j + 1] - 2.0 * con2[i][j] + con2[i][j - 1]) / (hy * hy)) - tau * ((con2[i + 1][j] - con2[i][j]) * (un[i][j] + un[i + 1][j] - fabsl(un[i][j] + un[i + 1][j])) / (4.0 * hx) + (con2[i][j] - con2[i - 1][j]) * (un[i][j] + un[i + 1][j] + fabsl(un[i][j] + un[i + 1][j])) / (4.0 * hx) + (con2[i][j + 1] - con2[i][j]) * (un[i][j + ny] + un[i][j + ny + 1] - fabsl(un[i][j + ny] + un[i][j + ny + 1])) / (4.0 * hy) + (con2[i][j] - con2[i][j - 1]) * (un[i][j + ny] + un[i][j + ny + 1] + fabsl(un[i][j + ny] + un[i][j + ny + 1])) / (4.0 * hy));

        /////// ??????? ???????
        //////////// ?? x

        for (j = 1; j < ny; j++)
            for (i = 1; i < nx; i++)
            {
                if (gcon[i][j] == 1 && cstart == -1)
                {
                    cstart = i - 1;
                    if (gcon[i - 1][j] != -2)
                        con[cstart][j] = con[cstart + 1][j];
                    cend = -1;
                }
                if (gcon[i][j] != 1 && cend == -1)
                {
                    cend = i + 1;
                    if (gcon[i][j] != -2)
                        con[cend - 1][j] = con[cend - 2][j];
                    cstart = -1;
                }
            }

        //////////// ?? y

        for (i = 1; i < nx; i++)
            for (j = 1; j < ny; j++)
            {
                if (gcon[i][j] == 1 && cstart == -1)
                {
                    cstart = j - 1;
                    if (gcon[i - 1][j] != -2)
                        con[i][cstart] = con[i][cstart + 1];
                    cend = -1;
                }
                if (gcon[i][j] != 1 && cend == -1)
                {
                    cend = j + 1;
                    if (gcon[i][j] != -2)
                        con[i][cend - 1] = con[i][cend - 2];
                    cstart = -1;
                }
            }

        //////////////////////////////////////////////////////////////////////////////////////

        ///////////// ????? ? ????

        if (t % 100 == 0 or t == 1) // контролировать частоту выгрузки
        { 
            ff = fopen(concetrFileName, "a");
            exptc(un, con, g, nx, ny, hx, hy, t, ff);
            fclose(ff);
        }

        for (i = 0; i < nx; i++)
        {
            for (j = 0; j < ny; j++)
            {

                Mu[i][j] = mu1 * mu2 / (con[i][j] * mu1 + (1.0 - con[i][j]) * mu2);
                Ro[i][j] = (1.0 - con[i][j]) * ro1 + con[i][j] * ro2;
            }
        }

        t++;
    }

    return 0;
}
