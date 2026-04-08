#!/bin/bash  
  
for i in {0..254}  
do  
	# sed "s/.$//" - substitui o último caractere qualquer ("s/.$) por nada (//")  
	ping -c 1 "$1.$i" | grep "ttl" | cut -d " " -f 4 | sed "s/.$//" &   
done
