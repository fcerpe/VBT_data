
library(BayesFactor)
library(dplyr)

# Quick script for specific analyses, will be improved later

# Read table
accuracies <- read.csv('../../outputs/derivatives/stats/VBT_data-test_variable-accuracy_table.csv')

# Get relevant data: different tables based on sesssion / day
ses1 <- accuracies[accuracies$day == 1, c("subject", "script", "target")]
ses2 <- accuracies[accuracies$day == 2, c("subject", "script", "target")]
ses3 <- accuracies[accuracies$day == 3, c("subject", "script", "target")]
ses4 <- accuracies[accuracies$day == 4, c("subject", "script", "target")]

# compute 4 ttests with bayes factor
ttest1 <- t.test(target ~ script, data = ses1, var.eq = TRUE)
ttest2 <- t.test(target ~ script, data = ses2, var.eq = TRUE)
ttest3 <- t.test(target ~ script, data = ses3, var.eq = TRUE)
ttest4 <- t.test(target ~ script, data = ses4, var.eq = TRUE)

ttest1_bf <- ttestBF(formula = target ~ script, data = ses1)
ttest2_bf <- ttestBF(formula = target ~ script, data = ses2)
ttest3_bf <- ttestBF(formula = target ~ script, data = ses3)
ttest4_bf <- ttestBF(formula = target ~ script, data = ses4)

bf1 <- extractBF(ttest1_bf)
bf2 <- extractBF(ttest2_bf)
bf3 <- extractBF(ttest3_bf)
bf4 <- extractBF(ttest4_bf)

# save results 
results <- read.csv('../../outputs/derivatives/results/VBT_data-test_variable-accuracy_analysis-posthoc.csv')

bf_data <- data.frame(session = c("session-1", "session-2", "session-3", "session-4"),
                      bf = c(bf1$bf, bf2$bf, bf3$bf, bf4$bf),
                      error = c(bf1$error, bf2$error, bf3$error, bf4$error))

# Merge the bf_data into the main results by session
results <- merge(results, bf_data, by = "session")

# Save and overwrite
write.csv(results, "../../outputs/derivatives/results/VBT_data-test_variable-accuracy_analysis-posthoc.csv", row.names = FALSE)







