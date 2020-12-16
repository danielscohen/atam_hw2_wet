#include <asm/desc.h>

void my_store_idt(struct desc_ptr *idtr) {
    asm("SIDT %0"
       :
       :"m" (idtr)
    );
}

void my_load_idt(struct desc_ptr *idtr) {
    asm("LIDT %0"
       :"m" (idtr)
       :
    );
}

void my_set_gate_offset(gate_desc *gate, unsigned long addr) {
// <STUDENT FILL>
	// TODO: pack_gate(gate, GATE_INTERRUPT, addr, 0, 0, __KERNEL_CS);
// </STUDENT FILL>
    asm("movw %%ax, (%1);
         shrq $16, %%rax;
         movw %%ax, 6(%1);
         shrq $16, %%rax;
         movl %%eax, 8(%1);"
       :
       :"a" (addr), "r" (gate)
    );
}

unsigned long my_get_gate_offset(gate_desc *gate) {
// <STUDENT FILL>
	// TODO: return gate_offset(gate);
// </STUDENT FILL>
    unsigned long addr;

    asm("movw (%1), %%ax;
         rorq $16, %rax;
         movw 6(%1), %%ax;
         rorq $16, %rax;
         movw 8(%1), %%ax;
         rorq $16, %rax;
         movw 10(%1), %%ax;
         rorq $16, %rax;"
       :"a" (addr)
       :"r" (gate)
    );

    return addr;
}
