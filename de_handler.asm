.globl my_de_handler
.extern what_to_do, old_de_handler

.data

.text
.align 4, 0x90
my_de_handler:
    pushq %rbp
    movq %rsp, %rbp

    pushq %rax
    pushq %rdi
    pushq %rsi
    pushq %rdx
    pushq %rcx
    pushq %r8
    pushq %r9
    pushq %r10
    pushq %r11
    movq %rax, %rdi

    call what_to_do
    popq %r11
    popq %r10
    popq %r9
    popq %r8
    popq %rcx
    popq %rdx
    popq %rsi
    popq %rdi
    cmpq $0, %rax
    jne not_zero

    popq %rax
    leave
    jmp *old_de_handler

not_zero:
    
    addq $8, %rsp
    addq $3, 8(%rsp)
    leave
    iretq
