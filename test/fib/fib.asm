.global _boot
.text

# RISC-V assembly code to generate Fibonacci numbers

_boot:
    # Fibonacci sequence in registers s1 and s2
    li s1, 1  # s1 will hold the current Fibonacci number
    li s2, 0  # s2 will hold the previous Fibonacci number
    li s3, 10 # s3 will hold the number of Fibonacci numbers to generate

.loop:
    beq s3, zero, .done # If s3 (counter) is zero, exit the loop
    add t0, s1, s2       # t0 = current + previous
    mv s2, s1           # Move current to previous
    mv s1, t0           # Move new Fibonacci number to current
    addi s3, s3, -1      # Decrement the counter

    # Print the current Fibonacci number
    li a7, 1            # syscall number for print integer
    mv a0, s1           # Move the current Fibonacci number to a0
    ecall                # make the syscall

    j .loop              # Repeat the loop

.done:
    # Exit the program
    li a7, 10            # syscall number for exit
    ecall                # make the syscall

