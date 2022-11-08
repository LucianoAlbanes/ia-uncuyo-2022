# Slow (rate-limited to 1 request), but I don't want to pay $ to google

library(readr)
library(dplyr)
library(httr)
library(jsonlite)


train_file <- './train_balanced_both.csv'
train <- read_csv(train_file)

get_elevation <- function(lat, long) {
  base <- 'https://api.open-elevation.com/api/v1/lookup?locations='
  API_URL <- paste0(base, lat, "," , long)
  
  raw_data <- GET(API_URL)
  results <- fromJSON(rawToChar(raw_data$content), flatten = TRUE)
  
  results$results$elevation
}

get_elevation_v <- Vectorize(get_elevation)

new_train <- train %>% 
  mutate(elevation = get_elevation_v(lat, long), .after=long)

write_csv(new_train, paste0(train_file, "._elevation"))

