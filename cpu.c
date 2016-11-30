#include <stdio.h>
#include <stdlib.h>

int *code;
int *mem;
unsigned int reg[4] = {0,0,0,0};
unsigned int cmp = 0;
unsigned int pc = 0;
unsigned int hlt = 0;

void print_cpu_state(){
  printf("CPU State:\nr0:  0x%x\nr1:  0x%x\n"
    "r2:  0x%x\nr3:  0x%x\ncmp: 0x%x\npc:  0x%x\nhlt: 0x%x\n\n",
    reg[0],reg[1],reg[2],reg[3],cmp,pc,hlt);
}

void print_mem_state(){
  printf("MEM Contents:\n");
  for(int i=0; i<1024; i++){
    printf("%x", mem[i]);
  }
}

void cpu(){
  int op = code[pc];
  switch (op){
    case 0x0:       //set hlt
      pc += 4;
      hlt = 1;
      break;
    //mov family opcodes
    case 0x1:       //mov val->reg
      reg[code[pc+1]] = code[pc+2];
      pc += 4;
      break;
    case 0x2:       //mov regA->regB
      reg[code[pc+1]] = reg[code[pc+2]];
      pc += 4;
      break;

    //cmp family
    case 0x10:       //compare rA and rB
      cmp = (reg[code[pc+1]] == reg[code[pc+2]]);
      pc += 4;
      break;

    //jmp family opcodes
    case 0x30:       //jmp
      pc += code[pc+1];
      break;
    case 0x31:       //je
      if(cmp){ pc += code[pc+1]; }
      else { pc += 4; }
      break;

    //other utility opcodes
    case 0x90:      //nop
      pc += 4;
      break;
    case 0x91:      //print register info
      pc += 4;
      printf("\nREG DIS CALL\n");
      print_cpu_state();
      break;
    default:
      pc += 4;
      break;
  }
}

void get_code(char *filename){
  FILE *code_file = fopen(filename, "rb");
  fseek(code_file, 0L, SEEK_END);
  int sz = ftell(code_file);
  fseek(code_file, 0L, SEEK_SET);
  fread(code, 4, sz/4, code_file);
  fclose(code_file);
}

int emulate(char *filename){
  code = (int *)calloc(4096, sizeof(char));
  mem = (int *)calloc(1024, sizeof(char));
  get_code(filename);
  unsigned int old_pc = -1;
  while(!hlt && old_pc != pc){
    old_pc = pc;
    cpu();
  }
  if(old_pc == pc && !hlt){ printf("\npc didnt change; program hung\n"); }
  print_cpu_state();
  free(mem);
  free(code);
  return reg[0];
}

int main(int argc, char **argv){
  printf("Begin emulation:\n\n");
  int ret = emulate(argv[1]);
  printf("End emulation\n");
  return ret;
}
