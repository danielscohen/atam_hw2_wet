.section .data
input: .fill 25, 1, 0

/* STACK: */
/* ========== */
/* COUNTER */
/* ---------- */
/* IS_COMPLEX */
/* ---------- */
/* TO_CONVERT */
/* ---------- */
/* DUMMY */
/* ---------- */
/* LHS */
/* ---------- */
/* OP */
/* ---------- */
/* RHS */
/* ========== */


.section .text
.global	calc_expr
calc_expr:
	pushq %rbp
	movq %rsp, %rbp
    xorq  %rax, %rax
    call evaluate
end:
    movq %rax, %rdi
    call result_as_string
    movq $1, %rdi
    movq $what_to_print, %rsi
    movq %rax, %rdx
    movq $1, %rax
    syscall

    leave
    ret

evaluate: 
	pushq %rbp
	movq %rsp, %rbp
	pushq $0
	pushq $0
	pushq $0
loop:
	movq -8(%rbp), %rdi
	pushq %rax
	call getchar
	popq %rax
	movq -8(%rbp) ,%r8 /*counter*/
	cmpb $10, input(,%r8,1) /* new line */
	jne not_end	
	leave
	ret
not_end:
	movq -8(%rbp) ,%r8 /*counter*/
	cmpb $40, input(,%r8,1) /* "(" */
	jne not_lp
	incq -8(%rbp)  /* counter++ */
	call evaluate /* recursive call */
	pushq %rax /* res of recursion */  
	jmp loop
not_lp:
	movq -8(%rbp) ,%r8 /*counter*/
	cmpb $41, input(,%r8,1) /* ")" */
	jne not_rp
	cmpq $1, -24(%rbp)
	jne already_number
	/* conversion */
	movq -8(%rbp) ,%r8 /*counter*/
	movb $0, input(,%r8,1)
	movq $input, %rdi
	call string_convert
	pushq %rax /* res of conversion */
    movq $0, -24(%rbp)
already_number:
    /* check if double expression */
	cmpq $1, -16(%rbp) 
    jne single

    /* lhs => r8 */
    movq -32(%rbp), %r8
    /* rhs => r9 */
    movq -48(%rbp), %r9
    /* op => r10 */
    movq -40(%rbp), %r10
    
    jmp *%r10

add:
    addq %r8, %r9
    movq %r9, %rax 
    jmp finnish
    
sub:
    subq %r9, %r8
    movq %r8, %rax 
    jmp finnish

mul:
    imul %r8, %r9
    movq %r9, %rax 
    jmp finnish

div:
    movq %r8, %rax
    cqo
    idiv %r9
    jmp finnish

single:
    movq -32(%rbp), %rax
        
finnish:
    leave
    ret	

not_rp:
	movq -8(%rbp) ,%r8 /*counter*/
    movb input(,%r8,1), %r11b
    cmpb $48, %r11b
    jae num
    cmpb $45, %r11b
    jne not_minus
    cmpq $0, -8(%rbp)    
    je num
not_minus:
	cmpq $1, -24(%rbp)
	jne is_conv
	/* conversion */
	movq -8(%rbp) ,%r8 /*counter*/
	movb $0, input(,%r8,1)
	movq $input, %rdi
    pushq %r11
	call string_convert
    popq %r11
	pushq %rax /* res of conversion */
    movq $0, -24(%rbp)
is_conv:
    incq -16(%rbp)
    movq $0, -8(%rbp)
	cmpb $43, %r11b /* "+" */
    je plus
	cmpb $45, %r11b /* "-" */
    je minus
	cmpb $42, %r11b /* "*" */
    je times
	cmpb $47, %r11b /* "/" */
    je quo

num:
    incq -8(%rbp)
    movq $1, -24(%rbp)
    jmp loop
    
plus:
    pushq $add
    jmp loop

minus:
    pushq $sub
    jmp loop
	
times:
    pushq $mul
    jmp loop

quo:
    pushq $div
    jmp loop


getchar:
	pushq %rbp
	movq %rsp, %rbp
	addq $input, %rdi /* will work beacuse char = 1byte. moving counter to array in order to perform array[i] */
	movq %rdi, %rsi
	movq $0, %rax
	movq $0, %rdi
	movq $1, %rdx
	syscall
	leave 
	ret


