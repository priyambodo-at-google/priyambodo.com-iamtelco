#/bin/bash
c=$(docker ps -q) && [[ $c ]] && docker kill $c