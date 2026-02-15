#include "file_scanner.h"

void add_record(Collections *arr, const char *file_name, char *full_path, long long file_size, long long creation_time, long long last_access_time, long long modified_time)
{
    //There is here Parameters (Collection arr,The file Name of Record,Full Path of File Name,Size Of File,Creation Time ,Access Time,Modified Time,)
    if (arr->num_of_record == arr->max_num_of_record)//Check If The Number of Records become Equal Maximum Number Of Record (Collection become maxed out) 
    {
        arr->max_num_of_record *= 2;//Duplicating The Maximum Number Of Record To Enter More Records
        record *temp = (record *)realloc(arr->records, arr->max_num_of_record * sizeof(record));//Making a Tempory Record to Duplicating the Max Number of Records using>>> Realloc();
        if (temp == NULL) {
            fprintf(stderr, "Realloc failed\n");
            return;
        }
        arr->records = temp;
    }
    //Entering All Data in the Record Struct 
    arr->records[arr->num_of_record].file_name = file_name; 
    arr->records[arr->num_of_record].file_size = file_size;
    arr->records[arr->num_of_record].modified_time = modified_time;
    arr->records[arr->num_of_record].full_path = full_path;
    arr->records[arr->num_of_record].creation_time = creation_time;
    //arr->records[arr->num_of_record].file_type = file_type;
    arr->records[arr->num_of_record].last_access_time = last_access_time;

    arr->num_of_record++; 
}

Collections* Intilize()//Intilize() make a Collection for adding Record Before Start
{
    return create_Collection(100); //create_Collection(Intial max_number of Record)
}

void CleanUp(Collections **arr) // Clean UP ALL Collection and Records using free();
{
    if (arr && *arr)
    {
        for (int i = 0; i < (*arr)->num_of_record; i++)
        {
            free((*arr)->records[i].file_name);
            free((*arr)->records[i].full_path);
        }
        free((*arr)->records);
        free(*arr);
        *arr = NULL;     
    }
}


void Scan_Directory(Collections *Collection_record,const char *directory_path) //Scan_Directory (Collection , Path that you will search on it );
{
    WIN32_FIND_DATAA data;  //it declare a variable that will recieve metadata about file 
    HANDLE hfind;  //It declare a variable the represent a Windows handle 
    char Searched_path[1024];
    // snprintf(new_variable,size of this variable,text,old variable );
    snprintf(Searched_path, sizeof(Searched_path), "%s\\*", directory_path); //snprintf(); it adds the directory path with this (\\*) to let the OS to search all files that in Directory

    hfind=FindFirstFileA(Searched_path,&data); 
    if (hfind==INVALID_HANDLE_VALUE)//hfind doesn't contain metadata it gives an error 
    {
        perror("Cannot Open Directory\n");
        return ;
    }

    do
    {
        if ((data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)|| (strcmp(data.cFileName,".")==0)||(strcmp(data.cFileName,"..")==0)) continue;
        else 
        {
            char full_path[1024];
            long long file_size= ((long long) data.nFileSizeHigh<<32) | (long long) data.nFileSizeLow ;
            snprintf(full_path,sizeof(full_path),"%s\\%s",directory_path,data.cFileName);//snprintf(); it adds the directory path with this (\\ file name) to let the OS to Save a full path of that file 
            char *file_name_copy=_strdup(data.cFileName);
            char *full_path_copy=_strdup(full_path);
            add_record(Collection_record,file_name_copy,full_path_copy,file_size,filetime(data.ftCreationTime),filetime(data.ftLastAccessTime),filetime(data.ftLastWriteTime));

        }
        
    } while (FindNextFileA(hfind,&data));//It search for all metadata that in file and put it in a truct data that will contain all this Information
    
    FindClose(hfind);
}




Collections *create_Collection(int intial_capacity)
{
    Collections *arr = (Collections *)malloc(sizeof(Collections)); //it create One collection with a size of one collection
    if(arr==NULL) return NULL; //If it is not created well ,return NULL
    arr->records = (record *)malloc(intial_capacity * sizeof(record)); //It create a records array with size of the (Intial Capacity*num of intial records ) 
    if(arr->records==NULL) {free(arr);return NULL;}
    arr->num_of_record = 0;
    arr->max_num_of_record = intial_capacity;
    return arr;
}

long long filetime(FILETIME ft)
{
    ULARGE_INTEGER ui;
    ui.LowPart=ft.dwLowDateTime;
    ui.HighPart=ft.dwHighDateTime;
    return (long long) ui.QuadPart;
}
