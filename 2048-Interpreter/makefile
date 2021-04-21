2048: game.tab.cc game.yy.cc game.h game.cpp
	g++ -w -o 2048 -g game.tab.cc game.yy.cc game.h game.cpp
game.tab.cc: game.y
	bison -d --warnings=none game.y -o game.tab.cc

game.yy.cc : game.l
	flex -o game.yy.cc game.l

clean:
	rm -f game.yy.cc game.tab.* 2048