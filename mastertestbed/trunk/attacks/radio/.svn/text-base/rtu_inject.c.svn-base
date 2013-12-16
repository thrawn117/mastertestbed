#define FORLINUX
#include "modbusrepo/modbus.h"

int main(int argc, char *argv[]) {  
  unsigned char addr, fc, data[255];
  const unsigned char targetfc=0x3;//Function code that we are trying to respond to
  const unsigned char targetbc=5;//byte count that we send on
  int datalen;
  char inport[100], outport[100];
  char inchar;
  
  char tempbytes[512];
  int bytecnt, end, sent;

  int i, j, len, err;
  int in;
  struct modbus_pdu *pdu; 
  struct modbus_pdu *rx_pdu;
  int pducnt = 1;

  strcpy(inport,"/dev/ttyS0");
  strcpy(outport,"/dev/ttyS1");
  
    /* Parse argumentts for port info */
    for (i=1;i<argc;i++) {
        if (strcmp(argv[i], "-inport") == 0) {
            len = strlen(argv[i+1]);
            if (len > 100) {
               printf("Error: Port name must be less then 100 characters long.\n");
               return(-1);
            };
            strncpy(inport, argv[i+1],len+1);//len+1 to ensure \0 gets copied
            i++;
            printf("INFO: Input port = %s\n", inport);
        } else if (strcmp(argv[i], "-outport") == 0) {
          len = strlen(argv[i+1]);
          if (len > 100) {
             printf("Error: Port name must be less then 100 characters long.\n");
             return(-1);
          };
          strncpy(outport, argv[i+1],len); 
          i++;
        } else {
          printf("ERROR: Illegal argument (%s)\n", argv[i]);
          printf("Usage: %s -inport /dev/ttyXX -outport /dev/ttyYY\n", argv[0]);
          return (-1);
        }
    }


    //Open serial port
    in = openport(inport);
    if (in < 0) {
        perror("Error can not open port");
        return (in);
    }

  // Prepare a dummy response. Crafted from Pipeline read
  strcpy(tempbytes,"1210100E101022000000000000000041D80000");
  for(i=0;i<strlen(tempbytes);i+=2) {
    //since the data in the ascii2.log file is ASCII 
    //below convert to binary, 2 bytes ASCII make 1 byte binary
    tobinary(data + (i/2), tempbytes[i], tempbytes[i+1]);
  }
  // used NULL for CRC. It will be calculated when sent.
  pdu = mkpdu(4, 0x3, data, 19, NULL); 
  calc_crc(pdu);
  printf("prepared response...\n");
  printmodbuspdu(pdu);

    while(1) {
        //for each new transaction reset end and bytecnt pointer
        //and clear the tempbytes sting.
        fc=0;
        strcpy(tempbytes,"");

        // Receive request
        rx_pdu = (struct modbus_pdu*) getmodbus_RTU(in);
        fc = rx_pdu->fc;

        // Decrease this number to start response sooner.
        if ((fc==targetfc)){ 
            printf("BR::Sending pdu\n");
            sendmodbus_RTU(in, pdu);
        }
    }
    // This is just printing data received by the port.
    printf("Tempbutes after end: %s", tempbytes);
}

