#!/usr/bin/env Rscript

library(data.table)
library(ggplot2)

lhist_file <- snakemake@input[["lhist"]]
merged_reads <- snakemake@input[["fq"]]

# run statswrapper
infile <- paste0("in=", merged_reads)
stats_string <- system2("statswrapper.sh",
                        infile,
                        stdout = TRUE)
stats <- fread(paste(stats_string, collapse = "\n"))

# set up a label for the plot
lp <- stats[, paste0(
    "'", round(scaf_bp/1e6, 0),
    " Mb total (",
    n_scaffolds,
    " reads, '*italic('L')[50]==",
    ctg_L50, "*')'")]

# load length histogram
lhist <- fread(lhist_file)

# transform into log4
lhist[, l4_length := log(`#Length`, 4)]

# bin manually
n_bins <- 50
qa <- lhist[, seq(min(l4_length), max(l4_length), length.out = n_bins)]
bin_labels <- sapply(1:length(qa), function(i)
    mean(c(qa[i], qa[i + 1])))[c(1:n_bins - 1)]
lhist[, lbin := as.numeric(
    as.character(
        cut(l4_length, breaks = qa,
            labels = bin_labels,
            include.lowest = TRUE)))]
lhist_log4 <- lhist[, .(count = sum(Count)), by = lbin]

# plot
gp <- ggplot(lhist_log4, aes(x = lbin, y = count)) +
    ggtitle(parse(text = lp)) +
    scale_x_continuous(labels = function(x) 4^x) +
    ylab("Count") + xlab("Read length") +
    geom_col()

# write output
ggsave(filename = snakemake@output[["plot"]],
    plot = gp,
    device = "pdf",
    width = 10,
    height = 7.5,
    units = "in")
