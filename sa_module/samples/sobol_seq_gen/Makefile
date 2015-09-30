all: sobol.o sobol.info

sobol.o: sobol.cc
	g++ -o sobol.o sobol.cc

sobol.info:
	g++ --version > sobol.info
	
sobol.win64: sobol.cc
	g++ -o sobol.win64 sobol.cc

sobol.lin64: sobol.cc
	g++ -o sobol.lin64 sobol.cc

clean:
	rm sobol.o
	rm sobol.info