#ifndef FILE_SCANNER_H_
#define FILE_SCANNER_H_

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

typedef struct
{
    char *file_name;
    char *full_path;
    long long file_size;
    long long creation_time;
    long long last_access_time;
    long long modified_time;

} record;

typedef struct
{
    record *records;
    int num_of_record;    // current number of records
    int max_num_of_record; // maximum number of record before resizing
} Collections;

Collections *create_Collection(int intial_capacity);
long long filetime(FILETIME ft);
void add_record(Collections *arr, const char *file_name, char *full_path, long long file_size, long long creation_time, long long last_access_time, long long modified_time);
Collections* Intilize();
void CleanUp(Collections **arr);
void Scan_Directory(Collections *Collection_record, const char *directory_path);

#endif