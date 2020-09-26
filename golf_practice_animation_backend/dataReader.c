#include <stdio.h>
#include <stdlib.h>
//#include <python.h>
#include <pigpio.h>

double test();
/*
   gcc -pthread -o dataReader dataReader.c -lpigpio
   gcc -shared -Wl,-soname,dataReader -pthread -o dataReader.so -fPIC dataReader.c -lpigpio
   ./dataReader 100000 5000000
*/

int main(int argc, char *argv[])
{
    int i;
    int j;
    int h;
    int v;
    int loops;
    int speed;
    int channel = 4;
    double start, diff, sps;
    unsigned char buf[3];

    if (argc > 1) loops = atoi(argv[1]);
    else loops = 1000000;

    if (argc > 2) speed = atoi(argv[2]);
    else speed = 1000000;

    if (gpioInitialise() < 0) return 1;

    h = spiOpen(0, speed, 0);

    if (h < 0) return 2;

    start = time_time();

    for (i=0; i<loops; i++)
    {
        if ((time_time() - start) < 0.00005*i)
        {
            i--;
            continue;
        }
        for (j=0; j<channel; j++)
        {
            buf[0] = 1;
            buf[1] = (8+j)<<4;
            buf[2] = 0;

            spiXfer(h, buf, buf, 3);

            v = ((buf[1]&3)<<8) | buf[2];

            //printf("%d | channel %d\n", v, j);

        }
        //time_sleep(0.00005);
    }

    diff = time_time() - start;

    fprintf(stderr, "sps=%.1f @ %d bps (%d/%.1f)\n",
      (double)loops / diff, speed, loops, diff);

    spiClose(h);

    gpioTerminate();

    return 0;
}

double test()
{
    int i;
    int j;
    int h;
    int v;
    int loops;
    int speed;
    int channel = 4;
    double start, diff, sps;
    unsigned char buf[3];

    loops = 10;

    speed = 5000000;

    if (gpioInitialise() < 0) return 1;

    h = spiOpen(0, speed, 0);

    if (h < 0) return 2;

    start = time_time();

    for (i=0; i<loops; i++)
    {
        if ((time_time() - start) < 0.00005*i)
        {
            i--;
            continue;
        }
        for (j=0; j<channel; j++)
        {
            buf[0] = 1;
            buf[1] = (8+j)<<4;
            buf[2] = 0;

            spiXfer(h, buf, buf, 3);

            v = ((buf[1]&3)<<8) | buf[2];

            printf("%d | channel %d\n", v, j);

        }
        //time_sleep(0.00005);
    }

    diff = time_time() - start;

    fprintf(stderr, "sps=%.1f @ %d bps (%d/%.1f)\n",
      (double)loops / diff, speed, loops, diff);

    spiClose(h);

    gpioTerminate();

    return (double)loops / diff;
}
