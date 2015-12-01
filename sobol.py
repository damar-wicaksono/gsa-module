"""Driver script to compute Sobol' Sensitivity Indices on some function
"""
import sys
import gsa_module

__author__ = "Damar Wicaksono"


def main():
    """Main entry point for the script."""

    n = 2000
    d = 10
    scheme = "sobol"
    gen_path = "./gsa_module/samples/sobol_seq_gen"
    params_sobol = ["./gsa_module/samples/sobol_seq_gen/sobol.o",
                    "./gsa_module/samples/sobol_seq_gen/new-joe-kuo-6.21201"]
    # make the executable for the generator
    gsa_module.samples.sobol.makegen("make", gen_path)
    dm = gsa_module.sobol.sobol_saltelli.create(n, d, scheme, params_sobol)
    # write down
    tag = "sobol_{}_{}" .format(n, d)
    gsa_module.sobol.sobol_saltelli.write(dm, tag)
    # clean the executable for the generator
    gsa_module.samples.sobol.makegen("clean", gen_path)


if __name__ == "__main__":
    sys.exit(main())
