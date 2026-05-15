# get_fluview_data.R --------------------------------------------

if (!requireNamespace("cdcfluview", quietly = TRUE)) {
  message("Installing 'cdcfluview' …")
  install.packages("cdcfluview", repos = "https://cloud.r-project.org")
}
library(cdcfluview)
library(dplyr)
library(readr)

year <- 2025                    # change for next season

flu_national <- ilinet("national", years = year)

flu_regional <- ilinet("hhs", years = year) %>% 
  filter(region == "Region 9")

nat_PIC <- pi_mortality(year = year) %>% unique()

reg_PIC <- pi_mortality("region", year = year) %>% 
  unique() %>% 
  filter(region_name == "Region 9")

st_PIC <- pi_mortality("state", year = year) %>% 
  unique() %>% 
  filter(region_name == "Nevada")

dir.create("downloads", showWarnings = FALSE)
write_csv(flu_national, "downloads/flu_national.csv")
write_csv(flu_regional, "downloads/flu_regional.csv")
write_csv(nat_PIC,      "downloads/nat_pic_mortality.csv")
write_csv(reg_PIC,      "downloads/reg_pic_mortality.csv")
write_csv(st_PIC,       "downloads/nv_pic_mortality.csv")