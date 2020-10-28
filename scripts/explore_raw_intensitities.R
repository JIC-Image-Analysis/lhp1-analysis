library(tidyverse)

aggregate.data <- read_csv("../../20200309_lhp1_W10_T14.csv")
ggplot(aggregate.data) + geom_histogram(aes(x=mean_intensity), bins=50)  + facet_wrap(vars(sname))
ggsave("T14-count-histograms.png") 
ggplot(aggregate.data) + geom_histogram(aes(x=mean_intensity), bins=50)

setwd("~/projects/image_analysis/lhp1/results/stats/")

data <- read_csv("20200309_lhp1_W10_T14-SDB995-5_01-stats.csv")
ggplot(data, aes(intensity)) + geom_count(aes(y=count)) + scale_y_log10()

ggplot(data, aes(x=intensity, y=count)) + geom_bar(stat="identity") + scale_y_log10()


data <- read_csv("../../aggregate_counts.csv")
ggplot(data, aes(x=intensity, y=count)) + geom_bar(stat="identity") + scale_y_log10() + facet_wrap(vars(sname))

by(data, data[, "sname"], weighted.mean(data$intensity, data$count))

a <- data %>%
  group_by(sname) %>%
  do(wm=weighted.mean(.$intensity, .$count))
