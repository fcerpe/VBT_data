
library(BayesFactor)
library(dplyr)


### Subfunctions

compute_bayes_factors <- function(pathIn) {
  
  # Read table
  measure <- read.csv(pathIn)
  
  # Initialize empty lists to store results
  ttest <- list()
  ttest_bf <- list()
  bf <- list()
  
  # Extract the sessions to loop through
  sessions <- sort(unique(measure$day))
  
  # Loop through each session (day)
  for (day in sessions) {
    # Subset data for the current day
    ses <- measure[measure$day == day, c("subject", "script", "target")]
    
    # Perform t-test
    ttest[[day]] <- t.test(target ~ script, data = ses, var.eq = TRUE)
    
    # Perform Bayes Factor t-test
    ttest_bf[[day]] <- ttestBF(formula = target ~ script, data = ses)
    
    # Extract Bayes Factor
    bf[[day]] <- extractBF(ttest_bf[[day]])
  }
  
  # If we are dealing with the training data, there are only three sessions
  if (length(sessions) == 3) {
    
    # Delete the first BF as it's empty
    bf <- bf[-1]
  }
  
  # Store as table
  bf_gpt <- data.frame(session = paste0("session-", sessions),
                       bf = sapply(bf, function(x) x$bf),
                       error = sapply(bf, function(x) x$error))
  
  compute_bayes_factors <- bf_gpt
  
}

overwrite_posthocs <- function(bfs, path) {
  
  # Read posthocs file
  posthoc <- read.csv(path)
  
  # Merge the bf_data into the main results by session
  results <- merge(posthoc, bfs, by = "session")
  
  # Save and overwrite
  write.csv(results, path, row.names = FALSE)
}



# Compute Bayes Factors for post-hoc t-tests
# 
# 'compute_bayes_factors' will  
# - load the prompted measure
# - compute t-tests and bayes factors for those t-tests
# - store everything as a table with session, bf, error
#
# 'overwrite_posthocs' will
# - open the post-hocs analyses made in python (script: stats_accuracy_timing.py: line 146)
# - concatenate the BFs
# - save everything 


# Test accuracy
test_accuracy_bf <- compute_bayes_factors('../../outputs/derivatives/stats/VBT_data-test_variable-accuracy_table.csv')
overwrite_posthocs(test_accuracy_bf, '../../outputs/derivatives/results/VBT_data-test_variable-accuracy_analysis-posthoc.csv')

# Test writing time
test_writing_bf <- compute_bayes_factors('../../outputs/derivatives/stats/VBT_data-test_variable-writing-time_table.csv')
overwrite_posthocs(test_writing_bf, '../../outputs/derivatives/results/VBT_data-test_variable-writing-time_analysis-posthoc.csv')

# Training reading time
train_reading_bf <- compute_bayes_factors('../../outputs/derivatives/stats/VBT_data-training_variable-reading-time_table.csv')
overwrite_posthocs(train_reading_bf, '../../outputs/derivatives/results/VBT_data-training_variable-reading-time_analysis-posthoc.csv')






