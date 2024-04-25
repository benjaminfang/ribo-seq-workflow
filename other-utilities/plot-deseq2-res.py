#!/usr/bin/env python3
"""
Plot mean-expression result generated by DESeq2.
"""
import argparse
import matplotlib.pyplot as plt
import numpy as np


def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="out")
    parser.add_argument("deres", help="result file from DESeq2")
    args = parser.parse_args()

    return args.out, args.deres


def plot_ma(data, ax):
    l2fc_max = 5
    data = data.T
    meanexp = data[0]
    l2fc = data[1]
    padj = data[5]

    out_mean = []
    out_l2fc = []
    out_color = []
    out_alpha = []
    out_edc = []
    out_edw = []

    in_mean = []
    in_l2fc = []
    in_color = []
    in_alpha = []
    in_edc = []
    in_edw = []

    for me, fc, pj in zip(meanexp, l2fc, padj):
        if abs(fc) > l2fc_max:
            out_mean.append(me)
            if fc > 0:
                out_l2fc.append(l2fc_max)
            else:
                out_l2fc.append(-l2fc_max)
            
            if np.isnan(pj):
                out_color.append("white")
                out_alpha.append(.5)
                out_edc.append("black")
                out_edw.append(.1)
            else:
                if pj >= .01:
                    out_color.append("gray")
                    out_alpha.append(.5)
                    out_edc.append("gray")
                    out_edw.append(0)
                else:
                    out_color.append("red")
                    out_alpha.append(1)
                    out_edc.append("gray")
                    out_edw.append(0)
        else:
            in_mean.append(me)
            in_l2fc.append(fc)
            if np.isnan(pj):
                in_color.append("white")
                in_alpha.append(.5)
                in_edc.append("black")
                in_edw.append(.1)
            else:
                if pj < .01 and abs(fc) > 1:
                    in_color.append("red")
                    in_alpha.append(1)
                    in_edc.append("gray")
                    in_edw.append(0)
                else:
                    in_color.append("gray")
                    in_alpha.append(.5)
                    in_edc.append("gray")
                    in_edw.append(0)
    if len(out_mean) > 0:
        ax.scatter(out_mean, out_l2fc, color=out_color, alpha=out_alpha, \
                s=5, linewidths=out_edw, edgecolor=out_edc, marker="^")
    ax.scatter(in_mean, in_l2fc, color=in_color, alpha=in_alpha, \
               linewidths=in_edw, edgecolor=in_edc, marker="o", s=5)
    ax.set_xscale("log", base=10)
    ax.set_ylim([-5.5, 5.5])
    ax.set_xlabel("mean expression")
    ax.set_ylabel("$log_2$ fold change of expression")


def read_deres(deres):
    data = []
    geneids = []
    fin = open(deres, "r")
    fin.readline()
    for line in fin:
        line =[ele.strip('"') for ele in line.rstrip().split(",")]
        geneids.append(line[0])
        new_line = []
        for ele in line[1:]:
            if ele == "NA":
                new_line.append(np.NAN)
            else:
                new_line.append(float(ele))
        data.append(new_line)
    return geneids, np.asarray(data)


def main():
    out, deres = getargs()
    geneids, data = read_deres(deres)
    fig, ax = plt.subplots(layout="constrained")
    plot_ma(data, ax)
    fig.savefig(out + "-ma.svg")


if __name__ == "__main__":
    main()