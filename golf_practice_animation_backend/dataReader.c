#include <stdio.h>
#include <stdlib.h>
//#include <python.h>
#include <pigpio.h>
#define CHANNEL 4
#define SAMPLE_RATE 20000
//#define SAMPLE_RATE 1
#define DETECT_RATE 1000
//#define DETECT_RATE 1
#define SPEED 5000000
#define SIZE 100

/*
   gcc -pthread -o dataReader dataReader.c -lpigpio
   gcc -shared -Wl,-soname,dataReader -pthread -o dataReader.so -fPIC dataReader.c -lpigpio
   ./dataReader 100000 5000000
*/

int detect(double* data_set, double high_threshold, double low_threshold, int size);
void sample(int h, int loops, double low_threshold, double* data_set);


int main(int argc, char *argv[])
{
    //double data_set[100][CHANNEL];
    //detect(data_set, 100,100,100);

    return 0;
}

int detect(double* data_set, double high_threshold, double low_threshold, int size)
{
    int j;
    int h;
    int v;
    int is_threshold_channel = 0;
    int is_threshold = 0;

    double start, sps;
    unsigned char buf[3];

    start = time_time();

    //if (gpioInitialise() < 0) return 1;
    if (gpioInitialise() < 0) return 0;

    h = spiOpen(0, SPEED, 0);

    //if (h < 0) return 2;
    if (h < 0) return 0;

    printf("Start detecting\n");
    while (1)
    {
        if ((time_time() - start) > 1/DETECT_RATE)
        {
            start = time_time();
            printf("----------\n");
            for (j=0; j<CHANNEL; j++)
            {

                buf[0] = 1;
                buf[1] = (8+j)<<4;
                buf[2] = 0;

                spiXfer(h, buf, buf, 3);

                v = ((buf[1]&3)<<8) | buf[2];
//                printf("Channel %d | %d | %f v\n", j, v, (float)v/1023.0*3.3);
                if (v>high_threshold && (j==0||j==2) || (v+30)>high_threshold && (j==1||j==3))
                {

                    is_threshold_channel++;
                }

            }
            if (is_threshold_channel>=2 && is_threshold>=5)
            {
                printf("==========\n");
                printf("Start sampling\n");
                sample(h, size, low_threshold, data_set);
                printf("Sampling finish\n");
                break;
            }
            else if(is_threshold_channel>=2)
            {
                is_threshold++;
            }
            else
            {
                is_threshold=0;
            }
            is_threshold_channel=0;
        }
    }

    //Finish sampling
    spiClose(h);

    gpioTerminate();
    return 1;
}

void sample(int h, int loops, double low_threshold, double* data_set)
{
    int i;
    int j;
    int is_finish = 0;
    int is_finish_channel = 0;
    int v;
    double start, diff, sps;
    unsigned char buf[3];

    start = time_time();
    for (i=0; i<loops; i++)
    {

        if ((time_time() - start) < 1/SAMPLE_RATE*i)
        {
            i--;
            continue;
        }
        else
        {
            printf("#%d\n", i);
            for (j=0; j<CHANNEL; j++)
            {
                buf[0] = 1;
                buf[1] = (8+j)<<4;
                buf[2] = 0;

                spiXfer(h, buf, buf, 3);

                v = ((buf[1]&3)<<8) | buf[2];
                data_set[i*CHANNEL+j] = v;
//                printf("Channel %d | %d | %f v\n", j, v, (float)v/1023.0*3.3);
                if (v<low_threshold && (j==0||j==2) || (v+30)<low_threshold && (j==1||j==3))
                {
                    is_finish_channel++;
                }
            }

            if (is_finish_channel>=2 && is_finish>=5)
            {
                break;
            }
            else if(is_finish_channel>=2)
            {
                is_finish++;
            }
            else
            {
                is_finish=0;
            }

            is_finish_channel=0;
            //time_sleep(0.00005);
        }
    }

    diff = time_time() - start;

    fprintf(stderr, "sps=%.1f @ %d bps (%d/%.1f)\n",
      (double)loops / diff, SPEED, loops, diff);
}
