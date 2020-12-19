#include <asm/desc.h>

void my_store_idt(struct desc_ptr *idtr) {
    asm("SIDT (%0);"
       :
       :"r" (idtr)
    );
}

void my_load_idt(struct desc_ptr *idtr) {
    asm("LIDT (%0);"
       :
       :"r" (idtr)
    );
}

void my_set_gate_offset(gate_desc *gate, unsigned long addr) {
    asm("movw %%ax, (%0);"
        "shrq $16, %%rax;"
        "movw %%ax, 6(%0);"
        "shrq $16, %%rax;"
        "movl %%eax, 8(%0)"
       :
       :"r" (gate), "a" (addr) 
    );
}

unsigned long my_get_gate_offset(gate_desc *gate) {
    unsigned long addr;

    asm("movw (%1), %%ax;"
        "rorq $16, %%rax;"
        "movw 6(%1), %%ax;"
        "rorq $16, %%rax;"
        "movw 8(%1), %%ax;"
        "rorq $16, %%rax;"
        "movw 10(%1), %%ax;"
        "rorq $16, %%rax"
       :"=a" (addr)
       :"r" (gate)
    );

    return addr;
}
