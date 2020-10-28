library(ggplot2)

data.lhp1 <- read.csv("projects/image_analysis/lhp1/local-data/lhp1_test.csv")
data.lhp1['mean_intensity'] = data.lhp1$total_intensity / data.lhp1$voxels
data.t7.series23 <- data.lhp1[(data.lhp1$file == '20200113_10W_T7.lif') & (data.lhp1$series_name == 'Series023'),]

ggplot(data.t7.series23, aes(mean_intensity)) + geom_histogram(aes(x=mean_intensity))
ggplot(data.t7.series23, aes(mean_intensity)) + geom_density(aes(x=mean_intensity))

freq <- hist(data.t7.series23$mean_intensity, breaks=20)

mdensity <- density(data.t7.series23$mean_intensity)
df <- data.frame(x=mdensity$x, y=mdensity$y)
fit <- nls(y ~ C1 * exp(-(x-mean1)**2/(2 * sigma1**2)) + C2 * exp(-(x-mean2)**2/(2 * sigma2**2)), data=df, start=list(C1=4.0, mean1=0.2, sigma1=0.1, C2=2.0, mean2=0.4, sigma2=0.2), algorithm='port')

fitted.values <- coef(fit)

C1 <- fitted.values['C1']
C2 <- fitted.values['C2']
mean1 <- fitted.values['mean1']
mean2 <- fitted.values['mean2']
sigma1 <- fitted.values['sigma1']
sigma2 <- fitted.values['sigma2']

off_area = C1 * sigma1
on_area = C2 * sigma2

fun1 <- function(x) C2 * exp(-(x-mean2)**2/(2 * sigma2**2))
fun2 <- function(x) C1 * exp(-(x-mean1)**2/(2 * sigma1**2))
fun3 <- function(x) C2 * exp(-(x-mean2)**2/(2 * sigma2**2)) + C1 * exp(-(x-mean1)**2/(2 * sigma1**2))

plot <- ggplot(df, aes(x=x, y=y)) +
  geom_line() +
  stat_function(fun = fun1, color='red') +
  stat_function(fun = fun2, color='green') +
  stat_function(fun = fun3, color='blue')

plot

sum(data.t7.series23$mean_intensity < 0.3)
sum(data.t7.series23$mean_intensity > 0.3)

