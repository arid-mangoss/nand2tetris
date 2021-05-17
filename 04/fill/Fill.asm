// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// while true :
//     if *KBD > 0:
//         set all pixels to black
//     else: 
//         set all pixels to white

(loop)
    @KBD
    D=M

    @black
    D;JGT

    @white
    D;JEQ

    (black) // make all the pixels black

        @blackCounter
        M=0

        (blackLoop)
            @blackCounter
            D=M

            @8192
            D=A-D
            @loop
            D;JLE

            @blackCounter
            D=M

            @SCREEN
            A=A+D
            M=-1

            @blackCounter
            M=M+1

            @blackLoop
            0;JMP

        @loop // back to beginning
        0;JMP


    (white) // make all the pixels white

        @whiteCounter
        M=0

        (whiteLoop)
            @whiteCounter
            D=M

            @8192
            D=A-D
            @loop
            D;JLE

            @whiteCounter
            D=M

            @SCREEN
            A=A+D
            M=0

            @whiteCounter
            M=M+1

            @whiteLoop
            0;JMP

        @loop // back to beginning
        0;JMP

@loop // back to beginning
0;JMP

// end of program
(end)
@end
0;JMP