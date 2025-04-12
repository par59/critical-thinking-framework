# Load required package
if (!require("dplyr")) install.packages("dplyr", dependencies=TRUE)
library(dplyr)

# File to store your productivity log
log_file <- "productivity_log.csv"

# Function to log a task
log_task <- function(task, minutes_spent) {
  entry <- data.frame(
    Date = Sys.Date(),
    Task = task,
    Minutes = minutes_spent
  )
  
  if (file.exists(log_file)) {
    write.table(entry, log_file, sep = ",", append = TRUE, row.names = FALSE, col.names = FALSE)
  } else {
    write.csv(entry, log_file, row.names = FALSE)
  }
  
  cat("✅ Task logged!\n")
}

# Function to summarize today's productivity
summarize_today <- function() {
  if (!file.exists(log_file)) {
    cat("No log file found.\n")
    return()
  }
  
  data <- read.csv(log_file)
  today <- Sys.Date()
  
  summary <- data %>%
    filter(Date == as.character(today)) %>%
    group_by(Task) %>%
    summarise(Total_Minutes = sum(Minutes)) %>%
    arrange(desc(Total_Minutes))
  
  cat("\n📊 Today's Summary:\n")
  print(summary)
}

# Example usage:
# log_task("Learning R", 30)
# log_task("Writing report", 45)
# summarize_today()
