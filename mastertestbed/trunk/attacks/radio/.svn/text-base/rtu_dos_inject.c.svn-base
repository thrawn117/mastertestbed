#define FORLINUX
#include <pthread.h>
#include "modbusrepo/modbus.h"

#warning BR::Remember to compile with -lpthread
//Globals
struct modbus_pdu* global_pdu_fake;
int in, out;   //Port file descriptors
int flag_sendpkt = 0;

#define GARBAGE_LEN 1 
const char GARBAGE[GARBAGE_LEN]="q";
void * thread_output(void* pParam);
void * thread_input(void* pParam);
void * make_fake_pdu(struct modbus_pdu** pdu_fake);

int main(int argc, char* argv[])
{
     //Data variables
     char inport[100], outport[100];
     int i, j, len, err;

     //Threading variables
     pthread_t pid_output;
     pthread_t pid_input;
     pthread_attr_t attr;
     void *pRetVal;

    strcpy(inport,"/dev/ttyS0");
    strcpy(outport,"/dev/ttyS1");
    
    //Read command line options
    for (i=1;i<argc;i++) {
      if (strcmp(argv[i], "-inport") == 0) {
        len = strlen(argv[i+1]);
        //printf("BR:: Length of argument %d+1 = %d", i, len);
        if (len > 100) {
           printf("Error: Port name must be less then 100 characters long.\n");
           return(-1);
        };
        memset(inport, '\0', 100);
        strncpy(inport, argv[i+1],len); 
        i++;
        printf("INFO: Input port = %s\n", inport);
      } else {
        printf("ERROR: Illegal argument (%s)\n", argv[i]);
        printf("Usage: %s -inport /dev/ttyXX -outport /dev/ttyYY\n", argv[0]);
        return (-1);
      }
    }

    in = openport(inport);
    if (in < 0) {
      perror("Error can not open port");
      return (in);
    }

    out =in; 
    //manufacture pdu
    make_fake_pdu(&global_pdu_fake);
    printmodbuspdu(global_pdu_fake);

    //Set kernel mode threading
    pthread_attr_init(&attr);
    pthread_attr_setscope(&attr, PTHREAD_SCOPE_SYSTEM);

    printf("BR::Starting threads\n");
    pthread_create(&pid_output, &attr, thread_input, NULL);
    pthread_create(&pid_input, &attr, thread_output, NULL);
    
    
    //Run join on all threads
    pthread_join(pid_output, &pRetVal);
    pthread_join(pid_input, &pRetVal);
    return 0;
}

void * thread_output(void* pParam)
{
    while(1){
      if(flag_sendpkt){
        sendmodbus_RTU(out, global_pdu_fake);
        printf("BR:: Sent packet\n");
        flag_sendpkt--;
      } else {
        write(out, GARBAGE ,GARBAGE_LEN);//Write garbage to the port
      }
    }
    return NULL;
}

void * thread_input(void* pParam)
{
    struct modbus_pdu *pdu;
    int targetfc=0x03;
    while(1){
      pdu = getmodbus_RTU(in);
      printf("BR::Recv'd packet \t fc: 0x%X \n", pdu->fc); 
      if (pdu->fc == targetfc){
        sendmodbus_RTU(out, global_pdu_fake);
        flag_sendpkt++;
        sched_yield();//Yield to ensure that we stop here
      }
    }
    return NULL;
}

void * make_fake_pdu(struct modbus_pdu** pdu_fake)
{
    struct modbus_pdu* pdu_temp;
    unsigned char addr=4;
    unsigned char fc=3;
    int datalen=19;
    unsigned char empty[2]={0};
    unsigned char data[]={
        0x12, 0x10, 0x10, 0x0e,\
		0x10, 0x10, 0x22, 0x00,\
		0x00, 0x00, 0x00, 0x00,\
		0x00, 0x00, 0x00, 0x41,\
		0xd8, 0x00, 0x00};

    *(pdu_fake) = mkpdu(addr, fc, data, datalen, empty);
    calc_crc(*pdu_fake);

    printmodbuspdu(*pdu_fake);
    return;
}
