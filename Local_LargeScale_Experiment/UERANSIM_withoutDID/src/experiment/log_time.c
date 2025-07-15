#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>
#include <time.h>
#include "log_time.h"

void log_time(const char *event_description,const char *filename){
    
    FILE *file = fopen(filename, "a");
    if (file == NULL ){
        perror("Failed to open file");
        exit(1);
    }
    
    
    struct timeval tv;
    gettimeofday(&tv,NULL);

    //time now
    time_t now = tv.tv_sec;

    // transfer the time to readable form
    struct tm *timeinfo;
    timeinfo = localtime(&now);

    //write to the file
    char buffer[80];
    strftime(buffer,sizeof(buffer),"%Y-%m-%d %H:%M:%S",timeinfo);
    fprintf(file, "%s: %s.%06ld\n", event_description, buffer, tv.tv_usec);

    fclose(file);

}

