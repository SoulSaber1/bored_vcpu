#include <stdio.h>
#include <stdlib.h>

unsigned int *code;
unsigned int *mem;


unsigned int reg[4] = {0,0,0,0};
unsigned int cmp = 0;
unsigned int pc = 0;
char hlt = 0;


#define incpc pc+=4
#define CODE_SIZE 128
#define MEM_SIZE 64

void print_cpu_state(){
  printf("CPU State:\nr0:  0x%08x\nr1:  0x%08x\n"
  "r2:  0x%08x\nr3:  0x%08x\ncmp: 0x%08x\npc:  0x%08x\nhlt: 0x%x\n\n",
  reg[0],reg[1],reg[2],reg[3],cmp,pc,hlt);
}

void print_mem_state(){
  printf("MEM Contents:\n");
  for(int i=0; i<MEM_SIZE; i++){
    printf("0x%08x ", mem[i]);
  }
  printf("\n");
}

void cpu(){
  int op = code[pc];
  switch (op){
    case 0x0:       //set hlt
      hlt = 1;
      incpc;
      break;

    //mov family opcodes
    case 0x1:       //mov regA->regB
      reg[code[pc+1]] = reg[code[pc+2]];
      incpc;
      break;
    case 0x2:       //mov val->reg
      reg[code[pc+1]] = code[pc+2];
      incpc;
      break;
    case 0x3:       //mov reg->mem
      mem[code[pc+1]] = reg[code[pc+2]];
      incpc;
      break;
    case 0x4:       //mov val->mem
      mem[code[pc+1]] = code[pc+2];
      incpc;
      break;
    case 0x5:       //mov mem->reg
      reg[code[pc+1]] = mem[code[pc+2]];
      incpc;
      break;

    //cmp family
    case 0x10:       //compare rA and rB
      cmp = (reg[code[pc+1]] == reg[code[pc+2]]);
      incpc;
      break;

    //math - add/sub
    case 0x20:      //add rA to rB; store rA
      reg[code[pc+1]] = reg[code[pc+1]]+reg[code[pc+2]];
      incpc;
      break;
    case 0x21:      //add v1 to rA; store rA
      reg[code[pc+1]] = reg[code[pc+1]]+code[pc+2];
      incpc;
      break;
    case 0x22:      //add mem to rA; store in rA
      reg[code[pc+1]] = reg[code[pc+1]]+mem[code[pc+2]];
      incpc;
      break;
    case 0x23:      //add rA to mem; store in mem
      mem[code[pc+1]] = mem[code[pc+1]]+reg[code[pc+2]];
      incpc;
      break;
    case 0x24:      //add val to mem; store in mem
      mem[code[pc+1]] = mem[code[pc+1]]+code[pc+2];
      incpc;
      break;
    case 0x25:      //sub rB from rA; store rA
      reg[code[pc+1]] = reg[code[pc+1]]-reg[code[pc+2]];
      incpc;
      break;
    case 0x26:      //sub v1 from rA; store rA
      reg[code[pc+1]] = reg[code[pc+1]]-code[pc+2];
      incpc;
      break;
    case 0x27:      //sub mem from rA; store in rA
      reg[code[pc+1]] = reg[code[pc+1]]-mem[code[pc+2]];
      incpc;
      break;
    case 0x28:      //sub rA from mem; store in mem
      mem[code[pc+1]] = mem[code[pc+1]]-reg[code[pc+2]];
      incpc;
      break;
    case 0x29:      //sub val from mem; store in mem
      mem[code[pc+1]] = mem[code[pc+1]]-code[pc+2];
      incpc;
      break;
    case 0x2a:      //add mem2 to mem1; store in mem1
      mem[code[pc+1]] = mem[code[pc+1]]+mem[code[pc+2]];
      incpc;
      break;
    case 0x2b:      //sub mem2 from mem1; store in mem1
      mem[code[pc+1]] = mem[code[pc+1]]-mem[code[pc+2]];
      incpc;
      break;

    //jmp family opcodes
    case 0x40:       //jmp
      pc += code[pc+1];
      break;
    case 0x41:       //je
      if(cmp){ pc += code[pc+1]; }
      else { incpc; }
      break;

    //other utility opcodes
    case 0x90:      //nop
      incpc;
      break;
    case 0x91:      //print register info
      printf("\nREG DIS CALL\n");
      print_cpu_state();
      incpc;
      break;
    case 0x92:      //print memory info
      printf("\nMEM DIS CALL\n");
      print_mem_state();
      incpc;
      break;
    default:
      printf("INVALID OPCODE\n");
      hlt = 1;
      incpc;
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
  code = (unsigned int *)calloc(CODE_SIZE, sizeof(int));
  mem = (unsigned int *)calloc(MEM_SIZE, sizeof(int));
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
  if(argc < 2){
    printf("Usage is %s input\n", argv[0]);
    exit(-1);
  }
  printf("Begin emulation:\n\n");
  int ret = emulate(argv[1]);
  printf("End emulation\n");
  return ret;
}
