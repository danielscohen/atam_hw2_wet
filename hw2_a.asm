.global main
.section .data
counter: .int  0
input: .ascii 25
.section .text
main:
    xorq  %rax, %rax
    call evaluate

    ret

evaluate: 
	pushq %rbp
	movq %rsp, %rbp
	pushq $0 //counter 
	pushq $0 //flag is complex
	pushq $0 //flag num to convert
loop:
	movq -8(%rbp), %rdi
	pushq %rax
	call getchar
	popq %rax
	cmpb $10, input /* new line */
	jne not_end	
	leave
	ret
not_end:
	cmpb $40, input /* "(" */
	jne not_(
	inc -8(%rbp)  /* counter++ */
	pushq %rax
	call evaluate /* recursive call */
	pushq %rax /* res of recursion */  
	jmp loop
not_(:
	cmpb $41, input /* ")" */
	jne not_)
	cmpq $1, -24(%rbp)
	jne already_number
	/* conversion */
	movq -8(%rbp) ,%r8 /*counter*/
	addb $0, input(,%r8,1)
	movq $input, %rdi
	call string_convert
	pushq %rax /* res of conversion */
	...


	
not_):

	
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
	
	
	
	